'''
Created on 12 Aug 2013

@author: hicksj
'''
from pages.page import Page
from pages.pageLink import PageLink
from userdb.userdb import UserDatabase, UserException
import string
from pages.redirect import RedirectException

class LoginValidation:

    def __init__(self):
        self.valid = True
        self.email = ""
        self.password = ""
        self.emailMessage = ""
        self.passwordMessage = ""

class UserLogin(Page):
    
    msgKeyNoLogin = "nologin"
    msgKeyNoAuth = "noAuth"
    messages = {}
    messages[msgKeyNoLogin] = "You must be logged in to view the requested page."
    messages[msgKeyNoAuth] = "You do not have the necessary authority ('{role}') to view the requested page."
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.userDb = UserDatabase()

    def getTitle(self):
        answer = "SEHICL User Login"
        return answer
    
    def getContent(self):
        if (self.allParams.get("displayed", None) == "true"):
            processingOutcome = self.processLoginData()
            if processingOutcome.valid:
                if processingOutcome.token is not None:
                    self.allParams["session"] = processingOutcome.token
                    pageLink = PageLink(self.allParams["forward"], self) 
                    raise RedirectException(pageLink)
                else:
                    answer = self.getLoginPage(processingOutcome)
            else:
                answer = self.getLoginPage(processingOutcome)
        else:
            answer = self.getLoginPage()
        return answer

    def getLoginPage(self, validation=LoginValidation()):
        html = """
        <h1>Login</h1>
        {message}
        <p>
            If you do not have a login, <a href="{register.url}">register here</a>.<br>
            Please note that if you registered for a login during the 2012-13 season, that login
            no longer works and you must re-register.
        </p>
        <p>
            If you have already registered, please fill in the fields below and press "Login".
            If you cannot remember your password, fill in the e-mail address and press 
            "Remind"; if the e-mail address you specify is that of a registered user, a password
            reminder will be sent to that address.
        </p>
        <form action="{submit.url}" method="post">
            <input type="hidden" name="displayed" value="true">
            <table>
                <tr>
                    <td>E-mail address</td>
                    <td><input type="text" name="email" value="{valid.email}"></td>
                    <td>{valid.emailMessage}</td>
                </tr>
                <tr>
                    <td>Password</td>
                    <td><input type="password" name="password" value="{valid.password}"></td>
                    <td>{valid.passwordMessage}</td>
                </tr>
            </table>
            <p>
                <input name="button" type="Submit" value="Login">
                <input name="button" type="Submit" value="Remind">
            </p>
        </form>
        """
        params = {}
        for k, v in self.allParams.items():
            if k in ("message", "role", "forward"):
                params[k] = v
        submitLink = PageLink("login", self, params)
        registerLink = PageLink("register", self)
        msgKey = self.allParams.get("message", None)
        msgTemplate = self.messages.get(msgKey, "")
        message = msgTemplate.format(role=self.allParams.get("role", None))
        answer = html.format(submit=submitLink, valid=validation, message=message, register=registerLink)
        return answer

    def processLoginData(self):
        answer = LoginValidation()
        buttonPressed = self.allParams.get("button", "") 
        answer.email = string.strip(self.allParams.get("email", ""))
        if answer.email == "":
            answer.valid = False
            answer.emailMessage = "Please specify your e-mail address."
        if buttonPressed != "Remind":
            answer.password = string.strip(self.allParams.get("password", ""))
            if answer.password == "":
                answer.valid = False
                answer.passwordMessage = "Please specify your password."
        if answer.valid:
            try:
                if buttonPressed == "Remind":
                    self.userDb.remindOfPassword(answer.email)
                    answer.token = None
                    answer.emailMessage = "A password reminder has been sent to this address."
                else:
                    answer.token = self.userDb.login(answer.email, answer.password)
            except UserException as ex:
                answer.valid = False
                answer.emailMessage = ex.message
        return answer
    
class RegistrationValidation:

    def __init__(self):
        self.valid = True
        self.name = ""
        self.club = ""
        self.email = ""
        self.password = ""
        self.passwordconf = ""
        self.nameMessage = ""
        self.clubMessage = ""
        self.emailMessage = ""
        self.passwordMessage = ""
        self.passwordconfMessage = ""

class UserRegistration(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.userDb = UserDatabase()

    def getTitle(self):
        answer = "SEHICL User Registration"
        return answer
    
    def getContent(self):
        if (self.allParams.get("displayed", None) == "true"):
            processingOutcome = self.processRegistrationData()
            if processingOutcome.valid:
                answer = self.getRegistrationConfirmationPage()
            else:
                answer = self.getRegistrationPage(processingOutcome)
        else:
            answer = self.getRegistrationPage()
        return answer

    def getRegistrationPage(self, validation=RegistrationValidation()):
        html = """
        <h1>New user registration</h1>
        <p>
        Please fill in the fields below and press "Submit". All fields marked with "*" must be completed.
        </p>
        <form action="{submit.url}" method="post">
            <input type="hidden" name="displayed" value="true">
            <input type="hidden" name="forward" value="{forward}">
            <table>
                <tr>
                    <td>Name</td>
                    <td>*</td>
                    <td><input type="text" name="name" value="{valid.name}"></td>
                    <td>{valid.nameMessage}</td>
                </tr>
                <tr>
                    <td>Club</td>
                    <td></td>
                    <td><input type="text" name="club" value="{club}"></td>
                    <td>{valid.clubMessage}</td>
                </tr>
                <tr>
                    <td>E-mail address</td>
                    <td>*</td>
                    <td><input type="text" name="email" value="{valid.email}"></td>
                    <td>{valid.emailMessage}</td>
                </tr>
                <tr>
                    <td>Password</td>
                    <td>*</td>
                    <td><input type="password" name="password""></td>
                    <td>{valid.passwordMessage}</td>
                </tr>
                <tr>
                    <td>Confirm password</td>
                    <td>*</td>
                    <td><input type="password" name="passwordconf""></td>
                    <td>{valid.passwordconfMessage}</td>
                </tr>
            </table>
            <p>
            By clicking the "Submit" button below, you agree that:
            <ul>
                <li>
                    We may store the information
                    you have supplied on a computer system, and we may use it only for the purpose
                    of administering your rights as a registered user of this site. We will never give
                    your details to any other party.
                </li>
                <li>
                    You will treat all information to which your login gives you access with appropriate
                    care and respect. In particular, where that information comprises other people's personal
                    details, you may use it only for legitimate purposes connected with the League,
                    unless you first gain the explicit consent of the person or persons concerned.
                </li>
            </ul>
            </p>
            <p>
                <input type="Submit" value="Submit">
            </p>
        </form>
        """
        submitLink = PageLink("register", self)
        club = "" if validation.club is None else validation.club
        forward = self.allParams.get("forward", PageLink(None, self).url)
        answer = html.format(submit=submitLink, valid=validation, forward=forward, club=club)
        return answer
    
    def processRegistrationData(self):
        answer = RegistrationValidation()
        answer.name = string.strip(self.allParams.get("name", ""))
        if answer.name == "":
            answer.valid = False
            answer.nameMessage = "Please specify your name."
        club = self.allParams.get("club", None)
        if club is not None:
            club = string.strip(club)
            if club == "":
                club = None
        answer.club = club  
        answer.email = string.strip(self.allParams.get("email", ""))
        if answer.email == "":
            answer.valid = False
            answer.emailMessage = "Please specify your e-mail address."
        answer.password = string.strip(self.allParams.get("password", ""))
        if answer.password == "":
            answer.valid = False
            answer.passwordMessage = "Please specify your password."
        answer.passwordconf = string.strip(self.allParams.get("passwordconf", ""))
        if answer.passwordconf == "":
            answer.valid = False
            answer.passwordconfMessage = "Please confirm your password."
        elif answer.passwordconf != answer.password:
            answer.valid = False
            answer.passwordconfMessage = "Password and Confirm password must be the same."
        if answer.valid:
            try:
                self.userDb.registerUser(answer.email, answer.name, answer.club, answer.password)
            except UserException as ex:
                answer.valid = False
                answer.emailMessage = ex.message
        return answer
    
    def getRegistrationConfirmationPage(self):
        html = """
        <h1>Registration successful</h1>
        <p>Thank you for registering. Your account has been set up, but needs to be activated.</p>
        <p>An e-mail has been sent to {email}. It contains a link, which you need to click in order to 
        activate the account. Once you have done this the account will be active and you will be able to
        log in.</p>
        """
        answer = html.format(email=self.allParams["email"])
        return answer
    
class UserActivation(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.userDb = UserDatabase()

    def getTitle(self):
        answer = "SEHICL User Activation"
        return answer
    
    def getContent(self):
        answer = self.getActivationPage()
        return answer

    def getActivationPage(self):
        html = """
        <h1>Activation successful</h1>
        <p>You have successfully activated the following account:</p>
        <ul>
            <li>Name: {user.name}</li>
            <li>E-mail: {user.email}</li>
            <li>Club: {user.club}</li>
        </ul>
        """
        userId = self.allParams.get("user")
        try:
            userDetails = self.userDb.activateUser(userId)
            answer = html.format(user=userDetails)
        except UserException:
            answer = """
            <h1>Activation failed</h1>
            <p>No user was found with the specified identity.</p>
            """
        return answer
