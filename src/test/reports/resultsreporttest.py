'''
Created on 5 Aug 2013

@author: hicksj
'''
from xml.etree import ElementTree
import datetime
import unittest
from operator import attrgetter
from reports.resultsreport import ResultsReportGenerator

class Test(unittest.TestCase):

    def testIsOnDateAnswerFalse(self):
        xml = """
        <match><date>2013-08-05.18:15</date></match>
        """
        matchElement = ElementTree.fromstring(xml)
        date = datetime.date(2013, 8, 4)
        expectedResult = False
        self.doTestIsOnDate(matchElement, date, expectedResult)

    def testIsOnDateAnswerTrue(self):
        xml = """
        <match><date>2013-08-05.18:15</date></match>
        """
        matchElement = ElementTree.fromstring(xml)
        date = datetime.date(2013, 8, 5)
        expectedResult = True
        self.doTestIsOnDate(matchElement, date, expectedResult)

    def doTestIsOnDate(self, matchElement, date, expectedResult):
        generator = ResultsReportGenerator()
        result = generator.isOnDate(matchElement, date)
        self.assertEquals(expectedResult, result)
        
    def testIsCompleteNotPlayedOrAwarded(self):
        xml = """
        <match></match>
        """
        matchElement = ElementTree.fromstring(xml)
        expectedResult = False
        self.doTestIsComplete(matchElement, expectedResult)

    def testIsCompletePlayed(self):
        xml = """
        <match><playedMatch/></match>
        """
        matchElement = ElementTree.fromstring(xml)
        expectedResult = True
        self.doTestIsComplete(matchElement, expectedResult)

    def testIsCompleteAwarded(self):
        xml = """
        <match><awardedMatch/></match>
        """
        matchElement = ElementTree.fromstring(xml)
        expectedResult = True
        self.doTestIsComplete(matchElement, expectedResult)

    def doTestIsComplete(self, matchElement, expectedResult):
        generator = ResultsReportGenerator()
        result = generator.isComplete(matchElement)
        self.assertEquals(expectedResult, result)
        
    def testGetCompletedMatchesDateSpecified(self):
        xml = """
        <league>
            <name>Hello</name>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <pitch>A</pitch>
                <date>2013-10-30.18:15</date>
                <playedMatch/>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <pitch>A</pitch>
                <date>2013-10-30.17:15</date>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.19:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-31.20:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        date = datetime.date(2013, 10, 30)
        generator = ResultsReportGenerator()
        result = generator.getCompletedMatches(leagueElement, {}, {}, date)
        expectedTimes = [datetime.time(18, 15), datetime.time(19, 15)]
        for e, a in zip(sorted([m.time for m in result]), sorted(expectedTimes)):
            self.assertEqual(e, a)
        
    def testGetCompletedMatchesDateNotSpecified(self):
        xml = """
        <league>
            <name>Hello</name>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.18:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.17:15</date>
                <pitch>A</pitch>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.19:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-31.20:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        date = None
        generator = ResultsReportGenerator()
        result = generator.getCompletedMatches(leagueElement, {}, {}, date)
        expectedTimes = [datetime.time(18, 15), datetime.time(19, 15), datetime.time(20, 15)]
        for e, a in zip(sorted([m.time for m in result]), sorted(expectedTimes)):
            self.assertEqual(e, a)
        
    def testGetCompletedMatchesForDate(self):
        xml = """
        <model>
        <league>
            <name>Hello</name>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.18:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.17:15</date>
                <pitch>A</pitch>
            </match>
        <league>
        </league>
            <name>Hello</name>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-30.19:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
            <match>
                <homeTeam id="asad"/>
                <awayTeam id="adasd"/>
                <date>2013-10-31.20:15</date>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
        </league>
        </model>
        """
        rootElement = ElementTree.fromstring(xml)
        date = datetime.date(2013, 10, 30)
        generator = ResultsReportGenerator()
        result = generator.getCompletedMatchesForDate(rootElement, date)
        expectedTimes = [datetime.time(18, 15), datetime.time(19, 15)]
        for e, a in zip(sorted([m.time for m in result]), sorted(expectedTimes)):
            self.assertEqual(e, a)
            
    def testGetCompletedMatchesForLeague(self):
        xml = """
        <league id="l1">
            <name>Hello</name>
            <team id="agsad"><name>sgdsag</name></team>
            <match>
                <date>2013-10-30.18:15</date>
                <homeTeam id="agsad"/>
                <awayTeam id="agsad"/>
                <pitch>A</pitch>
                <playedMatch/>
            </match>
            <match>
                <date>2013-10-30.17:15</date>
                <homeTeam id="agsad"/>
                <awayTeam id="agsad"/>
                <pitch>A</pitch>
                <awardedMatch>
                    <winner id="agsad"/>
                    <reason/>
                </awardedMatch>
            </match>
            <match>
                <date>2013-10-30.19:15</date>
                <homeTeam id="agsad"/>
                <awayTeam id="agsad"/>
                <pitch>A</pitch>
            </match>
        </league>
        """
        leagueElement = ElementTree.fromstring(xml)
        generator = ResultsReportGenerator()
        result = generator.getCompletedMatchesForLeague(leagueElement)
        expectedTimes = [datetime.time(18, 15), datetime.time(17, 15)]
        for e, a in zip(sorted([m.time for m in result]), sorted(expectedTimes)):
            self.assertEqual(e, a)
            
    def testGetMatchNotPlayedOrAwarded(self):
        xml = """
        <match>
            <date>2014-09-03.14:24</date>
            <pitch>A</pitch>
            <homeTeam id="asad"/>
            <awayTeam id="adasd"/>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        generator = ResultsReportGenerator()
        teams = {"asad": "asjghsdak", "adasd": "asgsgasdgssa"}
        result = generator.getMatch(matchElement, teams, {}, "Hello")
        self.assertEqual(datetime.date(2014, 9, 3), result.date)
        self.assertEqual(datetime.time(14, 24), result.time)
        self.assertEqual("A", result.court)
        self.assertEqual("asad", result.homeTeamId)
        self.assertEqual("asjghsdak", result.homeTeamName)
        self.assertEqual("adasd", result.awayTeamId)
        self.assertEqual("asgsgasdgssa", result.awayTeamName)
        self.assertEqual("Hello", result.leagueName)
        self.assertEqual(None, result.innings)
        self.assertEquals(None, result.award)
        
    def testGetMatchPlayed(self):
        xml = """
        <match>
            <date>2014-09-03.14:24</date>
            <homeTeam id="asad"/>
            <awayTeam id="adasd"/>
            <pitch>A</pitch>
            <playedMatch>
                <overLimit>11</overLimit>
                <teamInMatch>
                    <teamRef id="asad"/>
                    <battingFirst>false</battingFirst>
                    <innings>
                        <runsScored>120</runsScored>
                        <wicketsLost>3</wicketsLost>
                        <batsman id="p1"><runs>20</runs><out>true</out></batsman>
                        <bowler id="p2"><runs>4</runs><wickets>3</wickets><ballsBowled>15</ballsBowled></bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="adasd"/>
                    <battingFirst>true</battingFirst>
                    <innings>
                        <runsScored>130</runsScored>
                        <ballsBowled>64</ballsBowled>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        generator = ResultsReportGenerator()
        teams = {"asad": "asjghsdak", "adasd": "asgsgasdgssa"}
        players = {"p1": "sgsghdadhga", "p2": "hhfgjfjgjf"}
        result = generator.getMatch(matchElement, teams, players, "Hello")
        self.assertEqual(datetime.date(2014, 9, 3), result.date)
        self.assertEqual(datetime.time(14, 24), result.time)
        self.assertEqual("A", result.court)
        self.assertEqual("asad", result.homeTeamId)
        self.assertEqual("asjghsdak", result.homeTeamName)
        self.assertEqual("adasd", result.awayTeamId)
        self.assertEqual("asgsgasdgssa", result.awayTeamName)
        self.assertEqual("Hello", result.leagueName)
        for e, a in zip([False, True], ["asad", "adasd"]):
            self.assertEqual(e, result.innings.get(a).first)
        self.assertEquals(None, result.award)
        
    def testGetMatchAwarded(self):
        xml = """
        <match>
            <date>2014-09-03.14:24</date>
            <pitch>A</pitch>
            <homeTeam id="asad"/>
            <awayTeam id="adasd"/>
            <playedMatch>
                <overLimit>11</overLimit>
                <teamInMatch>
                    <teamRef id="asad"/>
                    <battingFirst>false</battingFirst>
                    <innings>
                        <runsScored>120</runsScored>
                        <wicketsLost>3</wicketsLost>
                        <batsman id="p1"><runs>20</runs><out>true</out></batsman>
                        <bowler id="p2"><runs>4</runs><wickets>3</wickets><ballsBowled>15</ballsBowled></bowler>
                    </innings>
                </teamInMatch>
                <teamInMatch>
                    <teamRef id="adasd"/>
                    <battingFirst>true</battingFirst>
                    <innings>
                        <runsScored>130</runsScored>
                        <ballsBowled>64</ballsBowled>
                    </innings>
                </teamInMatch>
            </playedMatch>
        </match>
        """
        matchElement = ElementTree.fromstring(xml)
        generator = ResultsReportGenerator()
        teams = {"asad": "asjghsdak", "adasd": "asgsgasdgssa"}
        players = {"p1": "sgsghdadhga", "p2": "hhfgjfjgjf"}
        result = generator.getMatch(matchElement, teams, players, "Hello")
        self.assertEqual(datetime.date(2014, 9, 3), result.date)
        self.assertEqual(datetime.time(14, 24), result.time)
        self.assertEqual("A", result.court)
        self.assertEqual("asad", result.homeTeamId)
        self.assertEqual("asjghsdak", result.homeTeamName)
        self.assertEqual("adasd", result.awayTeamId)
        self.assertEqual("asgsgasdgssa", result.awayTeamName)
        self.assertEqual("Hello", result.leagueName)
        for e, a in zip([False, True], ["asad", "adasd"]):
            self.assertEqual(e, result.innings.get(a).first)
        self.assertEquals(None, result.award)
        
    def testGetBattingHighlights(self):
        xml = """
        <innings>
            <batsman player="pc"><runs>20</runs><out>true</out></batsman>
            <batsman player="nr"><runs>27</runs><out>true</out></batsman>
            <batsman player="ph"><runs>19</runs><out>false</out></batsman>
            <batsman player="gc"><runs>20</runs><out>false</out><notes>inc. 3 sixes</notes></batsman>
            <batsman player="jl"><runs>19</runs><out>true</out></batsman>
        </innings>
        """
        inningsElement = ElementTree.fromstring(xml)
        players = {"ph": "P Hicks", "gc": "G Cornish", "jl": "J Lowe", "pc" : "P Croxson", "nr": "N Ross"}
        generator = ResultsReportGenerator()
        result = generator.getBattingHighlights(inningsElement, players)
        expectedResults = [["N Ross", 27, True, "972RossN"], ["G Cornish", 20, False, "979CornishG", "inc. 3 sixes"], ["P Croxson", 20, True, "979CroxsonP"]]
        for e, a in zip(expectedResults, sorted(result, key=attrgetter("sortKey"))):
            self.assertEquals(e[0], a.playerName)
            self.assertEquals(e[1], a.runs)
            self.assertEquals(e[2], a.out)
            self.assertEquals(e[3], a.sortKey)
            self.assertEquals(e[4] if len(e) > 4 else None, a.notes)
            
    def testGetBowlingHighlights(self):
        xml = """
        <innings>
            <bowler player="pc"><runs>20</runs><wickets>3</wickets><notes>inc. a hat-trick</notes></bowler>
            <bowler player="nr"><runs>20</runs><wickets>2</wickets></bowler>
            <bowler player="ph"><runs>19</runs><wickets>2</wickets></bowler>
            <bowler player="gc"><runs>20</runs><wickets>2</wickets></bowler>
            <bowler player="jl"><runs>19</runs><wickets>0</wickets></bowler>
        </innings>
        """
        inningsElement = ElementTree.fromstring(xml)
        players = {"ph": "P Hicks", "gc": "G Cornish", "jl": "J Lowe", "pc" : "P Croxson", "nr": "NRoss"}
        generator = ResultsReportGenerator()
        result = generator.getBowlingHighlights(inningsElement, players)
        expectedResults = [["P Croxson", 20, 3, "6020CroxsonP", "inc. a hat-trick"], ["P Hicks", 19, 2, "7019HicksP"], ["G Cornish", 20, 2, "7020CornishG"], ["NRoss", 20, 2, "7020NRoss"]]
        for e, a in zip(expectedResults, sorted(result, key=attrgetter("sortKey"))):
            self.assertEquals(e[0], a.playerName)
            self.assertEquals(e[1], a.runs)
            self.assertEquals(e[2], a.wickets)
            self.assertEquals(e[3], a.sortKey)
            self.assertEquals(e[4] if len(e) > 4 else None, a.notes)
            
    def testGetInningsWicketsNotSpecifiedBallsNotSpecified(self):
        xml = """
        <innings>
            <runsScored>113</runsScored>
            <batsman id="p1"><runs>40</runs><out>false</out></batsman>
            <bowler id="p2"><runs>19</runs><wickets>2</wickets></bowler>
        </innings>
        """
        inningsElement = ElementTree.fromstring(xml)
        players = {"p1": "P Hicks", "p2": "Saleem"}
        generator = ResultsReportGenerator()
        result = generator.getInnings(inningsElement, "t1", "Rotherham", True, 70, players)
        self.assertEquals(113, result.runs)
        self.assertEquals(6, result.wickets)
        self.assertEquals(70, result.balls)
        self.assertEquals(True, result.first)
        self.assertEquals("t1", result.teamId)
        self.assertEquals("Rotherham", result.teamName)
        self.assertEquals(1, len(result.batHighlights))
        self.assertEquals(1, len(result.bowlHighlights))

    def testGetInningsWicketsSpecifiedBallsNotSpecified(self):
        xml = """
        <innings>
            <runsScored>113</runsScored>
            <wicketsLost>4</wicketsLost>
            <batsman id="p1"><runs>40</runs><out>false</out></batsman>
            <bowler id="p2"><runs>19</runs><wickets>2</wickets></bowler>
        </innings>
        """
        inningsElement = ElementTree.fromstring(xml)
        players = {"p1": "P Hicks", "p2": "Saleem"}
        generator = ResultsReportGenerator()
        result = generator.getInnings(inningsElement, "t1", "Rotherham", False, 70, players)
        self.assertEquals(113, result.runs)
        self.assertEquals(4, result.wickets)
        self.assertEquals(70, result.balls)
        self.assertEquals(False, result.first)
        self.assertEquals("t1", result.teamId)
        self.assertEquals("Rotherham", result.teamName)
        self.assertEquals(1, len(result.batHighlights))
        self.assertEquals(1, len(result.bowlHighlights))

    def testGetInningsWicketsNotSpecifiedBallsSpecified(self):
        xml = """
        <innings>
            <runsScored>113</runsScored>
            <ballsBowled>63</ballsBowled>
            <batsman id="p1"><runs>40</runs><out>false</out></batsman>
            <bowler id="p2"><runs>19</runs><wickets>2</wickets></bowler>
        </innings>
        """
        inningsElement = ElementTree.fromstring(xml)
        players = {"p1": "P Hicks", "p2": "Saleem"}
        generator = ResultsReportGenerator()
        result = generator.getInnings(inningsElement, "t1", "Rotherham", True, 70, players)
        self.assertEquals(113, result.runs)
        self.assertEquals(6, result.wickets)
        self.assertEquals(63, result.balls)
        self.assertEquals(True, result.first)
        self.assertEquals("t1", result.teamId)
        self.assertEquals("Rotherham", result.teamName)
        self.assertEquals(1, len(result.batHighlights))
        self.assertEquals(1, len(result.bowlHighlights))

    def testGetInningsWicketsSpecifiedBallsSpecified(self):
        xml = """
        <innings>
            <runsScored>113</runsScored>
            <wicketsLost>5</wicketsLost>
            <ballsBowled>63</ballsBowled>
            <batsman id="p1"><runs>40</runs><out>false</out></batsman>
            <bowler id="p2"><runs>19</runs><wickets>2</wickets></bowler>
        </innings>
        """
        inningsElement = ElementTree.fromstring(xml)
        players = {"p1": "P Hicks", "p2": "Saleem"}
        generator = ResultsReportGenerator()
        result = generator.getInnings(inningsElement, "t1", "Rotherham", False, 70, players)
        self.assertEquals(113, result.runs)
        self.assertEquals(5, result.wickets)
        self.assertEquals(63, result.balls)
        self.assertEquals(False, result.first)
        self.assertEquals("t1", result.teamId)
        self.assertEquals("Rotherham", result.teamName)
        self.assertEquals(1, len(result.batHighlights))
        self.assertEquals(1, len(result.bowlHighlights))
        
    def testGetInningsListOverLimitSpecified(self):
        xml = """
        <playedMatch>
            <overLimit>11</overLimit>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>133</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>135</runsScored>
                    <wicketsLost>3</wicketsLost>
                    <ballsBowled>64</ballsBowled>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        players = {"p1": "P Hicks", "p2": "Saleem"}
        teams = {"t1": "Rotherham", "t2": "Reading"}
        generator = ResultsReportGenerator()
        result = generator.getInningsList(playedMatchElement, teams, players)
        expectedData = [["t1", True, 66], ["t2", False, 64]]
        self.assertEquals(len(expectedData), len(result))
        for d in expectedData:
            inns = result[d[0]]
            self.assertEquals(d[1], inns.first)
            self.assertEquals(d[2], inns.balls)

    def testGetInningsListOverLimitNotSpecified(self):
        xml = """
        <playedMatch>
            <teamInMatch>
                <teamRef id="t1"/>
                <battingFirst>true</battingFirst>
                <innings>
                    <runsScored>133</runsScored>
                </innings>
            </teamInMatch>
            <teamInMatch>
                <teamRef id="t2"/>
                <battingFirst>false</battingFirst>
                <innings>
                    <runsScored>135</runsScored>
                    <wicketsLost>3</wicketsLost>
                    <ballsBowled>64</ballsBowled>
                </innings>
            </teamInMatch>
        </playedMatch>
        """
        playedMatchElement = ElementTree.fromstring(xml)
        players = {"p1": "P Hicks", "p2": "Saleem"}
        teams = {"t1": "Rotherham", "t2": "Reading"}
        generator = ResultsReportGenerator()
        result = generator.getInningsList(playedMatchElement, teams, players)
        expectedData = [["t1", True, 72], ["t2", False, 64]]
        self.assertEquals(len(expectedData), len(result))
        for d in expectedData:
            inns = result[d[0]]
            self.assertEquals(d[1], inns.first)
            self.assertEquals(d[2], inns.balls)
            
    def testGetAwardedMatchDetails(self):
        xml = """
        <awardedMatch>
            <winner id="t1"/>
            <reason>Unable to raise a team</reason>
        </awardedMatch>
        """
        awardedMatchElement = ElementTree.fromstring(xml)
        generator = ResultsReportGenerator()
        teams = {"t1": "Rotherham", "t2": "Reading"}
        result = generator.getAwardedMatchDetails(awardedMatchElement, "t1", "t2", teams)
        self.assertEquals("t1", result.winnerId)
        self.assertEquals("Rotherham", result.winnerName)
        self.assertEquals("t2", result.loserId)
        self.assertEquals("Reading", result.loserName)
        self.assertEquals("Unable to raise a team", result.reason)
        
    def testGetLeagueResultsReportLeagueIdNotFound(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        leagueId = "Division5"
        generator = ResultsReportGenerator()
        result = generator.getLeagueResultsReport(rootElement, leagueId)
        self.assertEqual(None, result.leagueId)
        self.assertEqual(None, result.leagueName)

    def testGetLeagueResultsReportLeagueFound(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        leagueId = "Division1"
        generator = ResultsReportGenerator()
        result = generator.getLeagueResultsReport(rootElement, leagueId)
        self.assertEqual(leagueId, result.leagueId)
        self.assertEqual("Division 1", result.leagueName)
        self.assertEqual(45, len(result.matches))
        
    def testGetAllMatchDatesWithCompletedMatchesAllCompleteNoExcludedDate(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        generator = ResultsReportGenerator()
        result = generator.getAllMatchDatesWithCompletedMatches(rootElement)
        expectedResults = []
        date = datetime.date(2012, 9, 30)
        lastDate = datetime.date(2013, 3, 10)
        missedDate = datetime.date(2012, 12, 30)
        delta = datetime.timedelta(7)
        while date <= lastDate:
            if date != missedDate:
                expectedResults.append(date)
            date = date + delta
        for e, a in zip(expectedResults, sorted(result)):
            self.assertEquals(e, a)

    def testGetAllMatchDatesWithCompletedMatchesAllCompleteExcludedDate(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        generator = ResultsReportGenerator()
        excludeDate = datetime.date(2013, 3, 3)
        result = generator.getAllMatchDatesWithCompletedMatches(rootElement, excludeDate)
        expectedResults = []
        date = datetime.date(2012, 9, 30)
        lastDate = datetime.date(2013, 3, 10)
        missedDates = [datetime.date(2012, 12, 30), excludeDate]
        delta = datetime.timedelta(7)
        while date <= lastDate:
            if missedDates.count(date) == 0:
                expectedResults.append(date)
            date = date + delta
        for e, a in zip(expectedResults, sorted(result)):
            self.assertEquals(e, a)

    def testGetAllMatchDatesWithCompletedMatchesNoneComplete(self):
        rootElement = ElementTree.parse("data/2013-14.xml")
        generator = ResultsReportGenerator()
        result = generator.getAllMatchDatesWithCompletedMatches(rootElement)
        self.assertEquals(0, len(result))
        
    def testGetDateResultsReportDateSpecified(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        generator = ResultsReportGenerator()
        date = datetime.date(2013, 3, 3)
        result = generator.getDateResultsReport(rootElement, date)
        self.assertEqual(date, result.date)
        self.assertEqual(22, len(result.otherDates))
        self.assertEqual(12, len(result.matches))

    def testGetDateResultsReportNoDateSpecifiedResultsExist(self):
        rootElement = ElementTree.parse("data/2012-13.xml")
        generator = ResultsReportGenerator()
        date = None
        result = generator.getDateResultsReport(rootElement, date)
        self.assertEqual(datetime.date(2013, 3, 10), result.date)
        self.assertEqual(22, len(result.otherDates))
        self.assertEqual(12, len(result.matches))

    def testGetDateResultsReportNoDateSpecifiedNoResultsExist(self):
        rootElement = ElementTree.parse("data/2013-14.xml")
        generator = ResultsReportGenerator()
        date = None
        result = generator.getDateResultsReport(rootElement, date)
        self.assertEqual(None, result.date)
        self.assertEqual(0, len(result.otherDates))
        self.assertEqual(0, len(result.matches))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testIsOnDate']
    unittest.main()