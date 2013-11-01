'''
Created on 3 Sep 2013

@author: hicksj
'''
from pages.page import Page
from xml.etree import ElementTree
import re
import string
from pages.pageLink import HtmlLink, PageLink
from pages.mailto import Mailto
from pages import mailto
from pages.settings import Settings

class PersonData:
    def __init__(self, name=None, address=None, phoneNumbers=[], roles=[]):
        self.name = name
        self.address = address
        self.phoneNumbers = phoneNumbers
        self.roles = roles

class RoleData:
    def __init__(self, name=None, email=None, club=None):
        self.name = name
        self.email = email
        self.club = club

class Contacts(Page):

    sourceFile = "{0}/contacts.xml".format(Settings.dataDirectory)
    
    def __init__(self, pageId, full, params={}, role=None):
        Page.__init__(self, pageId, params, role)
        self.full = full
        
    def getTitle(self):
        return "SEHICL Contacts"
        
    def getContactData(self, rootElement=None):
        answer = []
        if rootElement is None:
            rootElement = ElementTree.parse(self.sourceFile)
        for personElement in rootElement.findall("person"):
            answer.append(self.getPersonData(personElement))
        return answer
    
    def getPersonData(self, personElement):
        answer = PersonData()
        self.getName(personElement, answer)
        self.getRoles(personElement, answer)
        if self.full:
            self.getPhoneNumbers(personElement, answer)
            self.getAddress(personElement, answer)
        return answer

    def getName(self, personElement, dataObject):
        nameElement = personElement.find("name")
        dataObject.name = None if nameElement is None else nameElement.text.strip()
            
    def getAddress(self, personElement, dataObject):
        addressElement = personElement.find("address")
        dataObject.address = None if addressElement is None else addressElement.text.strip()
            
    def getPhoneNumbers(self, personElement, dataObject):
        phoneNumbers = []
        for phoneElement in personElement.findall("phone"):
            phoneNo = self.formatPhoneNumber(phoneElement.text.strip())
            phoneNumbers.append(phoneNo)
        dataObject.phoneNumbers = phoneNumbers
        
    def formatPhoneNumber(self, phoneNumber):
        digits = re.sub("[^0-9]", "", phoneNumber)
        groups = None
        if digits[0] == '0':
            length = len(digits)
            if digits[1] == "2":
                if length == 11:
                    groups = [3, 4, 4]
            elif digits[1] == "1":
                if digits[2] == "1" or digits[3] == "1":
                    if length == 11:
                        groups = [4, 3, 4]
                else:
                    if length in range(9, 12):
                        groups = [5, length - 5]
            else:
                if length == 11:
                    groups = [5, 6]
        if groups is None:
            answer = "???{0}".format(digits)
        else:
            groupedDigits = []
            start = 0
            for g in groups:
                end = start + g
                groupedDigits.append(digits[start:end])
                start = end
            answer = string.join(groupedDigits, " ")
        return answer
            
    def getRoles(self, personElement, dataObject):
        roles = []
        for roleElement in personElement.findall("role"):
            role = self.getRole(roleElement)
            roles.append(role)
        dataObject.roles = roles
        
    def getRole(self, roleElement):
        answer = RoleData()
        self.getRoleName(roleElement, answer)
        self.getClub(roleElement, answer)
        self.getEmail(roleElement, answer)
        return answer

    def getRoleName(self, roleElement, dataObject):
        name = roleElement.get("name", None)
        dataObject.name = None if name is None else name.strip()

    def getClub(self, roleElement, dataObject):
        club = roleElement.get("club", None)
        dataObject.club = None if club is None else club.strip()

    def getEmail(self, roleElement, dataObject):
        emailElement = roleElement.find("email")
        address = None if emailElement is None else emailElement.get("id", None)
        dataObject.email = None if address is None else address.strip()
        
    def getContent(self, rootElement=None):
        html = """
        <div id="contacts">
        <h1>Contacts</h1>
        <p>
            <a href="#committee">Committee</a> | <a href="#club">Club secretaries</a>
        </p>
        {headermessages}
        <h2><a id="committee">Committee</a></h2>
        {committee}
        {committeemessages}
        <h2><a id="club">Clubs</a></h2>
        {clubs}
        </div>
        """
        personList = self.getContactData(rootElement)
        headerMessages = self.getHeaderMessages()
        committee = self.getCommitteeContacts(personList)
        committeeMessages = self.getCommitteeMessages();
        clubs = self.getClubContacts(personList)
        answer = html.format(headermessages=headerMessages, committee=committee, committeemessages=committeeMessages, clubs=clubs)
        return answer

    def getHeaderMessages(self):
        html = """
        <p>
            {gsm.atag}Game Set &amp; Match</a>, the
            League's sponsors, are located at Unit 1, Beaver Trade Park, Quarry Lane, Chichester PO19 8NY
            (tel: 01243 538800).
        </p>
        <p>
            The main means of communication on league matters is by e-mail. For
            urgent contacts, however, it may be preferable to telephone; telephone
            numbers for committee members, club secretaries and team captains and
            managers are given {phonelocation}.
        </p>
        <p>
            All e-mail contacts should be made using the e-mail addresses
            assigned to the relevant roles in the League's domain (that is,
            addresses ending with <i>sehicl.org.uk</i>). This ensures that when the
            person performing a role changes, the e-mail is still routed to the correct
            person. The easiest way to do this is to click on the person's name in
            the lists below.
        </p>
        <p>
            Please let {webmaster.html} know if any of the information below is incomplete or incorrect.
        </p>
        """
        if self.full:
            phoneLocation = "below"
        else:
            fullContacts = PageLink("fullContacts", self)
            phoneLocation = "on the <a href=\"{fullcontacts.url}\">Full Contacts</a> page".format(fullcontacts=fullContacts)
        gsm = HtmlLink("http://www.gsam.co.uk/")
        webmaster = Mailto("website", "the Webmaster", description="SEHICL Webmaster")
        answer = html.format(gsm=gsm, webmaster=webmaster, phonelocation=phoneLocation)
        return answer
    
    def getCommitteeMessages(self):
        html = """
        <p>
            General contacts should be addressed to {contacts.html}.
        </p>
        <p>
            Non-member clubs who wish to enter one or more teams in the League
            are asked to contact {secretary.html} in the first instance.
        </p>
        <p>
            Result sheets may be sent electronically to {fixturesec.html},
            using one of the template documents available on the <a href="{resources.url}">Resources</a> page.
        </p>
        """
        contacts = Mailto("contacts", "")
        secretary = Mailto("secretary", "the Secretary", description="SEHICL Secretary")
        fixturesec = Mailto("fixturesec", "the Fixture Secretary", description="SEHICL Fixture Secretary")
        resources = PageLink("resources", self)
        answer = html.format(contacts=contacts, secretary=secretary, fixturesec=fixturesec, resources=resources)
        return answer
    
    def getCommitteeContacts(self, personList):
        html = """
        <table>
            <tbody>
                {contacts}
            </tbody>
        </table>
        """
        contacts = []
        contactsByRole = {}
        for p in personList:
            for r in p.roles:
                if r.club is None:
                    contactsByRole[r.name.lower()] = (p, r)
        roles = ("President", "Chairman", "Vice-Chairman", "Secretary", "Treasurer", "Umpires' Co-ordinator", "Fixture Secretary", "Webmaster")
        for rn in roles:
            person, role = contactsByRole.get(rn.lower(), (None, None))
            contacts.append(self.getCommitteeContactHtml(rn, person, role, "Currently vacant"))
        answer = html.format(contacts=string.join(contacts, "\n"))
        return answer
    
    def getClubContacts(self, personList):
        contactsByClubAndRole = {}
        for p in personList:
            for r in p.roles:
                if r.club is not None:
                    club = r.club
                    contactsByRole = contactsByClubAndRole.get(club, {})
                    if contactsByRole == {}:
                        contactsByClubAndRole[club] = contactsByRole
                    roleName = r.name
                    contactsForRole = contactsByRole.get(roleName, [])
                    if contactsForRole == []:
                        contactsByRole[roleName] = contactsForRole
                    contactsForRole.append((p, r))
        answer = self.getAllClubsContactsHtml(contactsByClubAndRole)
        return answer
    
    def getCommitteeContactHtml(self, roleName, person, role, defaultText):
        html = """
        <tr>
            <td class="role">{role}</td>
            <td>{person}</td>
        </tr>
        """
        email = None if role is None else role.email
        answer = html.format(role=roleName, person=self.getPersonHtml(person, email, defaultText, True))
        return answer
    
    def getPersonHtml(self, person, email, defaultText, includeAddress):
        if person is None:
            answer = defaultText
        else:
            htmlItems = []
            if email is None:
                htmlItems.append(person.name)
            else:
                mailto = Mailto(email, person.name)
                htmlItems.append(mailto.html)
            addressPresent = False
            if self.full:
                addressPresent = includeAddress and person.address is not None
                if addressPresent:
                    htmlItems.append(person.address)
                if len(person.phoneNumbers) > 0:
                    htmlItems.append(string.join(person.phoneNumbers, " / "))
            answer = string.join(htmlItems, "<br>\n" if addressPresent else ",\n")
        return answer
                    
    def getAllClubsContactsHtml(self, contactsByClubAndRole):
        html = """
        <table>
            <tbody>
                {contacts}
            </tbody>
        </table>
        """
        sortableClubNames = {}
        for name in contactsByClubAndRole.keys():
            k = re.sub("[^a-z]", "", name.lower())
            sortableClubNames[k] = name
        contacts = []
        for k in sorted(sortableClubNames.keys()):
            name = sortableClubNames[k]
            contacts.append(self.getClubContactsHtml(name, contactsByClubAndRole[name]))
        answer = html.format(contacts=string.join(contacts, "\n"))
        return answer

    def getClubContactsHtml(self, clubName, contactsByRole):
        html = """
        <tr>
            <td class="role">{club}</td>
            <td>
                {contacts}
            </td>
        </tr>
        """
        answer = html.format(club=clubName, contacts=self.getClubContactListHtml(contactsByRole))
        return answer
    
class PartialContacts(Contacts):

    def __init__(self, pageId, params={}, role=None):
        Contacts.__init__(self, pageId, False, params, role)

    def getClubContactListHtml(self, contactsByRole):
        person, role = contactsByRole.get("Secretary", [(None, None)])[0]
        email = None if role is None else role.email
        answer = self.getPersonHtml(person, email, "TBC", False)
        return answer

class FullContacts(Contacts):

    def __init__(self, pageId, params={}, role=None):
        Contacts.__init__(self, pageId, True, params, role)

    def getClubContactListHtml(self, contactsByRole):
        roleOrder = ["secretary", "captain", "senior", "a team", "b team", "c team", "under-16", "under-13"]
        rolesByOrder = {}
        for k in contactsByRole.keys():
            order = roleOrder.index(k.lower())
            rolesByOrder[order] = k
        contacts = []
        for k in sorted(rolesByOrder.keys()):
            roleName = rolesByOrder[k]
            contactsForRole = contactsByRole[roleName]
            peopleData = [self.getPersonHtml(person, role.email, "TBC", roleName == "Secretary") for person, role in contactsForRole]
            contacts.append("{0}: {1}".format(roleName, string.join(peopleData, "; ")))
        answer = string.join(contacts, "<br>\n")
        return answer
  
    