'''
Created on 16 Aug 2013

@author: hicksj
'''
import unittest
from reports.averagesreport import BowlerInReport, BatsmanInReport,\
    AveragesReportGenerator
from xml.etree import ElementTree
import string
import datetime
from operator import itemgetter

class Test(unittest.TestCase):

    def getTestXml(self, leagueCount, teamCount, playerCount):
        et = "<{elem} {attrs}>{body}</{elem}>"
        at = "{0}=\"{1}\""
        leagueElems = []
        for l in range(1, leagueCount + 1):
            lId = "{0}".format(l)
            lName = "League {0}".format(lId)
            nameElem = et.format(elem="name", attrs="", body=lName)
            lIdAttr = at.format("id", "l{0}".format(lId))
            lSubElems = [nameElem]
            for t in range(1, teamCount + 1):
                tId = "{0}{1}".format(l, t)
                tName = "Team {0}".format(tId)
                nameElem = et.format(elem="name", attrs="", body=tName)
                tIdAttr = at.format("id", "t{0}".format(tId))
                tSubElems = [nameElem]
                for p in range(1, playerCount + 1):
                    pId = "{0}{1}{2}".format(l, t, p)
                    pName = "Player {0}".format(pId)
                    nameElem = et.format(elem="name", attrs="", body=pName)
                    pIdAttr = at.format("id", "p{0}".format(pId))
                    tSubElems.append(et.format(elem="player", attrs=pIdAttr, body=nameElem))
                lSubElems.append(et.format(elem="team", attrs=tIdAttr, body=string.join(tSubElems, "\n")))
            leagueElems.append(et.format(elem="league", attrs=lIdAttr, body=string.join(lSubElems, "\n")))
        answer = et.format(elem="model", attrs="", body=string.join(leagueElems, "\n"))
        return answer

    def testGetLeaguesTeamsAndPlayersLeaguesNotSpecifiedTeamNotSpecified(self):
        xml = self.getTestXml(3, 3, 3)
        rootElement = ElementTree.fromstring(xml)
        leagues, teams, players = AveragesReportGenerator().getLeaguesTeamsAndPlayers(rootElement)
        self.assertEquals({}, leagues)
        self.assertEquals({}, teams)
        self.assertEquals({}, players)

    def testGetLeaguesTeamsAndPlayersLeaguesSpecifiedTeamNotSpecified(self):
        xml = self.getTestXml(3, 3, 3)
        rootElement = ElementTree.fromstring(xml)
        leagues, teams, players = AveragesReportGenerator().getLeaguesTeamsAndPlayers(rootElement, leagueIds=("l1", "l3"))
        self.assertEquals({"l1": "League 1", "l3": "League 3"}, leagues)
        expectedTeams = {}
        expectedTeams["t11"] = "Team 11"
        expectedTeams["t12"] = "Team 12"
        expectedTeams["t13"] = "Team 13"
        expectedTeams["t31"] = "Team 31"
        expectedTeams["t32"] = "Team 32"
        expectedTeams["t33"] = "Team 33"
        self.assertEquals(expectedTeams, teams)
        expectedPlayers = {}
        expectedPlayers["p111"] = "Player 111"
        expectedPlayers["p112"] = "Player 112"
        expectedPlayers["p113"] = "Player 113"
        expectedPlayers["p121"] = "Player 121"
        expectedPlayers["p122"] = "Player 122"
        expectedPlayers["p123"] = "Player 123"
        expectedPlayers["p131"] = "Player 131"
        expectedPlayers["p132"] = "Player 132"
        expectedPlayers["p133"] = "Player 133"
        expectedPlayers["p311"] = "Player 311"
        expectedPlayers["p312"] = "Player 312"
        expectedPlayers["p313"] = "Player 313"
        expectedPlayers["p321"] = "Player 321"
        expectedPlayers["p322"] = "Player 322"
        expectedPlayers["p323"] = "Player 323"
        expectedPlayers["p331"] = "Player 331"
        expectedPlayers["p332"] = "Player 332"
        expectedPlayers["p333"] = "Player 333"
        self.assertEquals(expectedPlayers, players)

    def testGetLeaguesTeamsAndPlayersLeaguesNotSpecifiedTeamSpecified(self):
        xml = self.getTestXml(3, 3, 3)
        rootElement = ElementTree.fromstring(xml)
        leagues, teams, players = AveragesReportGenerator().getLeaguesTeamsAndPlayers(rootElement, teamId="t23")
        self.assertEquals({"l2": "League 2"}, leagues)
        expectedTeams = {"t23": "Team 23"}
        self.assertEquals(expectedTeams, teams)
        expectedPlayers = {}
        expectedPlayers["p231"] = "Player 231"
        expectedPlayers["p232"] = "Player 232"
        expectedPlayers["p233"] = "Player 233"
        self.assertEquals(expectedPlayers, players)

    def testGetLeaguesTeamsAndPlayersLeaguesSpecifiedTeamSpecified(self):
        xml = self.getTestXml(3, 3, 3)
        rootElement = ElementTree.fromstring(xml)
        leagues, teams, players = AveragesReportGenerator().getLeaguesTeamsAndPlayers(rootElement, leagueIds=["l1", "l2"], teamId="t23")
        self.assertEquals({}, leagues)
        self.assertEquals({}, teams)
        self.assertEquals({}, players)

    def testUpdateBowlingAveragesFromPerformanceBowlerNotAlreadyThere(self):
        xml = """
            <bowler player="p1">
                <ballsBowled>13</ballsBowled>
                <runs>22</runs>
                <wickets>0</wickets>
            </bowler>
        """
        bowlerElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "My Team"}
        players = {"p1": "Mr Player"}
        bowlingAverages = {}
        AveragesReportGenerator().updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)
        self.assertEquals(1, len(bowlingAverages))
        details = bowlingAverages["p1"]
        self.assertEquals("t1", details.teamId)
        self.assertEquals("My Team", details.teamName)
        self.assertEquals("p1", details.playerId)
        self.assertEquals("Mr Player", details.playerName)
        self.assertEquals(13, details.balls)
        self.assertEquals(22, details.runs)
        self.assertEquals(0, details.wickets)
        self.assertEquals(13, details.bestBalls)
        self.assertEquals(22, details.bestRuns)
        self.assertEquals(0, details.bestWickets)
        self.assertEquals(-1, details.averagePerWicket)
        self.assertAlmostEquals(10.153846153846153, details.averagePerOver, 15)
        self.assertEquals("9921.153846153846153PlayerMr", details.sortKey)

    def testUpdateBowlingAveragesFromPerformanceBowlerAlreadyThereWithBetterPerformanceOnWickets(self):
        xml = """
            <bowler player="p1">
                <ballsBowled>13</ballsBowled>
                <runs>22</runs>
                <wickets>0</wickets>
            </bowler>
        """
        bowlerElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {}
        players = {}
        bowler = BowlerInReport("asasa", "asdgasg", "asdgsda", "dgdasg")
        bowler.balls, bowler.runs, bowler.wickets = (42, 55, 3)
        bowler.bestBalls, bowler.bestRuns, bowler.bestWickets = (11, 2, 1)
        bowlingAverages = {"p1": bowler}
        AveragesReportGenerator().updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)
        self.assertEquals(1, len(bowlingAverages))
        details = bowlingAverages["p1"]
        self.assertTrue(details is bowler)
        self.assertEquals(55, details.balls)
        self.assertEquals(77, details.runs)
        self.assertEquals(3, details.wickets)
        self.assertEquals(11, details.bestBalls)
        self.assertEquals(2, details.bestRuns)
        self.assertEquals(1, details.bestWickets)
        self.assertAlmostEquals(25.666666666666667, details.averagePerWicket, 15)
        self.assertAlmostEquals(8.4, details.averagePerOver, 15)
        self.assertEquals("9619.399999999999999asdgasg", details.sortKey)

    def testUpdateBowlingAveragesFromPerformanceBowlerAlreadyThereWithBetterPerformanceOnRate(self):
        xml = """
            <bowler player="p1">
                <ballsBowled>13</ballsBowled>
                <runs>22</runs>
                <wickets>1</wickets>
            </bowler>
        """
        bowlerElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {}
        players = {}
        bowler = BowlerInReport("asasa", "asdgasg", "asdgsda", "dgdasg")
        bowler.balls, bowler.runs, bowler.wickets = (42, 55, 3)
        bowler.bestBalls, bowler.bestRuns, bowler.bestWickets = (12, 22, 1)
        bowlingAverages = {"p1": bowler}
        AveragesReportGenerator().updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)
        self.assertEquals(1, len(bowlingAverages))
        details = bowlingAverages["p1"]
        self.assertTrue(details is bowler)
        self.assertEquals(55, details.balls)
        self.assertEquals(77, details.runs)
        self.assertEquals(4, details.wickets)
        self.assertEquals(13, details.bestBalls)
        self.assertEquals(22, details.bestRuns)
        self.assertEquals(1, details.bestWickets)
        self.assertAlmostEquals(19.25, details.averagePerWicket, 15)
        self.assertAlmostEquals(8.4, details.averagePerOver, 15)
        self.assertEquals("9519.399999999999999asdgasg", details.sortKey)

    def testUpdateBowlingAveragesFromPerformanceBowlerAlreadyThereWithWorsePerformanceOnWickets(self):
        xml = """
            <bowler player="p1">
                <ballsBowled>13</ballsBowled>
                <runs>22</runs>
                <wickets>1</wickets>
            </bowler>
        """
        bowlerElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {}
        players = {}
        bowler = BowlerInReport("asasa", "asdgasg", "asdgsda", "dgdasg")
        bowler.balls, bowler.runs, bowler.wickets = (42, 55, 0)
        bowler.bestBalls, bowler.bestRuns, bowler.bestWickets = (12, 22, 0)
        bowlingAverages = {"p1": bowler}
        AveragesReportGenerator().updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)
        self.assertEquals(1, len(bowlingAverages))
        details = bowlingAverages["p1"]
        self.assertTrue(details is bowler)
        self.assertEquals(55, details.balls)
        self.assertEquals(77, details.runs)
        self.assertEquals(1, details.wickets)
        self.assertEquals(13, details.bestBalls)
        self.assertEquals(22, details.bestRuns)
        self.assertEquals(1, details.bestWickets)
        self.assertAlmostEquals(77, details.averagePerWicket, 15)
        self.assertAlmostEquals(8.4, details.averagePerOver, 15)
        self.assertEquals("9819.399999999999999asdgasg", details.sortKey)

    def testUpdateBowlingAveragesFromPerformanceBowlerAlreadyThereWithWorsePerformanceOnRate(self):
        xml = """
            <bowler player="p1">
                <ballsBowled>13</ballsBowled>
                <runs>22</runs>
                <wickets>1</wickets>
            </bowler>
        """
        bowlerElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {}
        players = {}
        bowler = BowlerInReport("asasa", "asdgasg", "asdgsda", "dgdasg")
        bowler.balls, bowler.runs, bowler.wickets = (42, 55, 1)
        bowler.bestBalls, bowler.bestRuns, bowler.bestWickets = (14, 22, 1)
        bowlingAverages = {"p1": bowler}
        AveragesReportGenerator().updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)
        self.assertEquals(1, len(bowlingAverages))
        details = bowlingAverages["p1"]
        self.assertTrue(details is bowler)
        self.assertEquals(55, details.balls)
        self.assertEquals(77, details.runs)
        self.assertEquals(2, details.wickets)
        self.assertEquals(13, details.bestBalls)
        self.assertEquals(22, details.bestRuns)
        self.assertEquals(1, details.bestWickets)
        self.assertAlmostEquals(38.5, details.averagePerWicket, 15)
        self.assertAlmostEquals(8.4, details.averagePerOver, 15)
        self.assertEquals("9719.399999999999999asdgasg", details.sortKey)

    def testUpdateBowlingAveragesFromPerformanceNoBallsBowled(self):
        xml = """
            <bowler player="p1">
                <ballsBowled>0</ballsBowled>
                <runs>2</runs>
                <wickets>0</wickets>
            </bowler>
        """
        bowlerElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "My Team"}
        players = {"p1": "Mr Player"}
        bowlingAverages = {}
        AveragesReportGenerator().updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)
        self.assertEquals(1, len(bowlingAverages))
        details = bowlingAverages["p1"]
        self.assertEquals(0, details.balls)
        self.assertEquals(2, details.runs)
        self.assertEquals(0, details.wickets)
        self.assertEquals(0, details.bestBalls)
        self.assertEquals(2, details.bestRuns)
        self.assertEquals(0, details.bestWickets)
        self.assertAlmostEquals(-1, details.averagePerWicket, 15)
        self.assertAlmostEquals(-1, details.averagePerOver, 15)
        self.assertEquals("9910.000000000000000PlayerMr", details.sortKey)
        
    def testUpdateBowlingAveragesFromMatchBothTeamsRelevant(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <innings>
                    <bowler player="p1">
                        <ballsBowled>18</ballsBowled>
                        <runs>13</runs>
                        <wickets>4</wickets>
                    </bowler>
                    <bowler player="p2">
                        <ballsBowled>18</ballsBowled>
                        <runs>44</runs>
                        <wickets>0</wickets>
                    </bowler>
                    <bowler player="p3">
                        <ballsBowled>18</ballsBowled>
                        <runs>21</runs>
                        <wickets>1</wickets>
                    </bowler>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <bowler player="p4">
                        <ballsBowled>18</ballsBowled>
                        <runs>22</runs>
                        <wickets>1</wickets>
                    </bowler>
                    <bowler player="p5">
                        <ballsBowled>18</ballsBowled>
                        <runs>14</runs>
                        <wickets>3</wickets>
                    </bowler>
                    <bowler player="p6">
                        <ballsBowled>16</ballsBowled>
                        <runs>32</runs>
                        <wickets>0</wickets>
                    </bowler>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        teams = {}
        for t in range(1, 3):
            teams["t{0}".format(t)] = "Team {0}".format(t)
        players = {}
        for p in range(1, 7):
            players["p{0}".format(p)] = "Player {0}".format(p)
        bowlingAverages = {}
        AveragesReportGenerator().updateBowlingAveragesFromMatch(playedMatchElement, teams, players, bowlingAverages)
        self.assertEquals(6, len(bowlingAverages))

    def testUpdateBowlingAveragesFromMatchOnlyOneTeamRelevant(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <innings>
                    <bowler player="p1">
                        <ballsBowled>18</ballsBowled>
                        <runs>13</runs>
                        <wickets>4</wickets>
                    </bowler>
                    <bowler player="p2">
                        <ballsBowled>18</ballsBowled>
                        <runs>44</runs>
                        <wickets>0</wickets>
                    </bowler>
                    <bowler player="p3">
                        <ballsBowled>18</ballsBowled>
                        <runs>21</runs>
                        <wickets>1</wickets>
                    </bowler>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <bowler player="p4">
                        <ballsBowled>18</ballsBowled>
                        <runs>22</runs>
                        <wickets>1</wickets>
                    </bowler>
                    <bowler player="p5">
                        <ballsBowled>18</ballsBowled>
                        <runs>14</runs>
                        <wickets>3</wickets>
                    </bowler>
                    <bowler player="p6">
                        <ballsBowled>16</ballsBowled>
                        <runs>32</runs>
                        <wickets>0</wickets>
                    </bowler>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        teams = {}
        for t in range(2, 3):
            teams["t{0}".format(t)] = "Team {0}".format(t)
        players = {}
        for p in range(1, 4):
            players["p{0}".format(p)] = "Player {0}".format(p)
        bowlingAverages = {}
        AveragesReportGenerator().updateBowlingAveragesFromMatch(playedMatchElement, teams, players, bowlingAverages)
        self.assertEquals(3, len(bowlingAverages))
        
    def testUpdateBattingAveragesFromPerformanceBatsmanNotFound(self):
        xml = """
        <batsman player="p1">
            <runs>32</runs>
            <out>false</out>
        </batsman>
        """
        batsmanElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "Team 1"}
        players = {"p1": "J Hicks"}
        battingAverages = {}
        AveragesReportGenerator().updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)
        self.assertEquals(1, len(battingAverages))
        details = battingAverages["p1"]
        self.assertEquals("t1", details.teamId)
        self.assertEquals("Team 1", details.teamName)
        self.assertEquals("p1", details.playerId)
        self.assertEquals("J Hicks", details.playerName)
        self.assertEquals(1, details.innings)
        self.assertEquals(32, details.runs)
        self.assertEquals(1, details.notout)
        self.assertEquals(32, details.highScore)
        self.assertEquals(False, details.highScoreOut)
        self.assertEquals(-1, details.average)
        self.assertEquals("967HicksJ", details.sortKey)

    def testUpdateBattingAveragesFromPerformanceBatsmanFoundWithBetterHighScore(self):
        xml = """
        <batsman player="p1">
            <runs>32</runs>
            <out>false</out>
        </batsman>
        """
        batsmanElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "Team 1"}
        players = {"p1": "J Hicks"}
        batsman = BatsmanInReport("p1", "J Hicks", "t1", "Team 1")
        batsman.runs, batsman.innings, batsman.notout = (68, 4, 2)
        batsman.highScore, batsman.highScoreOut = (42, True)
        battingAverages = {"p1": batsman}
        AveragesReportGenerator().updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)
        self.assertEquals(1, len(battingAverages))
        details = battingAverages["p1"]
        self.assertTrue(details is batsman)
        self.assertEquals(5, details.innings)
        self.assertEquals(100, details.runs)
        self.assertEquals(3, details.notout)
        self.assertEquals(42, details.highScore)
        self.assertEquals(True, details.highScoreOut)
        self.assertEquals(50, details.average)
        self.assertEquals("899HicksJ", details.sortKey)

    def testUpdateBattingAveragesFromPerformanceBatsmanFoundWithLowerHighScore(self):
        xml = """
        <batsman player="p1">
            <runs>32</runs>
            <out>false</out>
        </batsman>
        """
        batsmanElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "Team 1"}
        players = {"p1": "J Hicks"}
        batsman = BatsmanInReport("p1", "J Hicks", "t1", "Team 1")
        batsman.runs, batsman.innings, batsman.notout = (68, 4, 1)
        batsman.highScore, batsman.highScoreOut = (31, True)
        battingAverages = {"p1": batsman}
        AveragesReportGenerator().updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)
        self.assertEquals(1, len(battingAverages))
        details = battingAverages["p1"]
        self.assertTrue(details is batsman)
        self.assertEquals(5, details.innings)
        self.assertEquals(100, details.runs)
        self.assertEquals(2, details.notout)
        self.assertEquals(32, details.highScore)
        self.assertEquals(False, details.highScoreOut)
        self.assertAlmostEquals(33.333333333333333, details.average, 15)
        self.assertEquals("899HicksJ", details.sortKey)

    def testUpdateBattingAveragesFromPerformanceBatsmanFoundWithSameHighScoreBothOut(self):
        xml = """
        <batsman player="p1">
            <runs>32</runs>
            <out>true</out>
        </batsman>
        """
        batsmanElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "Team 1"}
        players = {"p1": "J Hicks"}
        batsman = BatsmanInReport("p1", "J Hicks", "t1", "Team 1")
        batsman.runs, batsman.innings, batsman.notout = (68, 4, 3)
        batsman.highScore, batsman.highScoreOut = (32, True)
        battingAverages = {"p1": batsman}
        AveragesReportGenerator().updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)
        self.assertEquals(1, len(battingAverages))
        details = battingAverages["p1"]
        self.assertTrue(details is batsman)
        self.assertEquals(5, details.innings)
        self.assertEquals(100, details.runs)
        self.assertEquals(3, details.notout)
        self.assertEquals(32, details.highScore)
        self.assertEquals(True, details.highScoreOut)
        self.assertAlmostEquals(50, details.average, 15)
        self.assertEquals("899HicksJ", details.sortKey)

    def testUpdateBattingAveragesFromPerformanceBatsmanFoundWithSameHighScoreBothNotOut(self):
        xml = """
        <batsman player="p1">
            <runs>32</runs>
            <out>false</out>
        </batsman>
        """
        batsmanElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "Team 1"}
        players = {"p1": "J Hicks"}
        batsman = BatsmanInReport("p1", "J Hicks", "t1", "Team 1")
        batsman.runs, batsman.innings, batsman.notout = (68, 4, 2)
        batsman.highScore, batsman.highScoreOut = (32, False)
        battingAverages = {"p1": batsman}
        AveragesReportGenerator().updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)
        self.assertEquals(1, len(battingAverages))
        details = battingAverages["p1"]
        self.assertTrue(details is batsman)
        self.assertEquals(5, details.innings)
        self.assertEquals(100, details.runs)
        self.assertEquals(3, details.notout)
        self.assertEquals(32, details.highScore)
        self.assertEquals(False, details.highScoreOut)
        self.assertAlmostEquals(50, details.average, 15)
        self.assertEquals("899HicksJ", details.sortKey)

    def testUpdateBattingAveragesFromPerformanceBatsmanFoundWithSameHighScoreOneOutOneNotOut(self):
        xml = """
        <batsman player="p1">
            <runs>32</runs>
            <out>false</out>
        </batsman>
        """
        batsmanElement = ElementTree.fromstring(xml)
        teamId = "t1"
        teams = {"t1": "Team 1"}
        players = {"p1": "J Hicks"}
        batsman = BatsmanInReport("p1", "J Hicks", "t1", "Team 1")
        batsman.runs, batsman.innings, batsman.notout = (68, 4, 2)
        batsman.highScore, batsman.highScoreOut = (32, True)
        battingAverages = {"p1": batsman}
        AveragesReportGenerator().updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)
        self.assertEquals(1, len(battingAverages))
        details = battingAverages["p1"]
        self.assertTrue(details is batsman)
        self.assertEquals(5, details.innings)
        self.assertEquals(100, details.runs)
        self.assertEquals(3, details.notout)
        self.assertEquals(32, details.highScore)
        self.assertEquals(False, details.highScoreOut)
        self.assertAlmostEquals(50, details.average, 15)
        self.assertEquals("899HicksJ", details.sortKey)

    def testUpdateBattingAveragesFromMatchBothTeamsRelevant(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <innings>
                    <batsman player="p1">
                        <runs>13</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p2">
                        <runs>44</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p3">
                        <runs>21</runs>
                        <out>true</out>
                    </batsman>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <batsman player="p4">
                        <runs>22</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p5">
                        <runs>14</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p6">
                        <runs>32</runs>
                        <out>true</out>
                    </batsman>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        teams = {}
        for t in range(1, 3):
            teams["t{0}".format(t)] = "Team {0}".format(t)
        players = {}
        for p in range(1, 7):
            players["p{0}".format(p)] = "Player {0}".format(p)
        battingAverages = {}
        AveragesReportGenerator().updateBattingAveragesFromMatch(playedMatchElement, teams, players, battingAverages)
        self.assertEquals(6, len(battingAverages))

    def testUpdateBattingAveragesFromMatchOneTeamRelevant(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <innings>
                    <batsman player="p1">
                        <runs>13</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p2">
                        <runs>44</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p3">
                        <runs>21</runs>
                        <out>true</out>
                    </batsman>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <innings>
                    <batsman player="p4">
                        <runs>22</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p5">
                        <runs>14</runs>
                        <out>true</out>
                    </batsman>
                    <batsman player="p6">
                        <runs>32</runs>
                        <out>true</out>
                    </batsman>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        teams = {}
        for t in range(2, 3):
            teams["t{0}".format(t)] = "Team {0}".format(t)
        players = {}
        for p in range(4, 7):
            players["p{0}".format(p)] = "Player {0}".format(p)
        battingAverages = {}
        AveragesReportGenerator().updateBattingAveragesFromMatch(playedMatchElement, teams, players, battingAverages)
        self.assertEquals(3, len(battingAverages))

    def testUpdateAveragesFromMatchNotPlayed(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {}
        players = {}
        battingAverages = {}
        bowlingAverages = {}
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(0, len(battingAverages))
        self.assertEquals(0, len(bowlingAverages))
        
    def testUpdateAveragesFromMatchPlayedButNeitherTeamRelevant(self):
        xml = """
        <match>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch/>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {}
        players = {}
        battingAverages = {}
        bowlingAverages = {}
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(0, len(battingAverages))
        self.assertEquals(0, len(bowlingAverages))
        
    def testUpdateAveragesFromMatchPlayedOnlyHomeTeamRelevant(self):
        xml = """
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {"t1": "Team 1"}
        players = {"p1": "Player 1"}
        battingAverages = {}
        bowlingAverages = {}
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(1, len(battingAverages))
        self.assertEquals(1, len(bowlingAverages))

    def testUpdateAveragesFromMatchPlayedOnlyAwayTeamRelevant(self):
        xml = """
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {"t2": "Team 2"}
        players = {"p2": "Player 2"}
        battingAverages = {}
        bowlingAverages = {}
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(1, len(battingAverages))
        self.assertEquals(1, len(bowlingAverages))
        
    def testUpdateAveragesFromMatchPlayedBothTeamsRelevantBowlingAndBattingRequired(self):
        xml = """
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {"t1": "Team 1", "t2": "Team 2"}
        players = {"p1": "Player 1", "p2": "Player 2"}
        battingAverages = {}
        bowlingAverages = {}
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(2, len(battingAverages))
        self.assertEquals(2, len(bowlingAverages))
        
    def testUpdateAveragesFromMatchPlayedBothTeamsRelevantBowlingOnlyRequired(self):
        xml = """
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {"t1": "Team 1", "t2": "Team 2"}
        players = {"p1": "Player 1", "p2": "Player 2"}
        battingAverages = None
        bowlingAverages = {}
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(None, battingAverages)
        self.assertEquals(2, len(bowlingAverages))
        
    def testUpdateAveragesFromMatchPlayedBothTeamsRelevantBattingOnlyRequired(self):
        xml = """
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        teams = {"t1": "Team 1", "t2": "Team 2"}
        players = {"p1": "Player 1", "p2": "Player 2"}
        battingAverages = {}
        bowlingAverages = None
        AveragesReportGenerator().updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
        self.assertEquals(2, len(battingAverages))
        self.assertEquals(None, bowlingAverages)
        
    def testGetAveragesAllLeaguesRelevantBattingAndBowlingRequired(self):
        xml = """
        <model>
        <league id="l1">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        <league id="l2">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t3"/>
            <awayTeam id="t4"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t3"/>
                    <innings>
                        <batsman player="p3">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p4">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t4"/>
                    <innings>
                        <batsman player="p4">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p3">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        leagues = {"l1": "League 1", "l2": "League 2"}
        teams = {"t1": "Team 1", "t2": "Team 2", "t3": "Team 3", "t4": "Team 4"}
        players = {"p1": "Player 1", "p2": "Player 2", "p3": "Player 3", "p4": "Player 4"}
        batting = True
        bowling = True
        generator = AveragesReportGenerator()
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(4, len(result.bowlingAverages))
        self.assertEquals(4, len(result.bowlingAverages))
        
    def testGetAveragesOneLeagueRelevantBattingAndBowlingRequired(self):
        xml = """
        <model>
        <league id="l1">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        <league id="l2">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t3"/>
            <awayTeam id="t4"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t3"/>
                    <innings>
                        <batsman player="p3">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p4">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t4"/>
                    <innings>
                        <batsman player="p4">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p3">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        leagues = {"l2": "League 2"}
        teams = {"t3": "Team 3", "t4": "Team 4"}
        players = {"p3": "Player 3", "p4": "Player 4"}
        batting = True
        bowling = True
        generator = AveragesReportGenerator()
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(2, len(result.bowlingAverages))
        self.assertEquals(2, len(result.bowlingAverages))
        
    def testGetAveragesAllLeaguesRelevantBattingOnlyRequired(self):
        xml = """
        <model>
        <league id="l1">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        <league id="l2">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t3"/>
            <awayTeam id="t4"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t3"/>
                    <innings>
                        <batsman player="p3">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p4">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t4"/>
                    <innings>
                        <batsman player="p4">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p3">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        leagues = {"l1": "League 1", "l2": "League 2"}
        teams = {"t1": "Team 1", "t2": "Team 2", "t3": "Team 3", "t4": "Team 4"}
        players = {"p1": "Player 1", "p2": "Player 2", "p3": "Player 3", "p4": "Player 4"}
        batting = True
        bowling = False
        generator = AveragesReportGenerator()
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(4, len(result.battingAverages))
        
    def testGetAveragesOneLeagueRelevantBattingOnlyRequired(self):
        xml = """
        <model>
        <league id="l1">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        <league id="l2">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t3"/>
            <awayTeam id="t4"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t3"/>
                    <innings>
                        <batsman player="p3">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p4">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t4"/>
                    <innings>
                        <batsman player="p4">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p3">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        leagues = {"l2": "League 2"}
        teams = {"t3": "Team 3", "t4": "Team 4"}
        players = {"p3": "Player 3", "p4": "Player 4"}
        batting = True
        bowling = False
        generator = AveragesReportGenerator()
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(2, len(result.battingAverages))
        
    def testGetAveragesAllLeaguesRelevantBowlingOnlyRequired(self):
        xml = """
        <model>
        <league id="l1">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        <league id="l2">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t3"/>
            <awayTeam id="t4"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t3"/>
                    <innings>
                        <batsman player="p3">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p4">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t4"/>
                    <innings>
                        <batsman player="p4">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p3">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        leagues = {"l1": "League 1", "l2": "League 2"}
        teams = {"t1": "Team 1", "t2": "Team 2", "t3": "Team 3", "t4": "Team 4"}
        players = {"p1": "Player 1", "p2": "Player 2", "p3": "Player 3", "p4": "Player 4"}
        batting = False
        bowling = True
        generator = AveragesReportGenerator()
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(4, len(result.bowlingAverages))
        
    def testGetAveragesOneLeagueRelevantBowlingOnlyRequired(self):
        xml = """
        <model>
        <league id="l1">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t1"/>
            <awayTeam id="t2"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t1"/>
                    <innings>
                        <batsman player="p1">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p2">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t2"/>
                    <innings>
                        <batsman player="p2">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p1">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        <league id="l2">
        <match>
            <date>2013-08-13.15:15</date>
            <homeTeam id="t3"/>
            <awayTeam id="t4"/>
            <playedMatch>
                <teamInMatch>
                    <teamRef id="t3"/>
                    <innings>
                        <batsman player="p3">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p4">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="t4"/>
                    <innings>
                        <batsman player="p4">
                            <runs>4</runs>
                            <out>true</out>
                        </batsman>
                        <bowler player="p3">
                            <ballsBowled>4</ballsBowled>
                            <runs>44</runs>
                            <wickets>3</wickets>
                        </bowler>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        leagues = {"l2": "League 2"}
        teams = {"t3": "Team 3", "t4": "Team 4"}
        players = {"p3": "Player 3", "p4": "Player 4"}
        batting = False
        bowling = True
        generator = AveragesReportGenerator()
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(2, len(result.bowlingAverages))

    def testGetAveragesNoRelevantMatchesPlayed(self):
        xml = """
        <model>
            <league id="l1">
                <match>
                    <date>2013-08-13.15:15</date>
                    <homeTeam id="t1"/>
                    <awayTeam id="t2"/>
                </match>
                <match>
                    <date>2013-08-13.15:15</date>
                    <homeTeam id="t3"/>
                    <awayTeam id="t4"/>
                    <awardedMatch/>
                </match>
                <match>
                    <date>2013-08-18.15:15</date>
                    <homeTeam id="t3"/>
                    <awayTeam id="t1"/>
                </match>
                <match>
                    <date>2013-08-18.15:15</date>
                    <homeTeam id="t4"/>
                    <awayTeam id="t2"/>
                </match>
                <match>
                    <date>2013-08-23.15:15</date>
                    <homeTeam id="t1"/>
                    <awayTeam id="t4"/>
                </match>
                <match>
                    <date>2013-08-23.15:15</date>
                    <homeTeam id="t2"/>
                    <awayTeam id="t3"/>
                </match>
            </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        generator = AveragesReportGenerator()
        leagues = {"l1": "League 1"}
        teams = {"t1": "Team 1", "t2": "Team 2"}
        players = {}
        batting = True
        bowling = True
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(result.lastCompleteMatchDate, None)
        self.assertEquals(result.lastScheduledMatchDate, datetime.date(2013, 8, 23))
        
    def testGetAveragesSomeRelevantMatchesPlayed(self):
        xml = """
        <model>
            <league id="l1">
                <match>
                    <date>2013-08-13.15:15</date>
                    <homeTeam id="t1"/>
                    <awayTeam id="t2"/>
                    <playedMatch>
                        <teamInMatch>
                            <teamRef id="t1"/>
                            <innings/>
                        </teamInMatch>
                        <teamInMatch>
                            <teamRef id="t2"/>
                            <innings/>
                        </teamInMatch>
                    </playedMatch>
                </match>
                <match>
                    <date>2013-08-13.15:15</date>
                    <homeTeam id="t3"/>
                    <awayTeam id="t4"/>
                </match>
                <match>
                    <date>2013-08-18.15:15</date>
                    <homeTeam id="t3"/>
                    <awayTeam id="t1"/>
                    <awardedMatch/>
                </match>
                <match>
                    <date>2013-08-18.15:15</date>
                    <homeTeam id="t4"/>
                    <awayTeam id="t2"/>
                </match>
                <match>
                    <date>2013-08-23.15:15</date>
                    <homeTeam id="t1"/>
                    <awayTeam id="t4"/>
                </match>
                <match>
                    <date>2013-08-23.15:15</date>
                    <homeTeam id="t2"/>
                    <awayTeam id="t3"/>
                </match>
            </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        generator = AveragesReportGenerator()
        leagues = {"l1": "League 1"}
        teams = {"t1": "Team 1", "t2": "Team 2"}
        players = {}
        batting = True
        bowling = True
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(result.lastCompleteMatchDate, datetime.date(2013, 8, 18))
        self.assertEquals(result.lastScheduledMatchDate, datetime.date(2013, 8, 23))
        self.assertEquals(1, result.toCome)
        
    def testGetAveragesAllRelevantMatchesPlayed(self):
        xml = """
        <model>
            <league id="l1">
                <match>
                    <date>2013-08-13.15:15</date>
                    <homeTeam id="t1"/>
                    <awayTeam id="t2"/>
                    <playedMatch>
                        <teamInMatch>
                            <teamRef id="t1"/>
                            <innings/>
                        </teamInMatch>
                        <teamInMatch>
                            <teamRef id="t2"/>
                            <innings/>
                        </teamInMatch>
                    </playedMatch>
                </match>
                <match>
                    <date>2013-08-13.15:15</date>
                    <homeTeam id="t3"/>
                    <awayTeam id="t4"/>
                </match>
                <match>
                    <date>2013-08-18.15:15</date>
                    <homeTeam id="t3"/>
                    <awayTeam id="t1"/>
                    <awardedMatch/>
                </match>
                <match>
                    <date>2013-08-18.15:15</date>
                    <homeTeam id="t4"/>
                    <awayTeam id="t2"/>
                    <playedMatch>
                        <teamInMatch>
                            <teamRef id="t4"/>
                            <innings/>
                        </teamInMatch>
                        <teamInMatch>
                            <teamRef id="t2"/>
                            <innings/>
                        </teamInMatch>
                    </playedMatch>
                </match>
                <match>
                    <date>2013-08-23.15:15</date>
                    <homeTeam id="t1"/>
                    <awayTeam id="t4"/>
                    <playedMatch>
                        <teamInMatch>
                            <teamRef id="t1"/>
                            <innings/>
                        </teamInMatch>
                        <teamInMatch>
                            <teamRef id="t4"/>
                            <innings/>
                        </teamInMatch>
                    </playedMatch>
                </match>
                <match>
                    <date>2013-08-23.15:15</date>
                    <homeTeam id="t2"/>
                    <awayTeam id="t3"/>
                    <playedMatch>
                        <teamInMatch>
                            <teamRef id="t2"/>
                            <innings/>
                        </teamInMatch>
                        <teamInMatch>
                            <teamRef id="t3"/>
                            <innings/>
                        </teamInMatch>
                    </playedMatch>
                </match>
            </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        generator = AveragesReportGenerator()
        leagues = {"l1": "League 1"}
        teams = {"t1": "Team 1", "t2": "Team 2"}
        players = {}
        batting = True
        bowling = True
        result = generator.getAverages(rootElement, leagues, teams, players, batting, bowling)
        self.assertEquals(result.lastCompleteMatchDate, datetime.date(2013, 8, 23))
        self.assertEquals(result.lastScheduledMatchDate, datetime.date(2013, 8, 23))
        self.assertEquals(0, result.toCome)
        
    def testGetAllTeamsByLeague(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        result = AveragesReportGenerator().getAllTeamsByLeague(rootElement)
        expectedResult = {}
        teams=[]
        expectedResult[("Division1", "Division 1")] = teams
        teams.append(("FarehamCroftonA", "Fareham & Crofton A"))
        teams.append(("FarehamCroftonB", "Fareham & Crofton B"))
        teams.append(("HambledonA", "Hambledon A"))
        teams.append(("HavantA", "Havant A"))
        teams.append(("HavantB", "Havant B"))
        teams.append(("PortchesterA", "Portchester A"))
        teams.append(("PortsmouthA", "Portsmouth A"))
        teams.append(("PurbrookA", "Purbrook A"))
        teams.append(("UnitedServices", "United Services"))
        teams.append(("WaterloovilleA", "Waterlooville A"))
        teams=[]
        expectedResult[("Division2", "Division 2")] = teams
        teams.append(("BedhamptonA", "Bedhampton A"))
        teams.append(("DOECavaliers", "DOE Cavaliers"))
        teams.append(("HaylingIsland", "Hayling Island"))
        teams.append(("LocksHeathA", "Locks Heath A"))
        teams.append(("PortsmouthSouthsea", "Portsmouth & Southsea"))
        teams.append(("Curdridge", "Curdridge"))
        teams.append(("PurbrookB", "Purbrook B"))
        teams.append(("SarisburyAthleticA", "Sarisbury Athletic A"))
        teams.append(("StJamesCasuals", "St James Casuals"))
        teams.append(("XIIthMenA", "XIIth Men A"))
        teams=[]
        expectedResult[("Division3", "Division 3")] = teams
        teams.append(("Corinthians", "Corinthians"))
        teams.append(("Denmead", "Denmead"))
        teams.append(("Emsworth", "Emsworth"))
        teams.append(("FarehamCroftonC", "Fareham & Crofton C"))
        teams.append(("IBMSouthHants", "IBM South Hants"))
        teams.append(("Petersfield", "Petersfield"))
        teams.append(("PortsmouthB", "Portsmouth B"))
        teams.append(("BedhamptonB", "Bedhampton B"))
        teams.append(("PortsmouthPriory", "Portsmouth Priory"))
        teams.append(("WaterloovilleB", "Waterlooville B"))
        teams=[]
        expectedResult[("Division4", "Division 4")] = teams
        teams.append(("KnowleVillage", "Knowle Village"))
        teams.append(("BedhamptonC", "Bedhampton C"))
        teams.append(("HambledonB", "Hambledon B"))
        teams.append(("HampshireBowman", "Hampshire Bowman"))
        teams.append(("LocksHeathB", "Locks Heath B"))
        teams.append(("PortchesterB", "Portchester B"))
        teams.append(("PurbrookC", "Purbrook C"))
        teams.append(("SarisburyAthleticB", "Sarisbury Athletic B"))
        teams.append(("SouthernElectric", "Southern Electric"))
        teams.append(("XIIthMenB", "XIIth Men B"))
        teams=[]
        expectedResult[("ColtsUnder16", "Colts Under-16")] = teams
        teams.append(("FarehamCrofton", "Fareham & Crofton"))
        teams.append(("GosportBorough", "Gosport Borough"))
        teams.append(("Hambledon", "Hambledon"))
        teams.append(("Havant", "Havant"))
        teams.append(("Petersfield0", "Petersfield"))
        teams.append(("Portsmouth", "Portsmouth"))
        teams.append(("PortsmouthSouthsea0", "Portsmouth & Southsea"))
        teams.append(("Purbrook", "Purbrook"))
        teams.append(("SarisburyAthletic", "Sarisbury Athletic"))
        teams.append(("Waterlooville", "Waterlooville"))
        teams=[]
        expectedResult[("ColtsUnder13", "Colts Under-13")] = teams
        teams.append(("FarehamCrofton0", "Fareham & Crofton"))
        teams.append(("Hambledon0", "Hambledon"))
        teams.append(("Havant0", "Havant"))
        teams.append(("LocksHeath", "Locks Heath"))
        teams.append(("Portsmouth0", "Portsmouth"))
        teams.append(("PortsmouthCommunity", "Portsmouth Community"))
        teams.append(("PortsmouthSouthsea1", "Portsmouth & Southsea"))
        teams.append(("Purbrook0", "Purbrook"))
        teams.append(("SarisburyAthletic0", "Sarisbury Athletic"))
        teams.append(("Waterlooville0", "Waterlooville"))        
        self.assertEquals(len(expectedResult), len(result))
        for k, v in expectedResult.items():
            r = result[k]
            self.assertEquals(sorted(v, key=itemgetter(0)), sorted(r, key=itemgetter(0)))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetLeaguesTeamsAndPlayersNeitherLeaguesNorTeamSpecified']
    unittest.main()