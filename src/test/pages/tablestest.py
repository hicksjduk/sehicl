'''
Created on 8 Aug 2013

@author: hicksj
'''
import unittest
from reports.tablesreport import LeagueTableInReport, TableRow, PointsDeduction,\
    LeagueTableReport
from pages.tables import LeagueTable
import datetime
from test.testbase import TestBase


class Test(TestBase):


    def testGetStatusMessageNoMatchesPlayed(self):
        table = LeagueTableInReport()
        table.lastCompleteMatchDate = None
        result = LeagueTable("").getStatusMessage(table)
        self.assertEquals("", result)

    def testGetStatusMessageAllMatchesPlayed(self):
        table = LeagueTableInReport()
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        table.complete = True
        result = LeagueTable("").getStatusMessage(table)
        expectedResult = """
        <p class="statusMessage">Final table.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetStatusMessageSomeMatchesPlayedNoneToCome(self):
        table = LeagueTableInReport()
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 2, 3)
        result = LeagueTable("").getStatusMessage(table)
        expectedResult = """
        <p class="statusMessage">Includes all games up to and including 3rd March 2013.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetStatusMessageSomeMatchesPlayedOneToCome(self):
        table = LeagueTableInReport()
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 2, 3)
        table.toCome = 1
        result = LeagueTable("").getStatusMessage(table)
        expectedResult = """
        <p class="statusMessage">Date of last game included: 3rd March 2013 (1 result to come).</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetStatusMessageSomeMatchesPlayedMoreThanOneToCome(self):
        table = LeagueTableInReport()
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 2, 3)
        table.toCome = 2
        result = LeagueTable("").getStatusMessage(table)
        expectedResult = """
        <p class="statusMessage">Date of last game included: 3rd March 2013 (2 results to come).</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMarkerClassesNotPromotedNotRelegatedNotChampions(self):
        tableRow = TableRow("", "")
        result = LeagueTable("").getMarkerClasses(tableRow, 5)
        self.assertEquals("", result)
        
    def testGetMarkerClassesPromotedNotRelegatedNotChampions(self):
        tableRow = TableRow("", "")
        tableRow.promoted = True
        result = LeagueTable("").getMarkerClasses(tableRow, 2)
        self.assertEquals("promoted", result)
        
    def testGetMarkerClassesNotPromotedRelegatedNotChampions(self):
        tableRow = TableRow("", "")
        tableRow.relegated = True
        result = LeagueTable("").getMarkerClasses(tableRow, 10)
        self.assertEquals("relegated", result)
        
    def testGetMarkerClassesNotPromotedNotRelegatedChampions(self):
        tableRow = TableRow("", "")
        tableRow.champions = True
        result = LeagueTable("").getMarkerClasses(tableRow, 1)
        self.assertEquals("champions", result)
        
    def testGetMarkerClassesPromotedNotRelegatedChampions(self):
        tableRow = TableRow("", "")
        tableRow.champions = True
        tableRow.promoted = True
        result = LeagueTable("").getMarkerClasses(tableRow, 1)
        self.assertEquals("champions promoted", result)
        
    def testGetDeductionInfoForRowNoDeductions(self):
        tableRow = TableRow("teamId", "teamName")
        deductionReasons = []
        keys, points = LeagueTable("").getDeductionInfoForRow(tableRow, deductionReasons)
        self.assertEquals("", keys)
        self.assertEquals("", points)
        self.assertEquals([], deductionReasons) 

    def testGetDeductionInfoForRowSomeDeductions(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.deductions.append(PointsDeduction(1, "Being rubbish"))
        tableRow.deductions.append(PointsDeduction(3, "Being crap"))
        deductionReasons = ["Being crap - 3 points deducted", "Being appalling - 3 points deducted"]
        keys, points = LeagueTable("").getDeductionInfoForRow(tableRow, deductionReasons)
        self.assertEquals("(1,3)", keys)
        self.assertEquals(4, points)
        self.assertEquals(["Being crap - 3 points deducted", "Being appalling - 3 points deducted", "Being rubbish - 1 point deducted"], deductionReasons) 

    def testGetRowPosition1(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.maintainInvariants()
        result = LeagueTable("").getRow(tableRow, 1, 0, 0, [])
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=teamId">teamName</a>
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">10</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowPositionNot1PointsDifferent(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.maintainInvariants()
        result = LeagueTable("").getRow(tableRow, 1, 0, 0, [])
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=teamId">teamName</a>
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">10</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowPositionNot1PointsDifferentRunRateDifferent(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.maintainInvariants()
        result = LeagueTable("").getRow(tableRow, 2, 100, 9, [])
        expectedResult = """
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=teamId">teamName</a>
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">10</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowPositionNot1PointsDifferentRunRateSame(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.maintainInvariants()
        result = LeagueTable("").getRow(tableRow, 2, 100, 12, [])
        expectedResult = """
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=teamId">teamName</a>
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">10</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowPositionNot1PointsSameRunRateDifferent(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (10, 20)
        tableRow.maintainInvariants()
        result = LeagueTable("").getRow(tableRow, 2, 72, 9, [])
        expectedResult = """
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=teamId">teamName</a>
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">10</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowPositionNot1PointsSameRunRateSame(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (14, 18)
        tableRow.deductions = [PointsDeduction(2, "Being crap")]
        tableRow.maintainInvariants()
        result = LeagueTable("").getRow(tableRow, 2, 72, 12, [])
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=teamId">teamName</a>
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">14</td>
            <td class="bowlpoints number">18</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number">2</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowNoLinks(self):
        tableRow = TableRow("teamId", "teamName")
        tableRow.won, tableRow.lost, tableRow.tied = (1, 3, 5)
        tableRow.runs, tableRow.balls = (100, 50)
        tableRow.batpoints, tableRow.bowlpoints = (14, 18)
        tableRow.deductions = [PointsDeduction(2, "Being crap")]
        tableRow.maintainInvariants()
        table = LeagueTable("")
        table.allParams["archive"] = "yes"
        result = table.getRow(tableRow, 2, 72, 12, [])
        expectedResult = """
        <tr>
            <td class="position number"></td>
            <td class="teamname ">
                teamName
            </td>
            <td class="played number">9</td>
            <td class="won number">1</td>
            <td class="tied number">5</td>
            <td class="lost number">3</td>
            <td class="batpoints number">14</td>
            <td class="bowlpoints number">18</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number">2</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">72</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetRowsNoMatchesPlayed(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            row.maintainInvariants()
            table.tableRows[teamId] = row
        table.promoted, table.relegated = 1, 1
        table.lastCompleteMatchDate = None
        deductionReasons = []
        result = LeagueTable("").getRows(table, deductionReasons)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
            </td>
            <td class="played number">0</td>
            <td class="won number">0</td>
            <td class="tied number">0</td>
            <td class="lost number">0</td>
            <td class="batpoints number">0</td>
            <td class="bowlpoints number">0</td>
            <td class="runrate number"></td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">0</td>
        </tr>
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
            </td>
            <td class="played number">0</td>
            <td class="won number">0</td>
            <td class="tied number">0</td>
            <td class="lost number">0</td>
            <td class="batpoints number">0</td>
            <td class="bowlpoints number">0</td>
            <td class="runrate number"></td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">0</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
            </td>
            <td class="played number">0</td>
            <td class="won number">0</td>
            <td class="tied number">0</td>
            <td class="lost number">0</td>
            <td class="batpoints number">0</td>
            <td class="bowlpoints number">0</td>
            <td class="runrate number"></td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">0</td>
        </tr>
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        <tr>
            <td class="position number"></td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
            </td>
            <td class="played number">0</td>
            <td class="won number">0</td>
            <td class="tied number">0</td>
            <td class="lost number">0</td>
            <td class="batpoints number">0</td>
            <td class="bowlpoints number">0</td>
            <td class="runrate number"></td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">0</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        self.assertEquals([], deductionReasons)
        
    def testGetRowsSomeMatchesPlayedPromoted1Relegated1(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.promoted, table.relegated = 1, 1
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 4)
        deductionReasons = []
        result = LeagueTable("").getRows(table, deductionReasons)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">21</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">25</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">8.00</td>
            <td class="dedpoints number">4</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">26</td>
            <td class="bowlpoints number">24</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">80</td>
        </tr>
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">20</td>
            <td class="bowlpoints number">15</td>
            <td class="runrate number">10.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">65</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        self.assertEquals(["Late start - 4 points deducted"], deductionReasons)
        
    def testGetRowsSomeMatchesPlayedPromoted0Relegated1(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.promoted, table.relegated = 0, 1
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 4)
        deductionReasons = []
        result = LeagueTable("").getRows(table, deductionReasons)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">21</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">25</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">8.00</td>
            <td class="dedpoints number">4</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">26</td>
            <td class="bowlpoints number">24</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">80</td>
        </tr>
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">20</td>
            <td class="bowlpoints number">15</td>
            <td class="runrate number">10.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">65</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        self.assertEquals(["Late start - 4 points deducted"], deductionReasons)
        
    def testGetRowsSomeMatchesPlayedPromoted1Relegated0(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.promoted, table.relegated = 1, 0
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 4)
        deductionReasons = []
        result = LeagueTable("").getRows(table, deductionReasons)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">21</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">25</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">8.00</td>
            <td class="dedpoints number">4</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">26</td>
            <td class="bowlpoints number">24</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">80</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">20</td>
            <td class="bowlpoints number">15</td>
            <td class="runrate number">10.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">65</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        self.assertEquals(["Late start - 4 points deducted"], deductionReasons)
        
    def testGetRowsSomeMatchesPlayedPromoted0Relegated0(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.promoted, table.relegated = 0, 0
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 4)
        deductionReasons = []
        result = LeagueTable("").getRows(table, deductionReasons)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">21</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">25</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">8.00</td>
            <td class="dedpoints number">4</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">26</td>
            <td class="bowlpoints number">24</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">80</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">20</td>
            <td class="bowlpoints number">15</td>
            <td class="runrate number">10.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">65</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        self.assertEquals(["Late start - 4 points deducted"], deductionReasons)
        
    def testGetRowsAllMatchesPlayed(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.promoted, table.relegated = 1, 1
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        table.complete = True
        deductionReasons = []
        result = LeagueTable("").getRows(table, deductionReasons)
        expectedResult = """
        <tr>
            <td class="position number">1</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">21</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">2</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
            </td>
            <td class="played number">5</td>
            <td class="won number">3</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">25</td>
            <td class="bowlpoints number">20</td>
            <td class="runrate number">8.00</td>
            <td class="dedpoints number">4</td>
            <td class="dedkeys">(1)</td>
            <td class="points number">83</td>
        </tr>
        <tr>
            <td class="position number">3</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">26</td>
            <td class="bowlpoints number">24</td>
            <td class="runrate number">12.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">80</td>
        </tr>
        <tr>
            <td class="position number">4</td>
            <td class="teamname ">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
            </td>
            <td class="played number">4</td>
            <td class="won number">2</td>
            <td class="tied number">1</td>
            <td class="lost number">1</td>
            <td class="batpoints number">20</td>
            <td class="bowlpoints number">15</td>
            <td class="runrate number">10.00</td>
            <td class="dedpoints number"></td>
            <td class="dedkeys"></td>
            <td class="points number">65</td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        self.assertEquals(["Late start - 4 points deducted"], deductionReasons)

    def testGetLeagueTableAllMatchesPlayed(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.leagueName = "The League"
        table.promoted, table.relegated = 1, 1
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 3)
        table.complete = True
        table.notes = ["Hello", "Goodbye"]
        result = LeagueTable("").getLeagueTable(table)
        expectedResult = """
        <div class="nobreak">
        <h1>The League</h1>
        <p class="statusMessage">Final table.</p>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
                    </td>
                    <td class="played number">5</td>
                    <td class="won number">3</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">21</td>
                    <td class="bowlpoints number">20</td>
                    <td class="runrate number">12.00</td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">83</td>
                </tr>
                <tr>
                    <td class="position number">2</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
                    </td>
                    <td class="played number">5</td>
                    <td class="won number">3</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">25</td>
                    <td class="bowlpoints number">20</td>
                    <td class="runrate number">8.00</td>
                    <td class="dedpoints number">4</td>
                    <td class="dedkeys">(1)</td>
                    <td class="points number">83</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
                    </td>
                    <td class="played number">4</td>
                    <td class="won number">2</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">26</td>
                    <td class="bowlpoints number">24</td>
                    <td class="runrate number">12.00</td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">80</td>
                </tr>
                <tr>
                    <td class="position number">4</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
                    </td>
                    <td class="played number">4</td>
                    <td class="won number">2</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">20</td>
                    <td class="bowlpoints number">15</td>
                    <td class="runrate number">10.00</td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">65</td>
                </tr>
            </tbody>
        </table>
        <ul class="deductions">
            <li>
                <span class="dedkeys">(1)</span>
                Late start - 4 points deducted.
            </li>
        </ul>
        <p class="tablenotes">
            Hello<br>
            Goodbye
        </p>
        </div>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetLeagueTableSomeMatchesPlayed(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            if i == 1:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 240
                row.batpoints, row.bowlpoints = 20, 15
            elif i == 2:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 300
                row.batpoints, row.bowlpoints = 25, 20
                row.deductions.append(PointsDeduction(4, "Late start"))
            elif i == 3:
                row.won, row.lost, row.tied = 3, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 21, 20
            elif i == 4:
                row.won, row.lost, row.tied = 2, 1, 1
                row.runs, row.balls = 400, 200
                row.batpoints, row.bowlpoints = 26, 24
            row.maintainInvariants()
        table.leagueName = "The League"
        table.lastCompleteMatchDate = datetime.date(2013, 3, 3)
        table.lastScheduledMatchDate = datetime.date(2013, 3, 10)
        result = LeagueTable("").getLeagueTable(table)
        expectedResult = """
        <div class="nobreak">
        <h1>The League</h1>
        <p class="statusMessage">Includes all games up to and including 3rd March 2013.</p>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
                    </td>
                    <td class="played number">5</td>
                    <td class="won number">3</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">21</td>
                    <td class="bowlpoints number">20</td>
                    <td class="runrate number">12.00</td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">83</td>
                </tr>
                <tr>
                    <td class="position number">2</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
                    </td>
                    <td class="played number">5</td>
                    <td class="won number">3</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">25</td>
                    <td class="bowlpoints number">20</td>
                    <td class="runrate number">8.00</td>
                    <td class="dedpoints number">4</td>
                    <td class="dedkeys">(1)</td>
                    <td class="points number">83</td>
                </tr>
                <tr>
                    <td class="position number">3</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
                    </td>
                    <td class="played number">4</td>
                    <td class="won number">2</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">26</td>
                    <td class="bowlpoints number">24</td>
                    <td class="runrate number">12.00</td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">80</td>
                </tr>
                <tr>
                    <td class="position number">4</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
                    </td>
                    <td class="played number">4</td>
                    <td class="won number">2</td>
                    <td class="tied number">1</td>
                    <td class="lost number">1</td>
                    <td class="batpoints number">20</td>
                    <td class="bowlpoints number">15</td>
                    <td class="runrate number">10.00</td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">65</td>
                </tr>
            </tbody>
        </table>
        <ul class="deductions">
            <li>
                <span class="dedkeys">(1)</span>
                Late start - 4 points deducted.
            </li>
        </ul>
        </div>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetLeagueTableNoMatchesPlayed(self):
        table = LeagueTableInReport()
        for i in range(1, 5):
            teamId = "t{0}".format(i)
            row = TableRow(teamId, "Team {0}".format(i))
            table.tableRows[teamId] = row
            row.maintainInvariants()
        table.leagueName = "The League"
        table.lastCompleteMatchDate = None
        table.lastScheduledMatchDate = datetime.date(2013, 3, 10)
        result = LeagueTable("").getLeagueTable(table)
        expectedResult = """
        <div class="nobreak">
        <h1>The League</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Team 1</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Team 2</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Team 3</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Team 4</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
            </tbody>
        </table>
        </div>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetDeductionListItemPointsDeducted1(self):
        deduction = "Being a bit crap - 1 point deducted"
        result = LeagueTable("").getDeductionListItem(deduction, 4)
        expectedResult = """
        <li>
            <span class="dedkeys">(4)</span>
            Being a bit crap - 1 point deducted.
        </li>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetDeductionListItemPointsDeductedMoreThan1(self):
        deduction = "Being very crap - 10 points deducted"
        result = LeagueTable("").getDeductionListItem(deduction, 2)
        expectedResult = """
        <li>
            <span class="dedkeys">(2)</span>
            Being very crap - 10 points deducted.
        </li>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetDeductionInfoForTableNoDeductions(self):
        deductionReasons = []
        result = LeagueTable("").getDeductionInfoForTable(deductionReasons)
        expectedResult = ""
        self.assertEqual(expectedResult, result)
        
    def testGetDeductionInfoForTableSomeDeductions(self):
        deductionReasons = []
        deductionReasons.append("Being a bit crap - 1 point deducted")
        deductionReasons.append("Being somewhat crap - 4 points deducted")
        deductionReasons.append("Being extremely crap - 10 points deducted")
        result = LeagueTable("").getDeductionInfoForTable(deductionReasons)
        expectedResult = """
        <ul class="deductions">
            <li>
                <span class="dedkeys">(1)</span>
                Being a bit crap - 1 point deducted.
            </li>
            <li>
                <span class="dedkeys">(2)</span>
                Being somewhat crap - 4 points deducted.
            </li>
            <li>
                <span class="dedkeys">(3)</span>
                Being extremely crap - 10 points deducted.
            </li>
        </ul>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBodyOneLeague(self):
        report = LeagueTableReport()
        for l in range(1, 2):
            table = LeagueTableInReport()
            report.tables.append(table)
            table.leagueName = "League {0}".format(l)
            for t in range(1, 3):
                teamId = "t{0}{1}".format(l, t)
                row = TableRow(teamId, "Team {0}/{1}".format(l, t))
                table.tableRows[teamId] = row
                row.maintainInvariants()
        result = LeagueTable("").getReportBody(report)
        expectedResult = """
        <div class="nobreak">
        <h1>League 1</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t11">Team 1/1</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t12">Team 1/2</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
            </tbody>
        </table>
        </div>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportBodyMoreThanOneLeague(self):
        report = LeagueTableReport()
        for l in range(1, 3):
            table = LeagueTableInReport()
            report.tables.append(table)
            table.leagueName = "League {0}".format(l)
            for t in range(1, 3):
                teamId = "t{0}{1}".format(l, t)
                row = TableRow(teamId, "Team {0}/{1}".format(l, t))
                table.tableRows[teamId] = row
                row.maintainInvariants()
        result = LeagueTable("").getReportBody(report)
        expectedResult = """
        <div class="nobreak">
        <h1>League 1</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t11">Team 1/1</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t12">Team 1/2</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
            </tbody>
        </table>
        </div>
        <div class="nobreak">
        <h1>League 2</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t21">Team 2/1</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t22">Team 2/2</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
            </tbody>
        </table>
        </div>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContent(self):
        report = LeagueTableReport()
        for l in range(1, 2):
            table = LeagueTableInReport()
            report.tables.append(table)
            table.leagueName = "League {0}".format(l)
            for t in range(1, 3):
                teamId = "t{0}{1}".format(l, t)
                row = TableRow(teamId, "Team {0}/{1}".format(l, t))
                table.tableRows[teamId] = row
                row.maintainInvariants()
        result = LeagueTable("").getReportContent(report)
        expectedResult = """
        <div class="nobreak">
        <h1>League 1</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="position number">1</td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t11">Team 1/1</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
                <tr>
                    <td class="position number"></td>
                    <td class="teamname ">
                        <a href="/cgi-bin/page.py?id=teamFixtures&team=t12">Team 1/2</a>
                    </td>
                    <td class="played number">0</td>
                    <td class="won number">0</td>
                    <td class="tied number">0</td>
                    <td class="lost number">0</td>
                    <td class="batpoints number">0</td>
                    <td class="bowlpoints number">0</td>
                    <td class="runrate number"></td>
                    <td class="dedpoints number"></td>
                    <td class="dedkeys"></td>
                    <td class="points number">0</td>
                </tr>
            </tbody>
        </table>
        </div>
        <p class="calctext noprint">
        <b>How the points are worked out:</b>
        <br>
            12 points for a win, 6 points for a tie, 0 points for a loss.<br>
            Batting points: 1 point for every 10 runs scored in excess of 60, plus (only for teams
            batting second and winning) 1 point for each wicket in
            hand. A maximum of 6 points per innings.<br>
            Bowling points: 1 point per wicket taken. If the batting side has fewer than six players,
            and the missing player(s) would have been required to bat if present, a bowling bonus point is awarded
            for each missing player.<br>
            In a game won by default, the winning team receives 3 batting points and
            6 bowling points as well as 12 points for winning.
        <br>
        Teams level on points are ranked by
        <b>run rate</b>, which is the total number of runs scored, divided by the total
        number of overs faced. For this purpose, an innings where the batting
        side is all out counts as lasting the full number of available overs, even if it is actually shorter.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()