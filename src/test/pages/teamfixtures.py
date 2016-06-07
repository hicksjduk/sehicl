'''
Created on 31 Jul 2013

@author: hicksj
'''
from pages.pageLink import PageLink
from pages.teamfixtures import TeamFixtures
from reports.teamfixturesreport import MatchInReport, TeamFixturesReport
from test.testbase import TestBase
import datetime
import unittest

class Test(TestBase):

    def testGetMatchLinePlayedAndNotTied(self):
        teamId = "HavantA"
        leagueResLink = PageLink("leagueResults", TeamFixtures(""), {"league": "Division1"})
        match = MatchInReport()
        match.opponentId = "FarehamCroftonB"
        match.opponentName = "Fareham & Crofton B"
        match.datetime = datetime.datetime(2012, 9, 30, 18, 15)
        match.court = "B"
        match.home = True
        match.result = "Won"
        match.margin = "30 runs"
        result = TeamFixtures("").getMatchLine(match, teamId, leagueResLink)
        expectedResult = """
        <tr>
        <td class="date">30th Sep 12</td>
        <td class="time">6:15</td>
        <td class="court">B</td>
        <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=FarehamCroftonB">Fareham & Crofton B</a></td>
        <td class="homeAway">H</td>
        <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division1#HavantAFarehamCroftonB">Won by 30 runs</a></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLinePlayedAndTied(self):
        teamId = "HavantA"
        leagueResLink = PageLink("leagueResults", TeamFixtures(""), {"league": "Division1"})
        match = MatchInReport()
        match.opponentId = "FarehamCroftonB"
        match.opponentName = "Fareham & Crofton B"
        match.datetime = datetime.datetime(2012, 9, 30, 18, 15)
        match.court = "B"
        match.home = True
        match.result = "Tied"
        match.margin = None
        result = TeamFixtures("").getMatchLine(match, teamId, leagueResLink)
        expectedResult = """
        <tr>
        <td class="date">30th Sep 12</td>
        <td class="time">6:15</td>
        <td class="court">B</td>
        <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=FarehamCroftonB">Fareham & Crofton B</a></td>
        <td class="homeAway">H</td>
        <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division1#HavantAFarehamCroftonB">Tied</a></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLineAwarded(self):
        teamId = "HavantA"
        leagueResLink = PageLink("leagueResults", TeamFixtures(""), {"league": "Division1"})
        match = MatchInReport()
        match.opponentId = "FarehamCroftonB"
        match.opponentName = "Fareham & Crofton B"
        match.datetime = datetime.datetime(2012, 9, 30, 18, 15)
        match.court = "B"
        match.home = False
        match.result = "Lost"
        match.margin = "default"
        result = TeamFixtures("").getMatchLine(match, teamId, leagueResLink)
        expectedResult = """
        <tr>
        <td class="date">30th Sep 12</td>
        <td class="time">6:15</td>
        <td class="court">B</td>
        <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=FarehamCroftonB">Fareham & Crofton B</a></td>
        <td class="homeAway">A</td>
        <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division1#FarehamCroftonBHavantA">Lost by default</a></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetMatchLineNotPlayed(self):
        teamId = "HavantA"
        leagueResLink = PageLink("leagueResults", TeamFixtures(""), {"league": "Division1"})
        match = MatchInReport()
        match.opponentId = "FarehamCroftonB"
        match.opponentName = "Fareham & Crofton B"
        match.datetime = datetime.datetime(2012, 9, 30, 18, 15)
        match.court = "B"
        match.home = True
        match.result = None
        match.margin = None
        result = TeamFixtures("").getMatchLine(match, teamId, leagueResLink)
        expectedResult = """
        <tr>
        <td class="date">30th Sep 12</td>
        <td class="time">6:15</td>
        <td class="court">B</td>
        <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=FarehamCroftonB">Fareham & Crofton B</a></td>
        <td class="homeAway">H</td>
        <td class="result"></td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContent(self):
        report = TeamFixturesReport()
        report.teamId = "IBMSouthHants"
        report.teamName = "IBM South Hants"
        report.leagueId = "Division3"
        report.leagueName = "Division 3"
        report.matches = []
        match = MatchInReport()
        match.datetime = datetime.datetime(2013, 1, 20, 21, 15)
        match.opponentId = "Corinthians"
        match.opponentName = "Corinthians"
        match.court = "B"
        match.home = False
        match.result = "Lost"
        match.margin = "4 wickets"
        report.matches.append(match)
        match = MatchInReport()
        match.datetime = datetime.datetime(2012, 10, 7, 18, 15)
        match.opponentId = "PortsmouthB"
        match.opponentName = "Portsmouth B"
        match.court = "A"
        match.home = True
        match.result = None
        match.margin = None
        report.matches.append(match)
        result = TeamFixtures("").getReportContent(report)
        expectedResult = """
        <h1>IBM South Hants (<a href="/cgi-bin/page.py?id=leagueFixtures&league=Division3">Division 3</a>)</h1>
        <table id="teamfix">
            <thead>
                <tr>
                    <th class="date">Date</th>
                    <th class="time">Time</th>
                    <th class="court">Court</th>
                    <th class="opponent">Opponent</th>
                    <th class="homeAway">H/A</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="date">7th Oct 12</td>
                    <td class="time">6:15</td>
                    <td class="court">A</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=PortsmouthB">Portsmouth B</a></td>
                    <td class="homeAway">H</td>
                    <td class="result"></td>
                </tr>
                <tr>
                    <td class="date">20th Jan 13</td>
                    <td class="time">9:15</td>
                    <td class="court">B</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=Corinthians">Corinthians</a></td>
                    <td class="homeAway">A</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#CorinthiansIBMSouthHants">Lost by 4 wickets</a></td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetContentNoTeamIdSpecified(self):
        try:
            TeamFixtures("").getContent()
            self.fail("Should have thrown an exception")
        except NameError:
            pass
        except:
            raise

    def testGetContentTeamIdSpecified(self):
        page = TeamFixtures("")
        page.allParams = {"team": "IBMSouthHants", "xmlFile": "testData/2012-13.xml"}
        result = page.getContent()
        expectedResult = """
        <h1>IBM South Hants (<a href="/cgi-bin/page.py?id=leagueFixtures&league=Division3">Division 3</a>)</h1>
        <table id="teamfix">
            <thead>
                <tr>
                    <th class="date">Date</th>
                    <th class="time">Time</th>
                    <th class="court">Court</th>
                    <th class="opponent">Opponent</th>
                    <th class="homeAway">H/A</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="date">7th Oct 12</td>
                    <td class="time">8:15</td>
                    <td class="court">A</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=PortsmouthB">Portsmouth B</a></td>
                    <td class="homeAway">H</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#IBMSouthHantsPortsmouthB">Lost by 2 wickets</a></td>
                </tr>
                <tr>
                    <td class="date">28th Oct 12</td>
                    <td class="time">7:15</td>
                    <td class="court">A</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=FarehamCroftonC">Fareham & Crofton C</a></td>
                    <td class="homeAway">A</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#FarehamCroftonCIBMSouthHants">Won by 5 wickets</a></td>
                </tr>
                <tr>
                    <td class="date">18th Nov 12</td>
                    <td class="time">8:15</td>
                    <td class="court">A</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=PortsmouthPriory">Portsmouth Priory</a></td>
                    <td class="homeAway">H</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#IBMSouthHantsPortsmouthPriory">Won by 31 runs</a></td>
                </tr>
                <tr>
                    <td class="date">2nd Dec 12</td>
                    <td class="time">9:15</td>
                    <td class="court">B</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=WaterloovilleB">Waterlooville B</a></td>
                    <td class="homeAway">A</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#WaterloovilleBIBMSouthHants">Lost by 37 runs</a></td>
                </tr>
                <tr>
                    <td class="date">16th Dec 12</td>
                    <td class="time">5:15</td>
                    <td class="court">B</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=Petersfield">Petersfield</a></td>
                    <td class="homeAway">H</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#IBMSouthHantsPetersfield">Won by 24 runs</a></td>
                </tr>
                <tr>
                    <td class="date">6th Jan 13</td>
                    <td class="time">8:15</td>
                    <td class="court">B</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=Emsworth">Emsworth</a></td>
                    <td class="homeAway">A</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#EmsworthIBMSouthHants">Won by 18 runs</a></td>
                </tr>
                <tr>
                    <td class="date">20th Jan 13</td>
                    <td class="time">9:15</td>
                    <td class="court">B</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=Corinthians">Corinthians</a></td>
                    <td class="homeAway">A</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#CorinthiansIBMSouthHants">Lost by 4 wickets</a></td>
                </tr>
                <tr>
                    <td class="date">10th Feb 13</td>
                    <td class="time">6:15</td>
                    <td class="court">B</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=BedhamptonB">Bedhampton B</a></td>
                    <td class="homeAway">H</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#IBMSouthHantsBedhamptonB">Won by 34 runs</a></td>
                </tr>
                <tr>
                    <td class="date">10th Mar 13</td>
                    <td class="time">9:15</td>
                    <td class="court">A</td>
                    <td class="opponent"><a href="/cgi-bin/page.py?id=teamFixtures&team=Denmead">Denmead</a></td>
                    <td class="homeAway">A</td>
                    <td class="result"><a href="/cgi-bin/page.py?id=leagueResults&league=Division3#DenmeadIBMSouthHants">Won by 1 wicket</a></td>
                </tr>
            </tbody>
        </table>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetContentTeamIdSpecifiedNoFixtures(self):
        page = TeamFixtures("")
        page.allParams = {"team": "IBMSouthHants", "xmlFile": "testData/2013-14.xml"}
        result = page.getContent()
        self.assertNotEqual(None, result)

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetMatchLine']
    unittest.main()