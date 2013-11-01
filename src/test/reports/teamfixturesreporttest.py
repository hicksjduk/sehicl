'''
Created on 26 Jul 2013

@author: hicksj
'''
from datetime import datetime
from xml.etree import ElementTree
import unittest
from reports.teamfixturesreport import TeamFixturesReportGenerator,\
    MatchInReport


class TeamFixturesReportGeneratorTest(unittest.TestCase):

    def testGetTeamElementsNoneFound(self):
        xml = """
        <league/>
        """
        league = ElementTree.fromstring(xml)
        result = TeamFixturesReportGenerator().getTeams(league)
        self.assertEqual(0, len(result))

    def testGetTeamsSomeFound(self):
        xml = """
        <league>
        <team id="Corinthians">
            <name>Corinthians</name>
        </team>
        <team id="Curdridge">
            <name>Curdridge</name>
        </team>
        <team id="FarehamCroftonB">
            <name>Fareham &amp; Crofton B</name>
        </team>
        <team id="HaylingIsland">
            <name>Hayling Island</name>
        </team>
        <team id="IBMSouthHants">
            <name>IBM South Hants</name>
        </team>
        <team id="LocksHeathA">
            <name>Locks Heath A</name>
        </team>
        <team id="PortchesterA">
            <name>Portchester A</name>
        </team>
        <team id="PortsmouthSouthsea">
            <name>Portsmouth &amp; Southsea</name>
        </team>
        <team id="WaterloovilleB">
            <name>Waterlooville B</name>
        </team>
        <team id="XIIthMenA">
            <name>XIIth Men A</name>
        </team>
        </league>
        """
        league = ElementTree.fromstring(xml)
        result = TeamFixturesReportGenerator().getTeams(league)
        expectedTeamNames = ['Corinthians', 'Curdridge', 'Fareham & Crofton B', 'Hayling Island', 'IBM South Hants', 'Locks Heath A', 'Portchester A', 'Portsmouth & Southsea', 'Waterlooville B', 'XIIth Men A']
        self.assertEqual(len(expectedTeamNames), len(result))
        for elem in result.values():
            self.assertTrue(elem in expectedTeamNames, elem)

    def testGetLeagueElement(self):
        xml = """
        <model>
            <league>
                <name>Division 1</name>
            </league>
            <league>
                <name>Division 2</name>
                <team id="IBMSouthHants"/>
            </league>
            <league>
                <name>Division 3</name>
            </league>
        </model>
        """
        root = ElementTree.fromstring(xml)
        result = TeamFixturesReportGenerator().getLeagueElement(root, "IBMSouthHants")
        self.assertNotEqual(None, result)
        self.assertEqual("Division 2", result.find("name").text)
        
    def testGetMatchElementsNoneFound(self):
        xml = """
        <league>
            <match>
                <homeTeam id="Corinthians"/>
                <awayTeam id="PortsmouthSouthsea"/>
            </match>
        </league>
        """
        league = ElementTree.fromstring(xml)
        result = TeamFixturesReportGenerator().getMatchElements(league, "IBMSouthHants")
        self.assertEqual(0, len(result))

    def testGetMatchElementsSomeFound(self):
        xml = """
        <league>
            <match>
                <homeTeam id="Corinthians"/>
                <awayTeam id="PortsmouthSouthsea"/>
            </match>
            <match>
                <homeTeam id="Corinthians"/>
                <awayTeam id="IBMSouthHants"/>
            </match>
            <match>
                <homeTeam id="IBMSouthHants"/>
                <awayTeam id="Curdridge"/>
            </match>
            <match>
                <homeTeam id="IBMSouthHants"/>
                <awayTeam id="PortsmouthSouthsea"/>
            </match>
            <match>
                <homeTeam id="Corinthians"/>
                <awayTeam id="PortsmouthSouthsea"/>
            </match>
        </league>
        """
        league = ElementTree.fromstring(xml)
        result = TeamFixturesReportGenerator().getMatchElements(league, "IBMSouthHants")
        self.assertEqual(3, len(result))

    def testSetOpponentInfoTeamIsAtHome(self):
        xml = """
        <match>
            <homeTeam id="IBMSouthHants"/>
            <awayTeam id="PortsmouthB"/>
        </match>
        """
        teamId = "IBMSouthHants"
        generator = TeamFixturesReportGenerator();
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        teams = {"PortsmouthB" : "Portsmouth B"}
        generator.setOpponentInfo(teamId, matchElement, match, teams)
        self.assertTrue(match.home)
        self.assertEqual("PortsmouthB", match.opponentId)
        self.assertEqual("Portsmouth B", match.opponentName)

    def testSetOpponentInfoTeamIsAway(self):
        xml = """
        <match>
            <awayTeam id="IBMSouthHants"/>
            <homeTeam id="PortsmouthB"/>
        </match>
        """
        teamId = "IBMSouthHants"
        generator = TeamFixturesReportGenerator();
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        teams = {"PortsmouthB" : "Portsmouth B"}
        generator.setOpponentInfo(teamId, matchElement, match, teams)
        self.assertFalse(match.home)
        self.assertEqual("PortsmouthB", match.opponentId)
        self.assertEqual("Portsmouth B", match.opponentName)

        
    def testSetWinLossInfoGameAwardedNotPlayedOrAwarded(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGameAwarded(teamId, matchElement, match)
        self.assertFalse(result)
        self.assertEquals(None, match.result)
        self.assertEquals(None, match.margin)

    def testSetWinLossInfoGameAwardedPlayed(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch/>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGameAwarded(teamId, matchElement, match)
        self.assertFalse(result)
        self.assertEquals(None, match.result)
        self.assertEquals(None, match.margin)

    def testSetWinLossInfoGameAwardedAwardedAndWon(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <awardedMatch>
                <winner id="HavantA"/>
            </awardedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGameAwarded(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Won", match.result)
        self.assertEquals("default", match.margin)

    def testSetWinLossInfoGameAwardedAwardedAndLost(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <awardedMatch>
                <winner id="HavantB"/>
            </awardedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGameAwarded(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Lost", match.result)
        self.assertEquals("default", match.margin)

    def testSetWinLossInfoGamePlayedNotPlayedOrAwarded(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertFalse(result)
        self.assertEquals(None, match.result)
        self.assertEquals(None, match.margin)

    def testSetWinLossInfoGamePlayedAwarded(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <awardedMatch/>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertFalse(result)
        self.assertEquals(None, match.result)
        self.assertEquals(None, match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndTied(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>113</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>113</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Tied", match.result)
        self.assertEquals(None, match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndWonBy1Run(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>113</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Won", match.result)
        self.assertEquals("1 run", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndWonByMoreThan1Run(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>114</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Won", match.result)
        self.assertEquals("2 runs", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndLostBy1Run(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>111</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Lost", match.result)
        self.assertEquals("1 run", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndLostByMoreThan1Run(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>114</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>116</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Lost", match.result)
        self.assertEquals("2 runs", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndWonBy1Wicket(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>113</runsScored>
                        <wicketsLost>5</wicketsLost>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Won", match.result)
        self.assertEquals("1 wicket", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndWonByMoreThan1Wicket(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>114</runsScored>
                        <wicketsLost>4</wicketsLost>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Won", match.result)
        self.assertEquals("2 wickets", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndLostBy1Wicket(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>113</runsScored>
                        <wicketsLost>5</wicketsLost>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantB"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Lost", match.result)
        self.assertEquals("1 wicket", match.margin)

    def testSetWinLossInfoGamePlayedPlayedAndLostByMoreThan1Wicket(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>114</runsScored>
                        <wicketsLost>4</wicketsLost>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        teamId = "HavantB"
        generator = TeamFixturesReportGenerator()
        matchElement = ElementTree.fromstring(xml)
        match = MatchInReport()
        match.result = None
        match.margin = None
        result = generator.setWinLossInfoGamePlayed(teamId, matchElement, match)
        self.assertTrue(result)
        self.assertEquals("Lost", match.result)
        self.assertEquals("2 wickets", match.margin)

    def testSetWinLossInfoGameNotPlayedOrAwarded(self):
        xml = """
        <match/>
        """
        matchElement = ElementTree.fromstring(xml)
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        match = MatchInReport()
        match.result = None
        match.margin = None
        generator.setWinLossInfo(teamId, matchElement, match);
        self.assertEquals(None, match.result)
        self.assertEquals(None, match.margin)

    def testSetWinLossInfoGameAwarded(self):
        xml = """
        <match>
            <awardedMatch>
                <winner id="HavantB"/>
            </awardedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        match = MatchInReport()
        match.result = None
        match.margin = None
        generator.setWinLossInfo(teamId, matchElement, match);
        self.assertEquals("Lost", match.result)
        self.assertEquals("default", match.margin)

    def testSetWinLossInfoGamePlayed(self):
        xml = """
        <match>
            <homeTeam id="HavantA"/>
            <awayTeam id="HavantB"/>
            <playedMatch>
                <teamInMatch>
                    <battingFirst>false</battingFirst>
                    <teamRef id="HavantA"/>
                    <innings>
                        <runsScored>104</runsScored>
                        <wicketsLost>4</wicketsLost>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <battingFirst>true</battingFirst>
                    <teamRef id="HavantB"/>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teamId = "HavantA"
        generator = TeamFixturesReportGenerator()
        match = MatchInReport()
        match.result = None
        match.margin = None
        generator.setWinLossInfo(teamId, matchElement, match);
        self.assertEquals("Lost", match.result)
        self.assertEquals("8 runs", match.margin)

    def testGetMatch(self):
        xml = """
        <match>
            <date>2012-10-14.19:15</date>
            <pitch>B</pitch>
            <homeTeam id="LocksHeathB"/>
            <awayTeam id="SarisburyAthleticB"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="LocksHeathB"/>
                    <battingFirst>true</battingFirst>
                    <innings>
                        <runsScored>112</runsScored>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="SarisburyAthleticB"/>
                    <battingFirst>false</battingFirst>
                    <innings>
                        <runsScored>113</runsScored>
                        <wicketsLost>2</wicketsLost>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teamId = "LocksHeathB"
        generator = TeamFixturesReportGenerator()
        teams = {"SarisburyAthleticB": "Sarisbury Athletic B"}
        result = generator.getMatch(matchElement, teamId, teams)
        self.assertEquals(datetime(2012, 10, 14, 19, 15), result.datetime)
        self.assertEquals("B", result.court)
        self.assertEquals("Lost", result.result)
        self.assertEquals("4 wickets", result.margin)
        self.assertEquals("SarisburyAthleticB", result.opponentId)
        self.assertEquals("Sarisbury Athletic B", result.opponentName)
        
    def testGetReportMatchesFound(self):
        xml = """
        <model>
            <league id="d1">
                <name>Division 1</name>
            </league>
            <league id="Division2">
                <name>Division 2</name>
                <team id="IBMSouthHants">
                    <name>IBM South Hants</name>
                </team>
                <team id="LocksHeathA">
                    <name>Locks Heath A</name>
                </team>
                <team id="Corinthians">
                    <name>Corinthians</name>
                </team>
                <match>
                    <homeTeam id="LocksHeathA"/>
                    <awayTeam id="IBMSouthHants"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="IBMSouthHants"/>
                    <awayTeam id="Corinthians"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="Corinthians"/>
                    <awayTeam id="LocksHeathA"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
            </league>
        </model>
        """
        root = ElementTree.fromstring(xml)
        teamId = "LocksHeathA"
        generator = TeamFixturesReportGenerator()
        result = generator.getReport(root, teamId)
        self.assertEquals(2, len(result.matches))
        self.assertEquals("LocksHeathA", result.teamId)
        self.assertEquals("Locks Heath A", result.teamName)
        self.assertEquals("Division2", result.leagueId)
        self.assertEquals("Division 2", result.leagueName)
        
    def testGetReportNoMatchesFound(self):
        xml = """
        <model>
            <league id="d1">
                <name>Division 1</name>
            </league>
            <league id="Division2">
                <name>Division 2</name>
                <team id="IBMSouthHants">
                    <name>IBM South Hants</name>
                </team>
                <team id="LocksHeathA">
                    <name>Locks Heath A</name>
                </team>
                <team id="Corinthians">
                    <name>Corinthians</name>
                </team>
                <team id="Curdridge">
                    <name>Curdridge</name>
                </team>
                <match>
                    <homeTeam id="LocksHeathA"/>
                    <awayTeam id="IBMSouthHants"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="IBMSouthHants"/>
                    <awayTeam id="Corinthians"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="Corinthians"/>
                    <awayTeam id="LocksHeathA"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
            </league>
        </model>
        """
        root = ElementTree.fromstring(xml)
        teamId = "Curdridge"
        generator = TeamFixturesReportGenerator()
        result = generator.getReport(root, teamId)
        self.assertEquals(0, len(result.matches))
        self.assertEquals("Curdridge", result.teamId)
        self.assertEquals("Curdridge", result.teamName)
        self.assertEquals("Division2", result.leagueId)
        self.assertEquals("Division 2", result.leagueName)
        
    def testGetSortedMatches(self):
        xml = """
        <model>
            <league id="d1">
                <name>Division 1</name>
            </league>
            <league id="Division2">
                <name>Division 2</name>
                <team id="IBMSouthHants">
                    <name>IBM South Hants</name>
                </team>
                <team id="LocksHeathA">
                    <name>Locks Heath A</name>
                </team>
                <team id="Corinthians">
                    <name>Corinthians</name>
                </team>
                <team id="Curdridge">
                    <name>Curdridge</name>
                </team>
                <team id="Denmead">
                    <name>Denmead</name>
                </team>
                <match>
                    <homeTeam id="LocksHeathA"/>
                    <awayTeam id="IBMSouthHants"/>
                    <date>2013-03-04.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="Denmead"/>
                    <awayTeam id="LocksHeathA"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="LocksHeathA"/>
                    <awayTeam id="Curdridge"/>
                    <date>2013-03-03.18:15</date>
                    <pitch>A</pitch>
                </match>
                <match>
                    <homeTeam id="Corinthians"/>
                    <awayTeam id="LocksHeathA"/>
                    <date>2013-03-12.18:15</date>
                    <pitch>A</pitch>
                </match>
            </league>
        </model>
        """
        root = ElementTree.fromstring(xml)
        teamId = "LocksHeathA"
        generator = TeamFixturesReportGenerator()
        report = generator.getReport(root, teamId)
        result = report.getSortedMatches()
        expectedOpponents = ["Curdridge", "Denmead", "IBM South Hants", "Corinthians"]
        for e, a in zip(expectedOpponents, result):
            self.assertEquals(e, a.opponentName)
        self.assertEquals(len(expectedOpponents), len(result))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()