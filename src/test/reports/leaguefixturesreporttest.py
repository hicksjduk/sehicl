'''
Created on 31 Jul 2013

@author: hicksj
'''
import unittest
from reports.leaguefixturesreport import LeagueFixturesReportGenerator
from xml.etree import ElementTree
from operator import itemgetter
import datetime


class TestLeagueFixturesReportGenerator(unittest.TestCase):


    def testGetLeagueElementsLeagueSpecifiedNotFound(self):
        rootElement = ElementTree.parse("testData/2013-14.xml")
        result = LeagueFixturesReportGenerator().getLeagueElements(rootElement, "ghgsd")
        self.assertEqual(0, len(result))
        
    def testGetLeagueElementsLeagueSpecifiedFound(self):
        rootElement = ElementTree.parse("testData/2013-14.xml")
        result = LeagueFixturesReportGenerator().getLeagueElements(rootElement, "ColtsUnder16")
        self.assertEqual(1, len(result))
        self.assertEqual("Colts Under-16", result[0].find("name").text)

    def testGetLeagueElementsLeagueNotSpecified(self):
        rootElement = ElementTree.parse("testData/2013-14.xml")
        result = LeagueFixturesReportGenerator().getLeagueElements(rootElement, None)
        expectedNames = ["Division 1", "Division 2", "Division 3", "Division 4", "Colts Under-16", "Colts Under-13"]
        names = [l.find("name").text for l in result]
        for e, a in zip(sorted(expectedNames), sorted(names)):
            self.assertEqual(e, a)

    def testGetInningsDataBattingFirstBallsNotSpecifiedWicketsNotSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>true</battingFirst>
            <innings>
                <runsScored>223</runsScored>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(True, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(6, result["wickets"])
        self.assertEqual(maxBalls, result["balls"])
        
    def testGetInningsDataBattingSecondBallsNotSpecifiedWicketsNotSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>false</battingFirst>
            <innings>
                <runsScored>223</runsScored>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(False, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(6, result["wickets"])
        self.assertEqual(maxBalls, result["balls"])
        
    def testGetInningsDataBattingFirstBallsSpecifiedWicketsNotSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>true</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <ballsBowled>63</ballsBowled>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(True, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(6, result["wickets"])
        self.assertEqual(63, result["balls"])
        
    def testGetInningsDataBattingSecondBallsSpecifiedWicketsNotSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>false</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <ballsBowled>63</ballsBowled>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(False, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(6, result["wickets"])
        self.assertEqual(63, result["balls"])
        
    def testGetInningsDataBattingFirstBallsNotSpecifiedWicketsSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>true</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <wicketsLost>4</wicketsLost>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(True, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(4, result["wickets"])
        self.assertEqual(maxBalls, result["balls"])
        
    def testGetInningsDataBattingSecondBallsNotSpecifiedWicketsSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>false</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <wicketsLost>4</wicketsLost>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(False, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(4, result["wickets"])
        self.assertEqual(maxBalls, result["balls"])
        
    def testGetInningsDataBattingFirstBallsSpecifiedWicketsSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>true</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <ballsBowled>63</ballsBowled>
                <wicketsLost>4</wicketsLost>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(True, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(4, result["wickets"])
        self.assertEqual(63, result["balls"])
        
    def testGetInningsDataBattingSecondBallsSpecifiedWicketsSpecified(self):
        xml = """
        <teamInMatch>
            <battingFirst>false</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <ballsBowled>63</ballsBowled>
                <wicketsLost>4</wicketsLost>
            </innings>
        </teamInMatch>
        """
        teamInMatchElement = ElementTree.fromstring(xml)
        maxBalls = 42
        result = LeagueFixturesReportGenerator().getInningsData(teamInMatchElement, maxBalls)
        self.assertEqual(False, result["batFirst"])
        self.assertEqual(223, result["runs"])
        self.assertEqual(4, result["wickets"])
        self.assertEqual(63, result["balls"])
        
    def testSortInnings(self):
        xml = """
        <playedMatch>
        <teamInMatch>
            <battingFirst>false</battingFirst>
            <innings>
                <runsScored>223</runsScored>
                <ballsBowled>63</ballsBowled>
                <wicketsLost>4</wicketsLost>
            </innings>
        </teamInMatch>
        <teamInMatch>
            <battingFirst>true</battingFirst>
            <innings>
                <runsScored>142</runsScored>
                <ballsBowled>63</ballsBowled>
                <wicketsLost>4</wicketsLost>
            </innings>
        </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        generator = LeagueFixturesReportGenerator()
        innings = [generator.getInningsData(t, 72) for t in playedMatchElement.findall("teamInMatch")]
        sortedInns = sorted(innings, key=itemgetter("batFirst"), reverse=True)
        self.assertEqual(142, sortedInns[0]["runs"])
        
    def testIsMatchCompleteNotPlayedOrAwarded(self):
        xml = """
        <match>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        generator = LeagueFixturesReportGenerator()
        result = generator.isMatchComplete(matchElement)
        expectedResult = False
        self.assertEqual(expectedResult, result)
        
    def testIsMatchCompleteAwarded(self):
        xml = """
        <match>
            <awardedMatch/>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        generator = LeagueFixturesReportGenerator()
        result = generator.isMatchComplete(matchElement)
        expectedResult = True
        self.assertEqual(expectedResult, result)
        
    def testIsMatchCompletePlayed(self):
        xml = """
        <match>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <innings>
                        <runsScored>140</runsScored>
                        <wicketsLost>6</wicketsLost>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <innings>
                        <runsScored>141</runsScored>
                        <wicketsLost>4</wicketsLost>
                        <ballsBowled>60</ballsBowled>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        generator = LeagueFixturesReportGenerator()
        result = generator.isMatchComplete(matchElement)
        expectedResult = True
        self.assertEqual(expectedResult, result)
        
    def testGetIncompleteMatchElementsOneCompleteOneIncomplete(self):
        xml = """
        <league>
            <match>
                <court>A</court>
            </match>
            <match>
                <court>B</court>
                <awardedMatch/>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        generator = LeagueFixturesReportGenerator()
        result = generator.getIncompleteMatchElements(leagueElement)
        self.assertEqual(1, len(result))
        self.assertEqual("A", result[0].find("court").text)
        
    def testGetTeamNames(self):
        xml = """
        <league>
            <team id="t1"><name>Team 1</name></team>
            <team id="t2"><name>Team 2</name></team>
            <team id="t3"><name>Team 3</name></team>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        generator = LeagueFixturesReportGenerator()
        result = generator.getTeamNames(leagueElement)
        expectedResult = {}
        for i in range(1, 4):
            expectedResult["t{0}".format(i)] = "Team {0}".format(i)
        self.assertEqual(len(expectedResult), len(result))
        for k, v in expectedResult.items():
            self.assertEqual(v, result[k])
            
    def testGetMatchLeagueSpecified(self):
        xml = """
        <league id="sagasdgas">
        <name>adsgsaghsagsdglksa</name>
        <match>
            <date>2013-07-31.12:15</date>
            <pitch>B</pitch>
            <homeTeam id="t2"/>
            <awayTeam id="t1"/>
        </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        matchElement = leagueElement.find("match")
        teams = {"t1": "agfaga", "t2": "aaaaaaa"}
        generator = LeagueFixturesReportGenerator()
        result = generator.getMatch(matchElement, teams, leagueElement)
        self.assertEqual(datetime.date(2013, 7, 31), result.date)
        self.assertEqual(datetime.time(12, 15), result.time)
        self.assertEqual("B", result.court)
        self.assertEqual("t2", result.homeTeamId)
        self.assertEqual("aaaaaaa", result.homeTeamName)
        self.assertEqual("t1", result.awayTeamId)
        self.assertEqual("agfaga", result.awayTeamName)
        self.assertEqual("sagasdgas", result.leagueId)
        self.assertEqual("adsgsaghsagsdglksa", result.leagueName)
        
    def testGetMatchLeagueNotSpecified(self):
        xml = """
        <league id="sagasdgas">
        <name>adsgsaghsagsdglksa</name>
        <match>
            <date>2013-07-31.12:15</date>
            <pitch>B</pitch>
            <homeTeam id="t2"/>
            <awayTeam id="t1"/>
        </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        matchElement = leagueElement.find("match")
        teams = {"t1": "agfaga", "t2": "aaaaaaa"}
        generator = LeagueFixturesReportGenerator()
        result = generator.getMatch(matchElement, teams, None)
        self.assertEqual(datetime.date(2013, 7, 31), result.date)
        self.assertEqual(datetime.time(12, 15), result.time)
        self.assertEqual("B", result.court)
        self.assertEqual("t2", result.homeTeamId)
        self.assertEqual("aaaaaaa", result.homeTeamName)
        self.assertEqual("t1", result.awayTeamId)
        self.assertEqual("agfaga", result.awayTeamName)
        self.assertEqual(None, result.leagueId)
        self.assertEqual(None, result.leagueName)
        
    def testGetReportOneLeagueNoIncompleteMatches(self):
        rootElement = ElementTree.parse("testData/2012-13.xml")
        leagueId = "Division2"
        generator = LeagueFixturesReportGenerator()
        result = generator.getReport(rootElement, leagueId)
        self.assertEquals(leagueId, result.leagueId)
        self.assertEquals("Division 2", result.leagueName)
        self.assertEquals(0, len(result.matches))
            
    def testGetReportOneLeagueIncompleteMatches(self):
        rootElement = ElementTree.parse("testData/2013-14.xml")
        leagueId = "Division1"
        generator = LeagueFixturesReportGenerator()
        result = generator.getReport(rootElement, leagueId)
        self.assertEquals(leagueId, result.leagueId)
        self.assertEquals("Division 1", result.leagueName)
        self.assertEquals(45, len(result.matches))
        self.assertEquals(None, result.matches[0].leagueId)
        self.assertEquals(None, result.matches[0].leagueName)
            
    def testGetReportAllLeaguesNoIncompleteMatches(self):
        rootElement = ElementTree.parse("testData/2011-12.xml")
        leagueId = None
        generator = LeagueFixturesReportGenerator()
        result = generator.getReport(rootElement, leagueId)
        self.assertEquals(None, result.leagueId)
        self.assertEquals(None, result.leagueName)
        self.assertEquals(0, len(result.matches))
            
    def testGetReportAllLeaguesIncompleteMatches(self):
        rootElement = ElementTree.parse("testData/2013-14.xml")
        leagueId = None
        generator = LeagueFixturesReportGenerator()
        result = generator.getReport(rootElement, leagueId)
        self.assertEquals(None, result.leagueId)
        self.assertEquals(None, result.leagueName)
        self.assertEquals(270, len(result.matches))
        self.assertNotEqual(None, result.matches[0].leagueId)
        self.assertNotEqual(None, result.matches[0].leagueName)
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetLeagueElementNotFound']
    unittest.main()