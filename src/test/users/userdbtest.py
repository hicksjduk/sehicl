'''
Created on 12 Aug 2013

@author: hicksj
'''
import unittest
import sqlite3
from userdb.userdb import UserDatabase, UserException
import random
from datetime import datetime, timedelta
from emailsend.settings import Settings

class EmailMessage:
    
    def __init__(self, addressees, subject, message):
        self.addressees = addressees
        self.subject = subject
        self.message = message

class DummyEmailSender:
    
    def __init__(self):
        self.messages = []
    
    def sendMessage(self, addressees, subject, message):
        self.messages.append(EmailMessage(addressees, subject, message))

class Test(unittest.TestCase):

    def testLoginConnectionNotSpecifiedIDNotFound(self):
        dbName = "users/users.db"
        database = UserDatabase(dbName)
        database.createDatabase(None, True)
        try:
            database.login("hello", "goodbye")
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.emailOrPasswordNotFound, ex.message)
            self.assertEquals(None, ex.cause)

    def testLoginUserIDNotFound(self):
        conn = self.inMemoryDatabaseConnection()
        try:
            UserDatabase().login("hello", "goodbye", conn)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.emailOrPasswordNotFound, ex.message)
            self.assertEquals(None, ex.cause)

    def testLoginUserIDFoundPasswordIncorrect(self):
        conn = self.inMemoryDatabaseConnection()
        try:
            c = conn.cursor()
            c.execute("insert into user (name, email, status) values(?, ?, ?)", ("Jeremy", "hello", UserDatabase.activeStatus))
            userId = c.execute("select last_insert_rowid()").fetchone()[0]
            c.execute("insert into password(id, password) values(?, ?)", (userId, "asfsdagsa"))
            UserDatabase().login("hello", "goodbye", conn)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.emailOrPasswordNotFound, ex.message)
            self.assertEquals(None, ex.cause)

    def testLoginUserIDFoundPasswordCorrectUserInactive(self):
        conn = self.inMemoryDatabaseConnection()
        try:
            c = conn.cursor()
            c.execute("insert into user (name, email, status) values(?, ?, ?)", ("Jeremy", "hello", UserDatabase.inactiveStatus))
            userId = c.execute("select last_insert_rowid()").fetchone()[0]
            c.execute("insert into password(id, password) values(?, ?)", (userId, "goodbye"))
            UserDatabase().login("hello", "goodbye", conn)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.userNotActive, ex.message)
            self.assertEquals(None, ex.cause)

    def testLoginUserIDFoundPasswordCorrectUserActive(self):
        conn = self.inMemoryDatabaseConnection()
        c = conn.cursor()
        c.execute("insert into user (name, email, status) values(?, ?, ?)", ("Jeremy", "hello", UserDatabase.activeStatus))
        userId = c.execute("select last_insert_rowid()").fetchone()[0]
        c.execute("insert into password(id, password) values(?, ?)", (userId, "goodbye"))
        random.seed(123)
        result = UserDatabase().login("hello", "goodbye", conn)
        expectedToken = "1D67B3"
        self.assertEquals(expectedToken, result)
        expiry, token = c.execute("select s.expiry, s.token from session s, user u where s.id = u.id").fetchone()
        self.assertEquals(expectedToken, token)
        expectedDate = datetime.now() + timedelta(1)
        msg = "{0}, {1}".format(expectedDate, expiry)
        self.assertTrue(expectedDate - datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S") < timedelta(0, 1), msg)

    def testGenerateToken(self):
        random.seed(123)
        result = UserDatabase().generateToken(12411)
        self.assertEquals("307BD67B3", result)
        
    def testClearExpiredSessions(self):
        conn = self.inMemoryDatabaseConnection()
        c = conn.cursor()
        now = datetime.now()
        for i in range(-3, 4, 2):
            date = now + timedelta(seconds=i)
            c.execute("insert into session(id, token, expiry) values(?, ?, ?)", (i + 12, "token{0}".format(i), date))
        count = c.execute("select count(*) from session").fetchone()[0]
        self.assertEquals(4, count)
        UserDatabase().clearExpiredSessions(conn)
        count = c.execute("select count(*) from session").fetchone()[0]
        self.assertEquals(2, count)
        
    def testCheckSessionTokenDoesNotExist(self):
        token = "theToken"
        conn = self.inMemoryDatabaseConnection()
        try:
            UserDatabase().checkSessionToken(token, conn)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.sessionExpired, ex.message)
            self.assertEquals(None, ex.cause)

    def testCheckSessionConnectionNotSpecifiedTokenDoesNotExist(self):
        token = "theToken"
        dbName = "users/users.db"
        database = UserDatabase(dbName)
        database.createDatabase(None, True)
        try:
            UserDatabase(dbName).checkSessionToken(token)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.sessionExpired, ex.message)
            self.assertEquals(None, ex.cause)

    def testCheckSessionTokenExistsButHasExpired(self):
        token = "theToken"
        conn = self.inMemoryDatabaseConnection()
        conn.cursor().execute("insert into session(id, token, expiry) values(1, ?, datetime('now', '-2 minutes', 'localtime'))", (token,))
        try:
            UserDatabase().checkSessionToken(token, conn)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.sessionExpired, ex.message)
            self.assertEquals(None, ex.cause)

    def testCheckSessionTokenExistsAndHasNotExpired(self):
        token = "theToken"
        conn = self.inMemoryDatabaseConnection()
        conn.cursor().execute("insert into session(id, token, expiry) values(1, ?, datetime('now', '+2 minutes', 'localtime'))", (token,))
        UserDatabase().checkSessionToken(token, conn)
        
    def testRegisterEmailAlreadyExists(self):
        conn = self.inMemoryDatabaseConnection()
        email = "jeremy"
        name = "Jeremy"
        team = "Rotherham"
        password = "password"
        conn.cursor().execute("insert into user (email) values('jeremy')")
        try:
            UserDatabase().registerUser(email, name, team, password, conn)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEquals(UserException.emailAlreadyExists, ex.message)
            self.assertEquals(None, ex.cause)

    def testRegisterEmailDoesNotAlreadyExistClubSpecified(self):
        conn = self.inMemoryDatabaseConnection()
        email = "jeremy"
        name = "Jeremy"
        club = "Rotherham"
        password = "password"
        userDb = UserDatabase()
        userDb.emailSender = DummyEmailSender()
        result = userDb.registerUser(email, name, club, password, conn)
        c = conn.cursor()
        row = c.execute("select id, email, name, club, status from user").fetchone()
        self.assertEquals((result, email, name, club, UserDatabase.inactiveStatus), row)
        row = c.execute("select password from password where id = ?", (result,)).fetchone()
        self.assertEquals((password,), row)
        self.assertEquals([email], userDb.emailSender.messages[0].addressees)
        self.assertEquals([Settings.adminEmail], userDb.emailSender.messages[1].addressees)


    def testRegisterEmailDoesNotAlreadyExistClubSpecifiedConnectionNotSpecified(self):
        dbName = "users/users.db"
        userDb = UserDatabase(dbName)
        userDb.emailSender = DummyEmailSender()
        userDb.createDatabase(None, True)
        email = "jeremy"
        name = "Jeremy"
        club = "Rotherham"
        password = "password"
        result = userDb.registerUser(email, name, club, password)
        conn = userDb.getConnection(None)
        c = conn.cursor()
        try:
            row = c.execute("select id, email, name, club, status from user").fetchone()
            self.assertEquals((result, email, name, club, UserDatabase.inactiveStatus), row)
            row = c.execute("select password from password where id = ?", (result,)).fetchone()
            self.assertEquals((password,), row)
        finally:
            conn.close()
        self.assertEquals([email], userDb.emailSender.messages[0].addressees)
        self.assertEquals([Settings.adminEmail], userDb.emailSender.messages[1].addressees)

    def testRegisterEmailDoesNotAlreadyExistClubNotSpecified(self):
        conn = self.inMemoryDatabaseConnection()
        email = "jeremy"
        name = "Jeremy"
        club = None
        password = "password"
        userDb = UserDatabase()
        userDb.emailSender = DummyEmailSender()
        result = userDb.registerUser(email, name, club, password, conn)
        c = conn.cursor()
        row = c.execute("select id, email, name, club, status from user").fetchone()
        self.assertEquals((result, email, name, club, UserDatabase.inactiveStatus), row)
        row = c.execute("select password from password where id = ?", (result,)).fetchone()
        self.assertEquals((password,), row)
        self.assertEquals([email], userDb.emailSender.messages[0].addressees)
        self.assertEquals([Settings.adminEmail], userDb.emailSender.messages[1].addressees)
        
    def testActivateUserIdNotFoundConnectionNotSpecified(self):
        dbName = "users/users.db"
        database = UserDatabase(dbName)
        database.createDatabase(None, True)
        userId = 3
        try:
            database.activateUser(userId)
            self.fail("Should have thrown an exception")
        except UserException as ex:
            self.assertEqual(UserException.userNotFound, ex.message)
            self.assertEqual(None, ex.cause)

    def testActivateUserIdFoundAndAlreadyActive(self):
        conn = self.inMemoryDatabaseConnection();
        userId = 3
        c = conn.cursor()
        c.execute("insert into user(id, status) values(?, ?)", (userId, UserDatabase.activeStatus))
        userDb = UserDatabase()
        userDb.emailSender = DummyEmailSender()
        userDb.activateUser(userId, conn)
        row = c.execute("select status from user where id = ?", (userId,)).fetchone()
        self.assertEquals((UserDatabase.activeStatus,), row)
        self.assertEquals([Settings.adminEmail], userDb.emailSender.messages[0].addressees)

    def testActivateUserIdFoundAndInactive(self):
        conn = self.inMemoryDatabaseConnection();
        userId = 3
        c = conn.cursor()
        c.execute("insert into user(id, status) values(?, ?)", (userId, UserDatabase.inactiveStatus))
        userDb = UserDatabase()
        userDb.emailSender = DummyEmailSender()
        userDb.activateUser(userId, conn)
        row = c.execute("select status from user where id = ?", (userId,)).fetchone()
        self.assertEquals((UserDatabase.activeStatus,), row)
        self.assertEquals([Settings.adminEmail], userDb.emailSender.messages[0].addressees)
        
    def inMemoryDatabaseConnection(self):
        dbName = ":memory:"
        conn = sqlite3.connect(dbName)
        UserDatabase().createDatabase(conn)
        return conn
    
    def testSendActivationEmail(self):
        conn = self.inMemoryDatabaseConnection();
        userId = 3
        email = "jeremy@thehickses.org.uk"
        c = conn.cursor()
        c.execute("insert into user(id, email) values(?, ?)", (userId, email))
        sender = DummyEmailSender()
        userDb = UserDatabase(emailSender=sender)
        userDb.sendActivationEmail(userId, conn)
        self.assertEquals([email], sender.messages[0].addressees)
        
    def testSessionHasRoleSessionNotInDbRoleNotInDb(self):
        conn = sqlite3.connect(":memory:")
        UserDatabase().createDatabase(conn)
        token = "hello"
        role = "admin"
        result = UserDatabase().sessionHasRole(token, role, conn)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testSessionHasRoleSessionInDbRoleNotInDb(self):
        conn = sqlite3.connect(":memory:")
        UserDatabase().createDatabase(conn)
        token = "hello"
        role = "admin"
        c = conn.cursor()
        c.execute("insert into session (id, token) values (?, ?)", (1, token))
        result = UserDatabase().sessionHasRole(token, role, conn)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testSessionHasRoleSessionNotInDbRoleInDb(self):
        conn = sqlite3.connect(":memory:")
        UserDatabase().createDatabase(conn)
        token = "hello"
        role = "admin"
        c = conn.cursor()
        c.execute("insert into role (id, role) values (?, ?)", (1, role))
        result = UserDatabase().sessionHasRole(token, role, conn)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testSessionHasRoleSessionInDbRoleInDbForDifferentUser(self):
        conn = sqlite3.connect(":memory:")
        UserDatabase().createDatabase(conn)
        token = "hello"
        role = "admin"
        c = conn.cursor()
        c.execute("insert into session (id, token) values (?, ?)", (1, token))
        c.execute("insert into role (id, role) values (?, ?)", (2, role))
        result = UserDatabase().sessionHasRole(token, role, conn)
        expectedResult = False
        self.assertEqual(expectedResult, result)

    def testSessionHasRoleSessionInDbRoleInDbForSameUser(self):
        conn = sqlite3.connect(":memory:")
        UserDatabase().createDatabase(conn)
        token = "hello"
        role = "admin"
        c = conn.cursor()
        c.execute("insert into session (id, token) values (?, ?)", (1, token))
        c.execute("insert into role (id, role) values (?, ?)", (1, role))
        result = UserDatabase().sessionHasRole(token, role, conn)
        expectedResult = True
        self.assertEqual(expectedResult, result)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testLoginFailed']
    unittest.main()