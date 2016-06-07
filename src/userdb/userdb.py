'''
Created on 12 Aug 2013

@author: hicksj
'''

import sqlite3
from exceptions import Exception
import random
from emailsend.emailsender import EmailSender
import re
import string
from smtplib import SMTPRecipientsRefused
from emailsend.settings import Settings
from pages import settings

class UserException(Exception):
    emailNotFound = "Email address not found"
    emailOrPasswordNotFound = "Email address and/or password not found"
    userNotActive = "User is not active - you must activate your ID before you can login"
    sessionExpired = "Session expired"
    emailAlreadyExists = "A user with this e-mail address already exists"
    userNotFound = "User not found"
     
    def __init__(self, message, cause=None):
        self.message = message
        self.cause = cause
        
    def __str__(self):
        if self.cause is None:
            answer = self.message
        else:
            answer = "{{0}\nCaused by: {1}}".format(self.message, self.cause)
        return answer

class UserDetails():
    def __init__(self, userid, name, email, club, token=None, status=None, failurecount=0):
        self.userId = userid
        self.name = name
        self.email = email
        self.club = "" if club is None else club
        self.roles = []
        self.token = token
        self.status = status
        self.failurecount = failurecount

class UserDatabase:
    activeStatus = "active"
    inactiveStatus = "inactive"
    
    def __init__(self, userdb="{0}/users.db".format(settings.Settings.usersDirectory), emailSender=None):
        self.userdb = userdb
        self.emailSender = EmailSender() if emailSender is None else emailSender
        self.blockList = []
        self.blockList.append("u03.gmailmirror.com")
        
    def getConnection(self, externalConn):
        if externalConn is not None:
            answer = externalConn
        else:
            answer = sqlite3.connect(self.userdb)
        return answer

    def closeConnectionIfNecessary(self, externalConn, conn):
        if conn is not None and conn is not externalConn:
            conn.close()
        
    def login(self, email, password, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            self.clearExpiredSessions(conn)
            sql = "select u.id, u.status from user u, password p where u.id = p.id and u.email = ? and p.password = ?"
            c.execute(sql, (email, password))
            row = c.fetchone()
            if row is None:
                raise UserException(UserException.emailOrPasswordNotFound)
            userId, status = row
            if status == UserDatabase.inactiveStatus:
                raise UserException(UserException.userNotActive)
            token = self.generateToken(userId)
            c.execute("delete from session where id = ?", (userId,))
            c.execute("insert into session (id, token, expiry) values(?, ?, datetime('now', '+1 day', 'localtime'))", (userId, token))
            conn.commit()
        except sqlite3.Error as ex:
            raise UserException("Error logging in", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
        return token
        
    def generateToken(self, userid):
        randValue = random.randint(0, 0xFFFFFF)
        answer = "{0:X}{1:X}".format(userid, randValue)
        return answer

    def clearExpiredSessions(self, conn):
        c = conn.cursor()
        c.execute("delete from session where expiry < datetime('now', 'localtime')")
        conn.commit()
        
    def checkSessionToken(self, token, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            self.clearExpiredSessions(conn)
            if c.execute("select id from session where token = ?", (token,)).fetchone() is None:
                raise UserException(UserException.sessionExpired)
        except sqlite3.Error as ex:
            raise UserException("Error checking session token", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
        
    def registerUser(self, email, name, club, password, externalConn=None):
        if self.isBlocked(email):
            return -1
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            if c.execute("select id from user where email = ?", (email,)).fetchone() is not None:
                raise UserException(UserException.emailAlreadyExists)
            c.execute("insert into user (name, email, club, status, failurecount) values(?, ?, ?, ?, 0)", (name, email, club, UserDatabase.inactiveStatus))
            answer = c.execute("select last_insert_rowid()").fetchone()[0]
            c.execute("insert into password(id, password) values(?, ?)", (answer, password))
            self.sendActivationEmail(answer, conn)
            self.notifyAdmin("register", answer, conn)
            conn.commit()
        except sqlite3.Error as ex:
            raise UserException("Error registering user", ex)
        finally:
            if not conn is None:
                self.closeConnectionIfNecessary(externalConn, conn)
        return answer
    
    def remindOfPassword(self, email, externalConn=None):
        if self.isBlocked(email):
            return -1
        try:
            conn = self.getConnection(externalConn)
            try:
                row = conn.cursor().execute("select id from user where email = ?", (email,)).fetchone()
                if row is None:
                    raise UserException(UserException.emailNotFound)
                userId, = row
                self.sendPasswordReminderEmail(userId, email, externalConn=conn)
            finally:
                self.closeConnectionIfNecessary(externalConn, conn)
        except sqlite3.Error as ex:
            raise UserException("Error sending password reminder", ex)
        
    
    def activateUser(self, userId, externalConn=None):
        return self.setUserStatus(userId, self.activeStatus, True, externalConn)

    def toggleUserStatus(self, userId, currentStatus,externalConn=None):
        newStatus = self.activeStatus if currentStatus == self.inactiveStatus else self.inactiveStatus
        return self.setUserStatus(userId, newStatus, False, externalConn)

    def setUserStatus(self, userId, status, notifyAdmin, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            c.execute("update user set status = ? where id = ?", (status, userId))
            if c.rowcount == 0:
                raise UserException(UserException.userNotFound)
            row = c.execute("select name, email, club from user where id = ?", (userId,)).fetchone()
            name, email, club = row
            answer = UserDetails(userId, name, email, club)
            if notifyAdmin:
                self.notifyAdmin("activate", userId, conn)
            conn.commit()
            return answer
        except sqlite3.Error as ex:
            raise UserException("Error activating user", ex)
        finally:
            if not conn is None:
                self.closeConnectionIfNecessary(externalConn, conn)

    def createDatabase(self, externalConn=None, recreate=False):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            if recreate:
                for index in ["email", "token"]:
                    try:
                        c.execute("drop index {0}".format(index))
                    except:
                        pass
                for table in ["user", "password", "session", "role"]:
                    try:
                        c.execute("drop table {0}".format(table))
                    except:
                        pass
            c.execute("create table user (id integer primary key, name text, email text, club text, status text, failurecount integer)")
            c.execute("create table password (id integer primary key, password text)")
            c.execute("create table session (id integer, token text, expiry timestamp)")
            c.execute("create table role (id integer, role text)")
            c.execute("create unique index email on user(email asc)")
            c.execute("create unique index token on session(token asc)")
            conn.commit()
        except sqlite3.Error as ex:
            raise UserException("Error creating database", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)

    def sendActivationEmail(self, userId, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            row = c.execute("select email from user where id = ?", (userId,)).fetchone()
            if row is not None:
                email, = row
                message = """
                Thank you for registering as a user of the South-East Hampshire Indoor Cricket League site.
                Your e-mail address (to which this message was sent) is your user name.
                
                Before you can use your account, you must activate it, which you can do by clicking the link below.
                http://sehicl.hampshire.org.uk/cgi-bin/page.py?id=activate&user={user}
                
                If you experience any problems with the activation process, please reply to this e-mail stating what problem you saw.
                
                Many thanks,
                The Webmaster
                """.format(user=userId)
                message = string.join([l.strip() for l in re.split("\n", message)], "\n")
                self.emailSender.sendMessage([email], "Activate your SEHICL account", message)
        except sqlite3.Error as ex:
            raise UserException("Error looking up e-mail address", ex)
        except SMTPRecipientsRefused as ex:
            raise UserException("Unable to send e-mail to specified address", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)

    def sendPasswordReminderEmail(self, userId, email, externalConn=None):
        try:
            conn = self.getConnection(externalConn)
            try:
                c = conn.cursor()
                row = c.execute("select password from password where id = ?", (userId,)).fetchone()
                if row is not None:
                    password, = row
                    message = """
                        This is a password reminder for your account as a registered user of the South-East Hampshire Indoor Cricket League site.

                        Your e-mail address (to which this message was sent) is your user name. Your password is {password}.

                        If you did not request this password reminder, please inform the Webmaster.
                
                        Many thanks,
                        The Webmaster
                    """.format(password=password)
                    message = string.join([l.strip() for l in re.split("\n", message)], "\n")
                    self.emailSender.sendMessage([email], "SEHICL password reminder", message)
            finally:
                self.closeConnectionIfNecessary(externalConn, conn)
        except sqlite3.Error as ex:
            raise UserException("Error looking up password", ex)
        except SMTPRecipientsRefused as ex:
            raise UserException("Unable to send e-mail to specified address", ex)

    def sessionHasRole(self, token, role, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            sql = "select count(*) from session s, role r where s.id = r.id and s.token = ? and r.role = ?"
            count, = c.execute(sql, (token, role)).fetchone()
            answer = count != 0
        except sqlite3.Error as ex:
            raise UserException("Error looking up role for token", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
        return answer
    
    def notifyAdmin(self, action, userId, externalConn=None):
        message = """
        Account details:
        User ID: {userid}
        Name: {name}
        Club: {club}
        Email: {email}
        """
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            sql = "select name, club, email from user where id = ?"
            name, club, email = c.execute(sql, (userId,)).fetchone()
            clubTxt = "(Not specified)" if club is None else club
            msg = message.format(userid=userId, name=name, club=clubTxt, email=email)
            msg = string.join([m.strip() for m in string.split(msg, "\n")], "\n")
            subject = "User action: {0}".format(action)
            self.emailSender.sendMessage([Settings.adminEmail], subject, msg)
        except sqlite3.Error as ex:
            raise UserException("Error looking up role for token", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
            
    def getUserList(self, externalConn=None):
        answer = []
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            sql = """
            select u.id, u.name, u.club, u.email, r.role, s.token, u.status, u.failurecount
            from
            user u left outer join role r on u.id = r.id
            left outer join session s on u.id = s.id 
            order by u.id
            """
            user = None
            for row in c.execute(sql).fetchall():
                userid, name, club, email, role, token, status, failurecount = row
                if user is None or userid != user:
                    user = UserDetails(userid, name, email, club, token, status, failurecount)
                    answer.append(user)
                if role is not None:
                    user.roles.append(role)
        except sqlite3.Error as ex:
            raise UserException("Error Fetching user list", ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
        return answer
    
    def getUserDetails(self, userId, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            sql = "select u.id, u.name, u.club, u.email, r.role from user u left outer join role r on u.id = r.id where u.id = ?"
            user = None
            for row in c.execute(sql, (userId,)).fetchall():
                userid, name, club, email, role = row
                if user is None or userid != user:
                    user = UserDetails(userid, name, email, club)
                    answer = user
                if role is not None:
                    user.roles.append(role)
        except sqlite3.Error as ex:
            raise UserException("Error looking up details of user {0}".format(userId), ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
        return answer
    
    def deleteUser(self, userId, externalConn=None):
        try:
            conn = None
            conn = self.getConnection(externalConn)
            c = conn.cursor()
            tables = ["password", "session", "role", "user"]
            for t in tables:
                sql = "delete from {0} where id = ?".format(t)
                c.execute(sql, (userId,))
            conn.commit()
        except sqlite3.Error as ex:
            raise UserException("Error looking up details of user {0}".format(userId), ex)
        finally:
            self.closeConnectionIfNecessary(externalConn, conn)
    
    def isBlocked(self, email):
        answer = False
        for b in self.blockList:
            answer = string.find(email, b) != -1
            if answer:
                break
        return answer