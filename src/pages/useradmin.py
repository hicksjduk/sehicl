'''
Created on 13 Sep 2013

@author: hicksj
'''
from pages.page import Page
from userdb.userdb import UserDatabase
import string
from pages.pageLink import PageLink

class UserAdmin(Page):

    def __init__(self, pageId, params={}, role=None):
        Page.__init__(self, pageId, params, role)
        
    def getTitle(self):
        return "SEHICL User Administration"
    
    def getContent(self, externalConn=None):
        action = self.allParams.get("action", None)
        if action is None:
            answer = self.getUserListPage(externalConn)
        elif action == "delete":
            answer = self.getUserDeleteConfirmationPage(self.allParams.get("user", None), externalConn)
        elif action == "togglestatus":
            currentStatus = self.allParams.get("status", None)
            UserDatabase().toggleUserStatus(self.allParams.get("user", None), currentStatus, externalConn)
            answer = self.getUserListPage(externalConn);
        elif action == "confirmdelete":
            UserDatabase().deleteUser(self.allParams.get("user", None), externalConn)
            answer = self.getUserListPage(externalConn)
        elif action == "canceldelete":
            answer = self.getUserListPage(externalConn)
        else:
            answer = action
        return answer
        
    def getUserListPage(self, externalConn=None):
        html = """
        <h1>User Administration</h1>
        <table id="users">
            <thead>
                <tr>
                    <th class="userid">ID</th>
                    <th class="name">Name</th>
                    <th class="email">E-mail</th>
                    <th class="club">Club</th>
                    <th class="status" colspan="2">Status</th>
                    <!--
                    <th class="failurecount">Failed logins</th>
                    -->
                    <th class="roles">Roles</th>
                </tr>
            </thead>
            <tbody>
                {users}
            </tbody>
        </table>
        """
        return html.format(users=string.join(self.getUsers(), "\n"))
    
    def getUsers(self, externalConn=None):
        html = """
        <tr>
            <td class="userid">{user.userId}</td>
            <td class="name">{user.name}</td>
            <td class="email">{user.email}</td>
            <td class="club">{club}</td>
            <td class="status action">{user.status}</td>
            <td class="action">
                {statusform}
            </td>
            <!--
            <td class="failurecount">{user.failurecount}</td>
            -->
            <td class="roles">{roles}</td>
            <td class="action">
                {deleteform}
            </td>
            <!--
            <td class="action">
                <form action="{thispage.url}" method="post">
                    <input type="hidden" name="action" value="addrole">
                    <input type="hidden" name="user" value="{user.userId}">
                    <input type="text" name="role">
                    <input type="submit" value="Add role">
                </form>
            </td>
            -->
        </tr>
        """
        answer = []
        for user in UserDatabase().getUserList(externalConn):
            club = "" if user.club is None else user.club
            thisPage = PageLink(self.pageId, self)
            roles = string.join(user.roles, ",")
            deleteForm = self.getUserDeleteActionForm(user, thisPage)
            statusForm = self.getToggleUserStatusActionForm(user, thisPage)
            answer.append(html.format(user=user, club=club, roles=roles, thispage=thisPage, deleteform=deleteForm, statusform=statusForm))
        return answer
    
    def getUserDeleteActionForm(self, user, thisPage):
        html = """
        <form action="{thispage.url}" method="post">
            <input type="hidden" name="action" value="delete">
            <input type="hidden" name="user" value="{user.userId}">
            <input type="submit" value="Delete">
        </form>
        """
        if self.allParams.get("session", None) == user.token:
            answer = ""
        else:
            answer = html.format(user=user, thispage=thisPage)
        return answer
    
    def getToggleUserStatusActionForm(self, user, thisPage):
        html = """
        <form action="{thispage.url}" method="post">
            <input type="hidden" name="action" value="togglestatus">
            <input type="hidden" name="user" value="{user.userId}">
            <input type="hidden" name="status" value="{user.status}">
            <input type="submit" value="{buttontext}">
        </form>
        """
        if self.allParams.get("session", None) == user.token:
            answer = ""
        else:
            buttonText = "Activate" if user.status == UserDatabase.inactiveStatus else "Deactivate"
            answer = html.format(user=user, thispage=thisPage, buttontext=buttonText)
        return answer
    
    def getUserDeleteConfirmationPage(self, userId, externalConn=None):
        html = """
        <h1>Please confirm</h1>
        <p>You have requested to delete the user with the following details:</p>
        <table>
            <tr><td>User ID: {user.userId}</td></tr>
            <tr><td>Name: {user.name}</td></tr>
            <tr><td>E-mail: {user.email}</td></tr>
            <tr><td>Club: {club}</td></tr>
            <tr><td>Roles: {roles}</td></tr>
        </table>
        <p>Press Delete to confirm and delete this user, or Cancel to cancel the deletion.</p>
        <table id="users">
            <tr>
                <td class="action">
                    <form action="{thispage.url}" method="post">
                        <input type="hidden" name="action" value="confirmdelete">
                        <input type="hidden" name="user" value="{user.userId}">
                        <input type="submit" value="Delete">
                    </form>
                </td>
                <td>
                    <form action="{thispage.url}" method="post">
                        <input type="hidden" name="action" value="canceldelete">
                        <input type="submit" value="Cancel">
                    </form>
                </td>
            </tr>
        </table>
        """
        user = UserDatabase().getUserDetails(userId, externalConn)
        club = "" if user.club is None else user.club
        thisPage = PageLink(self.pageId, self)
        roles = string.join(user.roles, ",")
        answer = html.format(user=user, club=club, thispage=thisPage, roles=roles)
        return answer