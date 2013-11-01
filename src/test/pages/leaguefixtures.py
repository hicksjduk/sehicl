'''
Created on 1 Aug 2013

@author: hicksj
'''
import unittest
from reports.leaguefixturesreport import MatchInReport, LeagueFixturesReport
import datetime
from pages.leaguefixtures import LeagueFixtures
from test.testbase import TestBase


class LeagueFixturesTest(TestBase):


    def testGetMatchLinePrevTimeNone(self):
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 6)
        match.time = datetime.time(16, 15)
        match.court = "A"
        match.homeTeamId = "IBMSouthHants"
        match.homeTeamName = "IBM South Hants"
        match.awayTeamId = "HavantA"
        match.awayTeamName = "Havant A"
        prevTime = None
        result = LeagueFixtures("").getMatchLine(match, prevTime)
        expectedResult = """
        <tr>
            <td class="time">4:15</td>
            <td class="court">A</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=IBMSouthHants">IBM South Hants</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=HavantA">Havant A</a>
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLinePrevTimeDifferent(self):
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 6)
        match.time = datetime.time(16, 15)
        match.court = "A"
        match.homeTeamId = "IBMSouthHants"
        match.homeTeamName = "IBM South Hants"
        match.awayTeamId = "HavantA"
        match.awayTeamName = "Havant A"
        prevTime = datetime.time(17, 15)
        result = LeagueFixtures("").getMatchLine(match, prevTime)
        expectedResult = """
        <tr>
            <td class="time">4:15</td>
            <td class="court">A</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=IBMSouthHants">IBM South Hants</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=HavantA">Havant A</a>
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLinePrevTimeSame(self):
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 6)
        match.time = datetime.time(16, 15)
        match.court = "A"
        match.homeTeamId = "IBMSouthHants"
        match.homeTeamName = "IBM South Hants"
        match.awayTeamId = "HavantA"
        match.awayTeamName = "Havant A"
        prevTime = datetime.time(16, 15)
        result = LeagueFixtures("").getMatchLine(match, prevTime)
        expectedResult = """
        <tr>
            <td class="time"></td>
            <td class="court">A</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=IBMSouthHants">IBM South Hants</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=HavantA">Havant A</a>
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLinesForDateNoMatches(self):
        theDate = None
        matches = []
        result = LeagueFixtures("").getMatchLines(theDate, matches)
        self.assertEqual("", result)

    def testGetMatchLinesForDateMatchesAtDifferentTimes(self):
        theDate = datetime.date(2013, 10, 13)
        matches = []
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(21, 15)
        match.court = "A"
        match.homeTeamId = "aaa"
        match.homeTeamName = "asagasgh"
        match.awayTeamId = "bbb"
        match.awayTeamName = "sgsdsdgsd"
        matches.append(match)
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(19, 15)
        match.court = "B"
        match.homeTeamId = "sdfgfds"
        match.homeTeamName = "sASGHSDAS"
        match.awayTeamId = "asda"
        match.awayTeamName = "ffjfdf"
        matches.append(match)
        result = LeagueFixtures("").getMatchLines(theDate, matches)
        expectedResult = """
        <tbody class="nobreak">
        <tr>
            <td class="date" colspan="3">13th October 2013</td>
        </tr>
        <tr>
            <td class="time">7:15</td>
            <td class="court">B</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=sdfgfds">sASGHSDAS</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=asda">ffjfdf</a>
            </td>
        </tr>
        <tr>
            <td class="time">9:15</td>
            <td class="court">A</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=aaa">asagasgh</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=bbb">sgsdsdgsd</a>
            </td>
        </tr>
        </tbody>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLinesForDateMatchesAtSameTime(self):
        theDate = datetime.date(2013, 10, 13)
        matches = []
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(19, 15)
        match.court = "A"
        match.homeTeamId = "aaa"
        match.homeTeamName = "asagasgh"
        match.awayTeamId = "bbb"
        match.awayTeamName = "sgsdsdgsd"
        matches.append(match)
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(19, 15)
        match.court = "B"
        match.homeTeamId = "sdfgfds"
        match.homeTeamName = "sASGHSDAS"
        match.awayTeamId = "asda"
        match.awayTeamName = "ffjfdf"
        matches.append(match)
        result = LeagueFixtures("").getMatchLines(theDate, matches)
        expectedResult = """
        <tbody class="nobreak">
        <tr>
            <td class="date" colspan="3">13th October 2013</td>
        </tr>
        <tr>
            <td class="time">7:15</td>
            <td class="court">A</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=aaa">asagasgh</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=bbb">sgsdsdgsd</a>
            </td>
        </tr>
        <tr>
            <td class="time"></td>
            <td class="court">B</td>
            <td class="teams">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=sdfgfds">sASGHSDAS</a>
                v
                <a href="/cgi-bin/page.py?id=teamFixtures&team=asda">ffjfdf</a>
            </td>
        </tr>
        </tbody>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetFixtureList(self):
        matches = []
        match = MatchInReport()
        match.date = datetime.date(2012, 10, 10)
        match.time = datetime.time(19, 15)
        match.court = "A"
        match.homeTeamId = "aaa"
        match.homeTeamName = "asagasgh"
        match.awayTeamId = "bbb"
        match.awayTeamName = "sgsdsdgsd"
        matches.append(match)
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(19, 15)
        match.court = "B"
        match.homeTeamId = "sdfgfds"
        match.homeTeamName = "sASGHSDAS"
        match.awayTeamId = "asda"
        match.awayTeamName = "ffjfdf"
        matches.append(match)
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "sadgsadg"
        match.homeTeamName = "fdhdahadhfa"
        match.awayTeamId = "sadsgasdg"
        match.awayTeamName = "hsdfhsdfhs"
        matches.append(match)
        report = LeagueFixturesReport()
        report.leagueId = "aafagf"
        report.leagueName = "sgasdlghsdlkghsdakgsd"
        report.matches = matches
        result = LeagueFixtures("").getFixtureList(report)
        expectedResult = """
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="fixlist">
            <tbody class="nobreak">
            <tr>
                <td class="date" colspan="3">10th October 2012</td>
            </tr>
            <tr>
                <td class="time">7:15</td>
                <td class="court">A</td>
                <td class="teams">
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=aaa">asagasgh</a>
                    v
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=bbb">sgsdsdgsd</a>
                </td>
            </tr>
            </tbody>
            <tbody class="nobreak">
            <tr>
                <td class="date" colspan="3">10th October 2013</td>
            </tr>
            <tr>
                <td class="time">6:15</td>
                <td class="court">A</td>
                <td class="teams">
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sadgsadg">fdhdahadhfa</a>
                    v
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sadsgasdg">hsdfhsdfhs</a>
                </td>
            </tr>
            <tr>
                <td class="time">7:15</td>
                <td class="court">B</td>
                <td class="teams">
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sdfgfds">sASGHSDAS</a>
                    v
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=asda">ffjfdf</a>
                </td>
            </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContentLeagueSpecifiedNoMatches(self):
        report = LeagueFixturesReport()
        report.leagueId = "aafagf"
        report.leagueName = "sgasdlghsdlkghsdakgsd"
        result = LeagueFixtures("").getReportContent(report)
        expectedResult = """
        <h1>sgasdlghsdlkghsdakgsd</h1>
        <p>There are no outstanding fixtures at present.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportContentLeagueSpecifiedSomeMatches(self):
        report = LeagueFixturesReport()
        report.leagueId = "aafagf"
        report.leagueName = "sgasdlghsdlkghsdakgsd"
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "sadgsadg"
        match.homeTeamName = "fdhdahadhfa"
        match.awayTeamId = "sadsgasdg"
        match.awayTeamName = "hsdfhsdfhs"
        report.matches.append(match)
        result = LeagueFixtures("").getReportContent(report)
        expectedResult = """
        <h1>sgasdlghsdlkghsdakgsd</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="fixlist">
            <tbody class="nobreak">
            <tr>
                <td class="date" colspan="3">10th October 2013</td>
            </tr>
            <tr>
                <td class="time">6:15</td>
                <td class="court">A</td>
                <td class="teams">
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sadgsadg">fdhdahadhfa</a>
                    v
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sadsgasdg">hsdfhsdfhs</a>
                </td>
            </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContentLeagueNotSpecifiedNoMatches(self):
        report = LeagueFixturesReport()
        report.leagueId = None
        report.leagueName = None
        result = LeagueFixtures("").getReportContent(report)
        expectedResult = """
        <h1>Fixtures</h1>
        <p>There are no outstanding fixtures at present.</p>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportContentLeagueNotSpecifiedSomeMatches(self):
        report = LeagueFixturesReport()
        report.leagueId = None
        report.leagueName = None
        match = MatchInReport()
        match.date = datetime.date(2013, 10, 10)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "sadgsadg"
        match.homeTeamName = "fdhdahadhfa"
        match.awayTeamId = "sadsgasdg"
        match.awayTeamName = "hsdfhsdfhs"
        match.leagueId = "asdgasdgasd"
        match.leagueName = "sghsaghsadlkghskgshkgsda"
        report.matches.append(match)
        result = LeagueFixtures("").getReportContent(report)
        expectedResult = """
        <h1>Fixtures</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="fixlist">
            <tbody class="nobreak">
            <tr>
                <td class="date" colspan="3">10th October 2013</td>
            </tr>
            <tr>
                <td class="time">6:15</td>
                <td class="court">A</td>
                <td class="teams">
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sadgsadg">fdhdahadhfa</a>
                    v
                    <a href="/cgi-bin/page.py?id=teamFixtures&team=sadsgasdg">hsdfhsdfhs</a>
                </td>
                <td>
                    <a href="/cgi-bin/page.py?id=leagueFixtures&league=asdgasdgasd">sghsaghsadlkghskgshkgsda</a>
                </td>
            </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()