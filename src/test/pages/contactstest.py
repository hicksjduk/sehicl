'''
Created on 17 Sep 2013

@author: hicksj
'''
import unittest
from pages.contacts import FullContacts, PartialContacts, PersonData, RoleData
from xml.etree import ElementTree
from test.testbase import TestBase


class Test(TestBase):


    def testFormatPhoneNumberInvalidCharacters(self):
        value = "1252asfd67s65sfd"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???12526765"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberInvalidLength(self):
        value = "012141"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???012141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberNotStartingWith0(self):
        value = "112 141 41414"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???11214141414"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith02TooFewDigits(self):
        value = "022 141 4141"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???0221414141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith02TooManyDigits(self):
        value = "0221 41 141444"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???022141141444"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith02CorrectNumberOfDigits(self):
        value = "0221 41 14 14 4"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "022 1411 4144"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith011TooFewDigits(self):
        value = "011 141 4141"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???0111414141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith011TooManyDigits(self):
        value = "0111 41 141444"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???011141141444"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith011CorrectNumberOfDigits(self):
        value = "0111 41 14 14 4"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "0111 411 4144"
        self.assertEquals(expectedResult, result)
        
    def testFormatPhoneNumberStartingWith0x1TooFewDigits(self):
        value = "016 141 4141"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???0161414141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith0x1TooManyDigits(self):
        value = "0131 41 141444"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???013141141444"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith0x1CorrectNumberOfDigits(self):
        value = "0191 41 14 14 4"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "0191 411 4144"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith01xxTooFewDigits(self):
        value = "016 241 41"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???01624141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith01xxTooManyDigits(self):
        value = "0132 41 141444"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???013241141444"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith01xx9Digits(self):
        value = "0193 41 14 1"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "01934 1141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith01xx10Digits(self):
        value = "0193 41 14 11"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "01934 11411"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith01xx11Digits(self):
        value = "0193 41 14 119"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "01934 114119"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith07TooFewDigits(self):
        value = "072 141 4141"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???0721414141"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith07TooManyDigits(self):
        value = "0721 41 141444"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "???072141141444"
        self.assertEquals(expectedResult, result)

    def testFormatPhoneNumberStartingWith07CorrectNumberOfDigits(self):
        value = "0721 41 14 14 4"
        result = PartialContacts("").formatPhoneNumber(value)
        expectedResult = "07214 114144"
        self.assertEquals(expectedResult, result)
        
    def testGetNameNoNameSpecified(self):
        xml = """
        <person/>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getName(personElement, dataObject)
        expectedResult = None
        self.assertEquals(expectedResult, dataObject.name)

    def testGetNameNameSpecified(self):
        xml = """
        <person>
            <name>    Jeremy Hicks   </name>
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getName(personElement, dataObject)
        expectedResult = "Jeremy Hicks"
        self.assertEquals(expectedResult, dataObject.name)

    def testGetAddressNoAddressSpecified(self):
        xml = """
        <person/>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getAddress(personElement, dataObject)
        expectedResult = None
        self.assertEquals(expectedResult, dataObject.address)

    def testGetAddressAddressSpecified(self):
        xml = """
        <person>
            <address> Four Stoneycroft Rise              </address>
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getAddress(personElement, dataObject)
        expectedResult = "Four Stoneycroft Rise"
        self.assertEquals(expectedResult, dataObject.address)

    def testGetPhoneNumbersNoNumbersSpecified(self):
        xml = """
        <person>
            <address> Four Stoneycroft Rise              </address>
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getPhoneNumbers(personElement, dataObject)
        expectedResult = []
        self.assertEquals(expectedResult, dataObject.phoneNumbers)

    def testGetPhoneNumbersSomeNumbersSpecified(self):
        xml = """
        <person>
            <phone> 07423152361  </phone>
            <phone>02392 563323</phone>
            <phone>0193 282 2282</phone>
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getPhoneNumbers(personElement, dataObject)
        expectedResult = ["07423 152361", "023 9256 3323", "01932 822282"]
        self.assertEquals(expectedResult, dataObject.phoneNumbers)
        
    def testGetRoleNameNameNotSpecified(self):
        xml = """
        <role/>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getRoleName(roleElement, dataObject)
        expectedResult = None
        self.assertEquals(expectedResult, dataObject.name)
        
    def testGetRoleNameNameSpecified(self):
        xml = """
        <role name=" sad sagsdgsa     "/>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getRoleName(roleElement, dataObject)
        expectedResult = "sad sagsdgsa"
        self.assertEquals(expectedResult, dataObject.name)
        
    def testGetClubClubNotSpecified(self):
        xml = """
        <role/>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getClub(roleElement, dataObject)
        expectedResult = None
        self.assertEquals(expectedResult, dataObject.club)
        
    def testGetClubClubSpecified(self):
        xml = """
        <role club="       OPCS    "/>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getClub(roleElement, dataObject)
        expectedResult = "OPCS"
        self.assertEquals(expectedResult, dataObject.club)
        
    def testGetEmailElementNotSpecified(self):
        xml = """
        <role club="       OPCS    "/>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getEmail(roleElement, dataObject)
        expectedResult = None
        self.assertEquals(expectedResult, dataObject.email)
        
    def testGetEmailElementSpecifiedIDNotSpecified(self):
        xml = """
        <role club="       OPCS    ">
            <email/>
        </role>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getEmail(roleElement, dataObject)
        expectedResult = None
        self.assertEquals(expectedResult, dataObject.email)
        
    def testGetEmailElementSpecifiedIDSpecified(self):
        xml = """
        <role club="       OPCS    ">
            <email id="            jeremy  "/>
        </role>
        """
        roleElement = ElementTree.fromstring(xml)
        dataObject = RoleData()
        PartialContacts("").getEmail(roleElement, dataObject)
        expectedResult = "jeremy"
        self.assertEquals(expectedResult, dataObject.email)
        
    def testGetRole(self):
        xml = """
        <role name="Secretary" club="Corinthians">
            <email id="corinthians.secretary" />
        </role>
        """
        roleElement = ElementTree.fromstring(xml)
        result = PartialContacts("").getRole(roleElement)
        self.assertEquals("Secretary", result.name)
        self.assertEquals("Corinthians", result.club)
        self.assertEquals("corinthians.secretary", result.email)
        
    def testGetRoles(self):
        xml = """
        <person>
        <role name="Chairman">
            <email id="chairman" />
        </role>
        <role name="Secretary" club="Denmead">
            <email id="denmead.secretary" />
        </role>
        <role name="Captain" club="Denmead" />
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        dataObject = PersonData()
        PartialContacts("").getRoles(personElement, dataObject)
        expectedResults = []
        expectedResults.append(("Chairman", None, "chairman"))
        expectedResults.append(("Secretary", "Denmead", "denmead.secretary"))
        expectedResults.append(("Captain", "Denmead", None))
        for expected, result in zip(expectedResults, dataObject.roles):
            expName, expClub, expEmail = expected
            self.assertEquals(expName, result.name)
            self.assertEquals(expClub, result.club)
            self.assertEquals(expEmail, result.email)
        self.assertEquals(len(expectedResults), len(dataObject.roles))

    def testGetPersonDataNotFullData(self):
        xml = """
        <person>
            <name>Rick Marston</name>
            <address>113 Festing Grove, Portsmouth PO4 9QE</address>
            <phone>023 9273 5987</phone>
            <phone>07724 138531</phone>
            <role name="Secretary" club="Portsmouth">
                <email id="portsmouth.secretary" />
            </role>
            <role name="B team" club="Portsmouth" />
            <role name="C team" club="Portsmouth" />
            <role name="Under-16" club="Portsmouth" />
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        result = PartialContacts("").getPersonData(personElement)
        self.assertEquals("Rick Marston", result.name)
        self.assertEquals(4, len(result.roles))
        self.assertEquals(None, result.address)
        self.assertEquals([], result.phoneNumbers)
        
    def testGetPersonDataFullData(self):
        xml = """
        <person>
            <name>Rick Marston</name>
            <address>113 Festing Grove, Portsmouth PO4 9QE</address>
            <phone>023 9273 5987</phone>
            <phone>07724 138531</phone>
            <role name="Secretary" club="Portsmouth">
                <email id="portsmouth.secretary" />
            </role>
            <role name="B team" club="Portsmouth" />
            <role name="C team" club="Portsmouth" />
            <role name="Under-16" club="Portsmouth" />
        </person>
        """
        personElement = ElementTree.fromstring(xml)
        result = FullContacts("").getPersonData(personElement)
        self.assertEquals("Rick Marston", result.name)
        self.assertEquals(4, len(result.roles))
        self.assertEquals("113 Festing Grove, Portsmouth PO4 9QE", result.address)
        self.assertEquals(["023 9273 5987", "07724 138531"], result.phoneNumbers)
        
    def testGetContactData(self):
        xml = """
        <contacts>
            <person>
                <name>Barry Plumb</name>
                <address>Pine Corner, 7A Anthill Close, Denmead PO7 6ND</address>
                <phone>07738 005543</phone>
                <role name="Treasurer">
                    <email id="treasurer" />
                </role>
            </person>

            <person>
                <name>Matt Reeves</name>
                <phone>07807 045580</phone>
                <role name="A team" club="Sarisbury Athletic" />
            </person>

            <person>
                <name>Andy Reynolds</name>
                <phone>07748 844609</phone>
                <role name="Under-13" club="Waterlooville" />
            </person>

            <person>
                <name>Steve Roberts</name>
                <address>192a Locks Road, Locks Heath SO31 6LE</address>
                <phone>01489 581477</phone>
                <phone>07918 671878</phone>
                <role name="Secretary" club="Sarisbury Athletic">
                    <email id="sarisbury.secretary" />
                </role>
            </person>
        </contacts>
        """
        rootElement = ElementTree.fromstring(xml)
        result = FullContacts("").getContactData(rootElement)
        expectedNames = ["Barry Plumb", "Matt Reeves", "Andy Reynolds", "Steve Roberts"]
        for e, a in zip(expectedNames, result):
            self.assertEquals(e, a.name)
        self.assertEquals(len(expectedNames), len(result))
        
    def testGetHeaderMessagesFullContacts(self):
        result = FullContacts("").getHeaderMessages()
        expectedResult = """
        <p>
            <a href="http://www.gsam.co.uk/" target="_blank">Game Set &amp; Match</a>, the
            League's sponsors, are located at Unit 1, Beaver Trade Park, Quarry Lane, Chichester PO19 8NY
            (tel: 01243 538800).
        </p>
        <p>
            The main means of communication on league matters is by e-mail. For
            urgent contacts, however, it may be preferable to telephone; telephone
            numbers for committee members, club secretaries and team captains and
            managers are given below.
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
            Please let <script language="javascript">
                document.write(mailTo("website", "", "SEHICL Webmaster", "the Webmaster"));
            </script>
            <noscript>the Webmaster<i> (Javascript not enabled: cannot display mail link)</i>
            </noscript> know if any of the information below is incomplete or incorrect.
        </p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetHeaderMessagesPartialContacts(self):
        result = PartialContacts("").getHeaderMessages()
        expectedResult = """
        <p>
            <a href="http://www.gsam.co.uk/" target="_blank">Game Set &amp; Match</a>, the
            League's sponsors, are located at Unit 1, Beaver Trade Park, Quarry Lane, Chichester PO19 8NY
            (tel: 01243 538800).
        </p>
        <p>
            The main means of communication on league matters is by e-mail. For
            urgent contacts, however, it may be preferable to telephone; telephone
            numbers for committee members, club secretaries and team captains and
            managers are given on the <a href="/cgi-bin/page.py?id=fullContacts">Full Contacts</a> page.
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
            Please let <script language="javascript">
                document.write(mailTo("website", "", "SEHICL Webmaster", "the Webmaster"));
            </script>
            <noscript>the Webmaster<i> (Javascript not enabled: cannot display mail link)</i>
            </noscript> know if any of the information below is incomplete or incorrect.
        </p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonNotSpecified(self):
        person = None
        email = None
        defaultText = "Hello goodbye"
        result = PartialContacts("").getPersonHtml(person, email, defaultText, False)
        expectedResult = "Hello goodbye"
        self.assertEquals(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedNotFull(self):
        person = PersonData(name="Pandolf Ironhead")
        email = None
        defaultText = "Hello goodbye"
        result = PartialContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = "Pandolf Ironhead"
        self.assertEquals(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedNotFull(self):
        person = PersonData(name="Pandolf Ironhead")
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = PartialContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedFullNoAddressNoPhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead")
        email = None
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = "Pandolf Ironhead"
        self.assertEquals(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedFullNoAddressNoPhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead")
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedFullAddressNoPhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead", address="Schloss Eisenkopf")
        email = None
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        Pandolf Ironhead<br>
        Schloss Eisenkopf
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedFullAddressNoPhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead", address="Schloss Eisenkopf")
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript><br>
        Schloss Eisenkopf
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedFullNoAddressOnePhoneNumber(self):
        person = PersonData(name="Pandolf Ironhead", phoneNumbers=["01329312895"])
        email = None
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        Pandolf Ironhead,
        01329312895
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedFullNoAddressOnePhoneNumber(self):
        person = PersonData(name="Pandolf Ironhead", phoneNumbers=["01329312895"])
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>,
        01329312895
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedFullAddressOnePhoneNumber(self):
        person = PersonData(name="Pandolf Ironhead", address="Schloss Eisenkopf", phoneNumbers=["01329312895"])
        email = None
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        Pandolf Ironhead<br>
        Schloss Eisenkopf<br>
        01329312895
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedFullAddressOnePhoneNumber(self):
        person = PersonData(name="Pandolf Ironhead", address="Schloss Eisenkopf", phoneNumbers=["01329312895"])
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript><br>
        Schloss Eisenkopf<br>
        01329312895
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedFullNoAddressMultiplePhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead", phoneNumbers=["01329312895", "07878727131"])
        email = None
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        Pandolf Ironhead, 
        01329312895 / 07878727131
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedFullNoAddressMultiplePhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead", phoneNumbers=["01329312895", "07878727131"])
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>,
        01329312895 / 07878727131
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailNotSpecifiedFullAddressMultiplePhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead", address="Schloss Eisenkopf", phoneNumbers=["01329312895", "07878727131"])
        email = None
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        Pandolf Ironhead<br>
        Schloss Eisenkopf<br>
        01329312895 / 07878727131
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPersonHtmlPersonSpecifiedEmailSpecifiedFullAddressMultiplePhoneNumbers(self):
        person = PersonData(name="Pandolf Ironhead", address="Schloss Eisenkopf", phoneNumbers=["01329312895", "07878727131"])
        email = "pandolf"
        defaultText = "Hello goodbye"
        result = FullContacts("").getPersonHtml(person, email, defaultText, True)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("pandolf", "", "", "Pandolf Ironhead"));
        </script>
        <noscript>Pandolf Ironhead<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript><br>
        Schloss Eisenkopf<br>
        01329312895 / 07878727131
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetCommitteeContactHtmlNoPersonForRole(self):
        roleName = "Treasurer"
        person = None
        role = None
        defaultText = "Not filled at the moment"
        result = PartialContacts("").getCommitteeContactHtml(roleName, person, role, defaultText)
        expectedResult = """
        <tr>
            <td class="role">Treasurer</td>
            <td>Not filled at the moment</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetCommitteeContactHtmlPersonForRoleNoEmail(self):
        roleName = "Manager"
        person = PersonData(name="Steve Evans")
        role = RoleData()
        defaultText = "Not filled at the moment"
        result = PartialContacts("").getCommitteeContactHtml(roleName, person, role, defaultText)
        expectedResult = """
        <tr>
            <td class="role">Manager</td>
            <td>Steve Evans</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetCommitteeContactHtmlPersonForRoleWithEmail(self):
        roleName = "Manager"
        person = PersonData(name="Steve Evans")
        role = RoleData(email="rufcmgr")
        defaultText = "Not filled at the moment"
        result = PartialContacts("").getCommitteeContactHtml(roleName, person, role, defaultText)
        expectedResult = """
        <tr>
            <td class="role">Manager</td>
            <td><script language="javascript">
            document.write(mailTo("rufcmgr", "", "", "Steve Evans"));
        </script>
        <noscript>Steve Evans<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetCommitteeContactsNoRolesFilled(self):
        personList = []
        result = PartialContacts("").getCommitteeContacts(personList)
        expectedResult = """
        <table>
            <tbody>
                <tr>
                    <td class="role">President</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Chairman</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Vice-Chairman</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Secretary</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Treasurer</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Umpires' Co-ordinator</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Fixture Secretary</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Webmaster</td>
                    <td>Currently vacant</td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetCommitteeContactsSomeRolesFilled(self):
        personList = []
        personList.append(PersonData(name="Richard Matthews", \
                                     roles=[RoleData(name="Chairman", email="chairman"), \
                                            RoleData(name="Secretary", club="Denmead", email="denmead.secretary")]))
        personList.append(PersonData(name="Jeremy Hicks", \
                                     roles=[RoleData(name="Fixture secretary", email="fixturesec"), \
                                            RoleData(name="Webmaster", email="website")]))
        result = PartialContacts("").getCommitteeContacts(personList)
        expectedResult = """
        <table>
            <tbody>
                <tr>
                    <td class="role">President</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Chairman</td>
                    <td><script language="javascript">
            document.write(mailTo("chairman", "", "", "Richard Matthews"));
        </script>
        <noscript>Richard Matthews<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript></td>
                </tr>
                <tr>
                    <td class="role">Vice-Chairman</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Secretary</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Treasurer</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Umpires' Co-ordinator</td>
                    <td>Currently vacant</td>
                </tr>
                <tr>
                    <td class="role">Fixture Secretary</td>
                    <td><script language="javascript">
            document.write(mailTo("fixturesec", "", "", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript></td>
                </tr>
                <tr>
                    <td class="role">Webmaster</td>
                    <td><script language="javascript">
            document.write(mailTo("website", "", "", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript></td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetClubContactListHtmlFull(self):
        contactsByRole = {}
        contactsByRole["Secretary"] = [(PersonData(name="Contact 1", address="Buckingham Palace", phoneNumbers=["0124124"]), RoleData(email="thesecretary"))]
        contactsByRole["Under-16"] = [(PersonData(name="Contact 2", phoneNumbers=["113"]), RoleData())]
        contactsByRole["Captain"] = [(PersonData(name="Contact 3", phoneNumbers=["999"]), RoleData())]
        result = FullContacts("").getClubContactListHtml(contactsByRole)
        expectedResult = """
        Secretary: <script language="javascript">
            document.write(mailTo("thesecretary", "", "", "Contact 1"));
        </script>
        <noscript>Contact 1<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript><br>
        Buckingham Palace<br>
        0124124<br>
        Captain: Contact 3, 
        999<br>
        Under-16: Contact 2, 
        113
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetClubContactListHtmlFullMultipleContactsForRole(self):
        contactsByRole = {}
        contactsByRole["Secretary"] = [(PersonData(name="Contact 1", address="Buckingham Palace", phoneNumbers=["0124124"]), RoleData(email="thesecretary"))]
        contactsByRole["Under-16"] = [(PersonData(name="Contact 2", phoneNumbers=["113"]), RoleData()),\
                                      (PersonData(name="Contact 4", phoneNumbers=["121"]), RoleData())]
        contactsByRole["Captain"] = [(PersonData(name="Contact 3", phoneNumbers=["999"]), RoleData())]
        result = FullContacts("").getClubContactListHtml(contactsByRole)
        expectedResult = """
        Secretary: <script language="javascript">
            document.write(mailTo("thesecretary", "", "", "Contact 1"));
        </script>
        <noscript>Contact 1<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript><br>
        Buckingham Palace<br>
        0124124<br>
        Captain: Contact 3, 
        999<br>
        Under-16: Contact 2, 
        113; Contact 4,
        121
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetClubContactListHtmlNotFullSecretarySpecified(self):
        contactsByRole = {}
        contactsByRole["Secretary"] = [(PersonData(name="Contact 1", address="Buckingham Palace", phoneNumbers=["0124124"]), RoleData(email="thesecretary"))]
        contactsByRole["Under-16"] = [(PersonData(name="Contact 2", phoneNumbers=["113"]), RoleData())]
        contactsByRole["Captain"] = [(PersonData(name="Contact 3", phoneNumbers=["999"]), RoleData())]
        result = PartialContacts("").getClubContactListHtml(contactsByRole)
        expectedResult = """
        <script language="javascript">
            document.write(mailTo("thesecretary", "", "", "Contact 1"));
        </script>
        <noscript>Contact 1<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetClubContactListHtmlNotFullSecretaryNotSpecified(self):
        contactsByRole = {}
        contactsByRole["asdgsdags"] = (PersonData(name="Contact 1", address="Buckingham Palace", phoneNumbers=["0124124"]), RoleData(email="thesecretary"))
        contactsByRole["Under-16"] = (PersonData(name="Contact 2", phoneNumbers=["113"]), RoleData())
        contactsByRole["Captain"] = (PersonData(name="Contact 3", phoneNumbers=["999"]), RoleData())
        result = PartialContacts("").getClubContactListHtml(contactsByRole)
        expectedResult = "TBC"
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetClubContactsHtml(self):
        contactsByRole = {}
        contactsByRole["Secretary"] = [(PersonData(name="Contact 1", address="Buckingham Palace", phoneNumbers=["0124124"]), RoleData(email="thesecretary"))]
        contactsByRole["Under-16"] = [(PersonData(name="Contact 2", phoneNumbers=["113"]), RoleData())]
        contactsByRole["Captain"] = [(PersonData(name="Contact 3", phoneNumbers=["999"]), RoleData())]
        result = FullContacts("").getClubContactsHtml("My Club", contactsByRole)
        expectedResult = """
        <tr>
        <td class="role">My Club</td>
        <td>
        Secretary: <script language="javascript">
            document.write(mailTo("thesecretary", "", "", "Contact 1"));
        </script>
        <noscript>Contact 1<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript><br>
        Buckingham Palace<br>
        0124124<br>
        Captain: Contact 3, 
        999<br>
        Under-16: Contact 2, 
        113
        </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetAllClubsContactHtml(self):
        people = []
        people.append(PersonData(name="Jeremy Hicks", roles=[RoleData(name="Secretary", email="rufc", club="Rotherham")]))
        people.append(PersonData(name="Peter Hicks", roles=[RoleData(name="Secretary", email="pvfc", club="Port Vale")]))
        people.append(PersonData(name="Joe Hicks", roles=[RoleData(name="Secretary", email="pfc", club="Portsmouth")]))
        contactsByClubAndRole = {}
        for p in people:
            role = p.roles[0]
            contactsByClubAndRole[role.club] = {role.name: [(p, p.roles[0])]}
        result = PartialContacts("").getAllClubsContactsHtml(contactsByClubAndRole)
        expectedResult = """
        <table>
            <tbody>
                <tr>
                    <td class="role">Portsmouth</td>
                    <td>
                        <script language="javascript">
            document.write(mailTo("pfc", "", "", "Joe Hicks"));
        </script>
        <noscript>Joe Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>
                    </td>
                </tr>
                <tr>
                    <td class="role">Port Vale</td>
                    <td>
                        <script language="javascript">
            document.write(mailTo("pvfc", "", "", "Peter Hicks"));
        </script>
        <noscript>Peter Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>
                    </td>
                </tr>
                <tr>
                    <td class="role">Rotherham</td>
                    <td>
                        <script language="javascript">
            document.write(mailTo("rufc", "", "", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>
                    </td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetContentPartialContacts(self):
        rootElement = ElementTree.parse("data/contacts.xml")
        PartialContacts("").getContent(rootElement);

    def testGetContentFullContacts(self):
        rootElement = ElementTree.parse("data/contacts.xml")
        FullContacts("").getContent(rootElement)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testFormatPhoneNumberInvalidCharacters']
    unittest.main()