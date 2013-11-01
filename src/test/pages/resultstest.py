'''
Created on 7 Aug 2013

@author: hicksj
'''
from pages.results import Results, LeagueResults, DateResults
from reports.resultsreport import BattingPerformance, BowlingPerformance, \
    InningsInMatch, MatchInReport, AwardDetails, LeagueResultsReport, \
    DateResultsReport
from test.testbase import TestBase
import datetime
import unittest


class Test(TestBase):

    def testGetOversTextNoRemainder(self):
        balls = 54
        result = Results("").getOversText(balls)
        self.assertEqual("9", result)

    def testGetOversTextWithRemainder(self):
        balls = 57
        result = Results("").getOversText(balls)
        self.assertEqual("9.3", result)

    def testGetBattingHighlightBatsmanOutNoNotes(self):
        highlight = BattingPerformance("J Hicks", 20, True, None)
        result = Results("").getBattingHighlight(highlight)
        self.assertEquals("<span class=\"nolinewrap\">J Hicks 20</span>", result)

    def testGetBattingHighlightBatsmanOutWithNotes(self):
        highlight = BattingPerformance("J Hicks", 20, True, "Batsman is rubbish")
        result = Results("").getBattingHighlight(highlight)
        self.assertEquals("<span class=\"nolinewrap\">J Hicks 20</span> (Batsman is rubbish)", result)

    def testGetBattingHighlightBatsmanNotOutNoNotes(self):
        highlight = BattingPerformance("J Hicks", 20, False, None)
        result = Results("").getBattingHighlight(highlight)
        self.assertEquals("<span class=\"nolinewrap\">J Hicks 20*</span>", result)

    def testGetBattingHighlightBatsmanNotOutWithNotes(self):
        highlight = BattingPerformance("J Hicks", 26, False, "Batsman is rather good")
        result = Results("").getBattingHighlight(highlight)
        self.assertEquals("<span class=\"nolinewrap\">J Hicks 26*</span> (Batsman is rather good)", result)
        
    def testGetBowlingHighlightNoNotes(self):
        highlight = BowlingPerformance("J Hicks", 42, 2, None)
        result = Results("").getBowlingHighlight(highlight)
        self.assertEquals("<span class=\"nolinewrap\">J Hicks 2/42</span>", result)

    def testGetBowlingHighlightWithNotes(self):
        highlight = BowlingPerformance("J Hicks", 42, 2, "Very loose")
        result = Results("").getBowlingHighlight(highlight)
        self.assertEquals("<span class=\"nolinewrap\">J Hicks 2/42</span> (Very loose)", result)
        
    def testGetScoreTextAllOut(self):
        result = Results("").getScoreText(140, 6)
        self.assertEquals("140 all out", result)

    def testGetScoreTextNotAllOut(self):
        result = Results("").getScoreText(140, 5)
        self.assertEquals("140 for 5", result)
        
    def testGetInningsHighlightsBatAbsentBowlAbsent(self):
        innings = InningsInMatch()
        result = Results("").getInningsHighlights(innings)
        expectedResult = ""
        self.assertEquals(expectedResult, result)

    def testGetInningsHighlightsBatPresentBowlAbsent(self):
        innings = InningsInMatch()
        innings.batHighlights.append(BattingPerformance("J Hicks", 40, False, None))
        innings.batHighlights.append(BattingPerformance("P Hicks", 30, True, None))
        innings.batHighlights.append(BattingPerformance("G Cornish", 40, True, None))
        result = Results("").getInningsHighlights(innings)
        expectedResult = """
        <span class="nolinewrap">G Cornish 40</span>,
        <span class="nolinewrap">J Hicks 40*</span>,
        <span class="nolinewrap">P Hicks 30</span>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetInningsHighlightsBatAbsentBowlPresent(self):
        innings = InningsInMatch()
        innings.bowlHighlights.append(BowlingPerformance("J Hicks", 20, 2, None))
        innings.bowlHighlights.append(BowlingPerformance("P Hicks", 20, 3, None))
        innings.bowlHighlights.append(BowlingPerformance("G Cornish", 15, 2, None))
        innings.bowlHighlights.append(BowlingPerformance("M Ahern", 20, 2, None))
        result = Results("").getInningsHighlights(innings)
        expectedResult = """
        <span class="nolinewrap">P Hicks 3/20</span>,
        <span class="nolinewrap">G Cornish 2/15</span>,
        <span class="nolinewrap">M Ahern 2/20</span>,
        <span class="nolinewrap">J Hicks 2/20</span>
        """
        self.assertMultiLineEqual(expectedResult, result)

    def testGetInningsHighlightsBatPresentBowlPresent(self):
        innings = InningsInMatch()
        innings.batHighlights.append(BattingPerformance("J Hicks", 40, False, None))
        innings.bowlHighlights.append(BowlingPerformance("G Cornish", 15, 2, None))
        result = Results("").getInningsHighlights(innings)
        expectedResult = """
        <span class="nolinewrap">J Hicks 40*</span>,
        <span class="nolinewrap">G Cornish 2/15</span>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetHighlightsLineInns1NoHighlightsInns2NoHighlights(self):
        innings1 = InningsInMatch()
        innings2 = InningsInMatch()
        expectedResult = """
        """
        result = Results("").getHighlightsLine(innings1, innings2)
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetHighlightsLineInns1NoHighlightsInns2Highlights(self):
        innings1 = InningsInMatch()
        innings2 = InningsInMatch()
        innings2.bowlHighlights.append(BowlingPerformance("J Hicks", 20, 4, "inc. a hat-trick"))
        expectedResult = """
        <tr>
            <td class="highlights">
            </td>
            <td class="highlights">
                <span class="nolinewrap">J Hicks 4/20</span> (inc. a hat-trick)
            </td>
        </tr>
        """
        result = Results("").getHighlightsLine(innings1, innings2)
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetHighlightsLineInns1HighlightsInns2NoHighlights(self):
        innings1 = InningsInMatch()
        innings1.batHighlights.append(BattingPerformance("J Hicks", 50, False, None))
        innings2 = InningsInMatch()
        expectedResult = """
        <tr>
            <td class="highlights">
                <span class="nolinewrap">J Hicks 50*</span>
            </td>
            <td class="highlights">
            </td>
        </tr>
        """
        result = Results("").getHighlightsLine(innings1, innings2)
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetHighlightsLineInns1HighlightsInns2Highlights(self):
        innings1 = InningsInMatch()
        innings1.batHighlights.append(BattingPerformance("J Hicks", 50, False, None))
        innings2 = InningsInMatch()
        innings2.bowlHighlights.append(BowlingPerformance("J Hicks", 20, 4, "inc. a hat-trick"))
        expectedResult = """
        <tr>
            <td class="highlights">
                <span class="nolinewrap">J Hicks 50*</span>
            </td>
            <td class="highlights">
                <span class="nolinewrap">J Hicks 4/20</span> (inc. a hat-trick)
            </td>
        </tr>
        """
        result = Results("").getHighlightsLine(innings1, innings2)
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetScore(self):
        innings = InningsInMatch()
        innings.runs = 120
        innings.wickets = 5
        innings.balls = 72
        innings.teamId = "t1"
        innings.teamName = "Rotherham"
        result = Results("").getScore(innings)
        expectedResult = """
        <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 120 for 5 (12 ov)
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetScoreLine(self):
        innings = InningsInMatch()
        innings.runs = 120
        innings.wickets = 5
        innings.balls = 72
        innings.teamId = "t1"
        innings.teamName = "Rotherham"
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 40
        innings.wickets = 6
        innings.balls = 35
        innings.teamId = "t2"
        innings.teamName = "Reading"
        innings2 = innings
        homeTeamId = "t2"
        awayTeamId = "t1"
        result = Results("").getScoreLine(innings1, innings2, homeTeamId, awayTeamId)
        expectedResult = """
        <tr>
            <td class="teamscore">
                <a id="t2t1"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 120 for 5 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 40 all out (5.5 ov)
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetResultTextTied(self):
        innings = InningsInMatch()
        innings.runs = 40
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 40
        innings2 = innings
        result = Results("").getResultText(innings1, innings2)
        expectedResult = "Match tied"
        self.assertEqual(expectedResult, result) 
        
    def testGetResultTextWonBy1Run(self):
        innings = InningsInMatch()
        innings.runs = 41
        innings.teamName = "Rotherham"
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 40
        innings2 = innings
        result = Results("").getResultText(innings1, innings2)
        expectedResult = "Rotherham won by 1 run"
        self.assertEqual(expectedResult, result) 
        
    def testGetResultTextWonByMoreThan1Run(self):
        innings = InningsInMatch()
        innings.runs = 42
        innings.teamName = "Rotherham"
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 40
        innings2 = innings
        result = Results("").getResultText(innings1, innings2)
        expectedResult = "Rotherham won by 2 runs"
        self.assertEqual(expectedResult, result) 

    def testGetResultTextWonBy1Wicket(self):
        innings = InningsInMatch()
        innings.runs = 41
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 42
        innings.wickets = 5
        innings.teamName = "Rotherham"
        innings2 = innings
        result = Results("").getResultText(innings1, innings2)
        expectedResult = "Rotherham won by 1 wicket"
        self.assertEqual(expectedResult, result) 
        
    def testGetResultTextWonByMoreThan1Wicket(self):
        innings = InningsInMatch()
        innings.runs = 41
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 42
        innings.wickets = 4
        innings.teamName = "Rotherham"
        innings2 = innings
        result = Results("").getResultText(innings1, innings2)
        expectedResult = "Rotherham won by 2 wickets"
        self.assertEqual(expectedResult, result)
        
    def testGetResultLine(self):
        innings = InningsInMatch()
        innings.runs = 41
        innings1 = innings
        innings = InningsInMatch()
        innings.runs = 42
        innings.wickets = 4
        innings.teamName = "Rotherham"
        innings2 = innings
        result = Results("").getResultLine(innings1, innings2)
        expectedResult = """
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 2 wickets
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPlayedMatchResultWithHighlights(self):
        match = MatchInReport()
        match.homeTeamId = "t1"
        match.homeTeamName = "Rotherham"
        match.awayTeamId = "t2"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.runs = 67
        innings.wickets = 4
        innings.balls = 72
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.batHighlights = [BattingPerformance("J Hicks", 50, False, None)]
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.runs = 62
        innings.wickets = 6
        innings.balls = 63
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.bowlHighlights = [BowlingPerformance("J Hicks", 12, 6, None)]
        result = Results("").getPlayedMatchResult(match)
        expectedResult = """
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 62 all out (10.3 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 67 for 4 (12 ov)
            </td>
        </tr>
        <tr>
            <td class="highlights">
                <span class="nolinewrap">J Hicks 6/12</span>
            </td>
            <td class="highlights">
                <span class="nolinewrap">J Hicks 50*</span>
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 2 wickets
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetPlayedMatchResultNoHighlights(self):
        match = MatchInReport()
        match.homeTeamId = "t1"
        match.homeTeamName = "Rotherham"
        match.awayTeamId = "t2"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.runs = 67
        innings.wickets = 4
        innings.balls = 72
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.runs = 62
        innings.wickets = 6
        innings.balls = 63
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        result = Results("").getPlayedMatchResult(match)
        expectedResult = """
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 62 all out (10.3 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 67 for 4 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 2 wickets
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetAwardedMatchResultHomeTeamWins(self):
        match = MatchInReport()
        award = AwardDetails()
        match.award = award
        award.winnerId = match.homeTeamId = "t1"
        award.winnerName = "Rotherham"
        award.loserId = match.awayTeamId = "t2"
        award.loserName = "Reading"
        award.reason = "Being a bit crap"
        result = Results("").getAwardedMatchResult(match)
        expectedResult = """
        <tr>
            <td colspan="2" class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a>
                beat
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a>
                by default (Being a bit crap)
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetAwardedMatchResultAwayTeamWins(self):
        match = MatchInReport()
        award = AwardDetails()
        match.award = award
        award.winnerId = match.awayTeamId = "t1"
        award.winnerName = "Rotherham"
        award.loserId = match.homeTeamId = "t2"
        award.loserName = "Reading"
        award.reason = "Being a bit crap"
        result = Results("").getAwardedMatchResult(match)
        expectedResult = """
        <tr>
            <td colspan="2" class="teamscore">
                <a id="t2t1"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a>
                beat
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a>
                by default (Being a bit crap)
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetMatchResultPlayedMatch(self):
        match = MatchInReport()
        match.homeTeamId = "t1"
        match.homeTeamName = "Rotherham"
        match.awayTeamId = "t2"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.runs = 67
        innings.wickets = 4
        innings.balls = 72
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.runs = 62
        innings.wickets = 6
        innings.balls = 63
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        result = Results("").getMatchResult(match)
        expectedResult = """
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 62 all out (10.3 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 67 for 4 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 2 wickets
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetMatchResultAwardedMatch(self):
        match = MatchInReport()
        award = AwardDetails()
        match.award = award
        award.winnerId = match.awayTeamId = "t1"
        award.winnerName = "Rotherham"
        award.loserId = match.homeTeamId = "t2"
        award.loserName = "Reading"
        award.reason = "Being a bit crap"
        result = Results("").getMatchResult(match)
        expectedResult = """
        <tr>
            <td colspan="2" class="teamscore">
                <a id="t2t1"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a>
                beat
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a>
                by default (Being a bit crap)
            </td>
        </tr>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetResultsForDate(self):
        theDate = datetime.date(2013, 3, 5)
        matches = []
        
        match = MatchInReport()
        matches.append(match)
        match.time = datetime.time(18, 15)
        match.court = "B"
        match.homeTeamId = "t1"
        match.awayTeamId = "t2"
        match.homeTeamName = "Rotherham"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = True
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 400
        innings.wickets = 0
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = False
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 4
        innings.wickets = 6
        innings.balls = 22
        
        match = MatchInReport()
        matches.append(match)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "t3"
        match.awayTeamId = "t4"
        match.homeTeamName = "Charlton"
        match.awayTeamName = "Oxford"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 12
        innings.wickets = 5
        innings.balls = 9
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 11
        innings.wickets = 6
        innings.balls = 24

        match = MatchInReport()
        matches.append(match)
        match.time = datetime.time(17, 15)
        match.court = "A"
        match.homeTeamId = "t5"
        match.awayTeamId = "t6"
        match.homeTeamName = "Birmingham"
        match.awayTeamName = "Plymouth"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 138
        innings.wickets = 5
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 144
        innings.wickets = 6
        innings.balls = 67

        result = LeagueResults("").getResultsForDate(theDate, matches)
        
        expectedResult = """
        <tr>
            <td class="date" colspan="2">5th March 2013</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t5t6"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t6">Plymouth</a> 144 all out (11.1 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t5">Birmingham</a> 138 for 5 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Plymouth won by 6 runs
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t3t4"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Oxford</a> 11 all out (4 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Charlton</a> 12 for 5 (1.3 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Charlton won by 1 wicket
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 400 for 0 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 4 all out (3.4 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 396 runs
            </td>
        </tr>
        """
        
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportBodyForLeague(self):
        report = LeagueResultsReport()
        report.leagueId = "l1"
        report.leagueName = "League 1"
        matches = []
        report.matches = matches
        
        match = MatchInReport()
        matches.append(match)
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(18, 15)
        match.court = "B"
        match.homeTeamId = "t1"
        match.awayTeamId = "t2"
        match.homeTeamName = "Rotherham"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = True
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 400
        innings.wickets = 0
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = False
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 4
        innings.wickets = 6
        innings.balls = 22
        
        match = MatchInReport()
        matches.append(match)
        match.date = datetime.date(2013, 3, 12)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "t3"
        match.awayTeamId = "t4"
        match.homeTeamName = "Charlton"
        match.awayTeamName = "Oxford"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 12
        innings.wickets = 5
        innings.balls = 9
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 11
        innings.wickets = 6
        innings.balls = 24

        match = MatchInReport()
        matches.append(match)
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(17, 15)
        match.court = "A"
        match.homeTeamId = "t5"
        match.awayTeamId = "t6"
        match.homeTeamName = "Birmingham"
        match.awayTeamName = "Plymouth"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 138
        innings.wickets = 5
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 144
        innings.wickets = 6
        innings.balls = 67

        result = LeagueResults("").getReportBody(report)

        expectedResult = """
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
        <tr>
            <td class="date" colspan="2">12th March 2013</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t3t4"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Oxford</a> 11 all out (4 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Charlton</a> 12 for 5 (1.3 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Charlton won by 1 wicket
            </td>
        </tr>
        <tr>
            <td class="date" colspan="2">5th March 2013</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t5t6"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t6">Plymouth</a> 144 all out (11.1 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t5">Birmingham</a> 138 for 5 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Plymouth won by 6 runs
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 400 for 0 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 4 all out (3.4 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 396 runs
            </td>
        </tr>
        </table>
        """
        
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContentForLeagueNoMatchesExist(self):
        report = LeagueResultsReport()
        report.leagueId = "l1"
        report.leagueName = "League 1"
        matches = []
        report.matches = matches
        result = LeagueResults("").getReportContent(report)

        expectedResult = """
        <h1>League 1</h1>
        <p>Results will be available once the season has started.</p>
        """
        
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetReportContentForLeagueMatchesExist(self):
        report = LeagueResultsReport()
        report.leagueId = "l1"
        report.leagueName = "League 1"
        matches = []
        report.matches = matches
        
        match = MatchInReport()
        matches.append(match)
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(18, 15)
        match.court = "B"
        match.homeTeamId = "t1"
        match.awayTeamId = "t2"
        match.homeTeamName = "Rotherham"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = True
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 400
        innings.wickets = 0
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = False
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 4
        innings.wickets = 6
        innings.balls = 22
        
        match = MatchInReport()
        matches.append(match)
        match.date = datetime.date(2013, 3, 12)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "t3"
        match.awayTeamId = "t4"
        match.homeTeamName = "Charlton"
        match.awayTeamName = "Oxford"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 12
        innings.wickets = 5
        innings.balls = 9
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 11
        innings.wickets = 6
        innings.balls = 24

        match = MatchInReport()
        matches.append(match)
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(17, 15)
        match.court = "A"
        match.homeTeamId = "t5"
        match.awayTeamId = "t6"
        match.homeTeamName = "Birmingham"
        match.awayTeamName = "Plymouth"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 138
        innings.wickets = 5
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 144
        innings.wickets = 6
        innings.balls = 67

        result = LeagueResults("").getReportContent(report)

        expectedResult = """
        <h1>League 1</h1>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
        <tr>
            <td class="date" colspan="2">12th March 2013</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t3t4"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Oxford</a> 11 all out (4 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Charlton</a> 12 for 5 (1.3 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Charlton won by 1 wicket
            </td>
        </tr>
        <tr>
            <td class="date" colspan="2">5th March 2013</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t5t6"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t6">Plymouth</a> 144 all out (11.1 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t5">Birmingham</a> 138 for 5 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Plymouth won by 6 runs
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 400 for 0 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 4 all out (3.4 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 396 runs
            </td>
        </tr>
        </table>
        """
        
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetContentForLeague(self):
        page = LeagueResults("")
        page.allParams = {"xmlFile": "data/2012-13.xml", "league": "Division1"}
        result = page.getContent()
        self.assertNotEqual("", result)

    def testGetOtherDateLinksNoOtherDates(self):
        report = DateResultsReport()
        report.otherDates = []
        result = DateResults("").getOtherDateLinks(report)
        expectedResult = ""
        self.assertEqual(expectedResult, result)
        
    def testGetOtherDateLinksSomeOtherDates(self):
        report = DateResultsReport()
        report.otherDates = []
        report.otherDates.append(datetime.date(2013, 3, 5))
        report.otherDates.append(datetime.date(2014, 3, 5))
        report.otherDates.append(datetime.date(2013, 8, 7))
        result = DateResults("").getOtherDateLinks(report)
        expectedResult = """
        <ul id="datenav" class="noprint">
        <li>Results on other dates:</li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2014-03-05">5th Mar</a>
        </li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2013-08-07">7th Aug</a>
        </li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2013-03-05">5th Mar</a>
        </li>
        </ul>
        """
        self.assertMultiLineEqual(expectedResult, result)
        
    def testGetLeagueSortKeyNoNumericsInInput(self):
        leagueName = "gdsgsgdsags"
        result = DateResults("").getLeagueSortKey(leagueName)
        self.assertEquals(0, result)
        
    def testGetLeagueSortKeyMultipleNumericsInInput(self):
        leagueName = "asdf10sgsgds11"
        result = DateResults("").getLeagueSortKey(leagueName)
        self.assertEquals(20, result)
        
    def testGetLeagueSortKeyOneNumericInInputLessThan10(self):
        leagueName = "asdf9asdgsdg"
        result = DateResults("").getLeagueSortKey(leagueName)
        self.assertEquals(9, result)
        
    def testGetLeagueSortKeyOneNumericInInput10OrMore(self):
        leagueName = "asdf10asdgsdg"
        result = DateResults("").getLeagueSortKey(leagueName)
        self.assertEquals(20, result)
        
    def testGetLeagueSortKeyRealLeagueValues(self):
        data = {}
        data["Division 1"] = 1
        data["Division 2"] = 2
        data["Division 3"] = 3
        data["Division 4"] = 4
        data["Colts Under-16"] = 14
        data["Colts Under-13"] = 17
        for leagueName, expectedResult in data.items():
            result = DateResults("").getLeagueSortKey(leagueName)
            self.assertEquals(expectedResult, result)
    
    def testGetResultsForLeague(self):
        matches = []
        
        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(18, 15)
        match.court = "B"
        match.homeTeamId = "t1"
        match.awayTeamId = "t2"
        match.homeTeamName = "Rotherham"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = True
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 400
        innings.wickets = 0
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = False
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 4
        innings.wickets = 6
        innings.balls = 22
        
        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.date = datetime.date(2013, 3, 12)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "t3"
        match.awayTeamId = "t4"
        match.homeTeamName = "Charlton"
        match.awayTeamName = "Oxford"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 12
        innings.wickets = 5
        innings.balls = 9
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 11
        innings.wickets = 6
        innings.balls = 24

        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(17, 15)
        match.court = "A"
        match.homeTeamId = "t5"
        match.awayTeamId = "t6"
        match.homeTeamName = "Birmingham"
        match.awayTeamName = "Plymouth"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 138
        innings.wickets = 5
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 144
        innings.wickets = 6
        innings.balls = 67
        
        result = DateResults("").getResultsForLeague(matches)

        expectedResult = """
        <tr>
            <td class="division" colspan="2">Division 1</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t5t6"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t6">Plymouth</a> 144 all out (11.1 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t5">Birmingham</a> 138 for 5 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Plymouth won by 6 runs
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t3t4"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Oxford</a> 11 all out (4 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Charlton</a> 12 for 5 (1.3 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Charlton won by 1 wicket
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 400 for 0 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 4 all out (3.4 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 396 runs
            </td>
        </tr>
        """
        
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportBody(self):
        matches = []
        
        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.leagueId = "Division1"
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(18, 15)
        match.court = "B"
        match.homeTeamId = "t1"
        match.awayTeamId = "t2"
        match.homeTeamName = "Rotherham"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = True
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 400
        innings.wickets = 0
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = False
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 4
        innings.wickets = 6
        innings.balls = 22
        
        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Colts Under-16"
        match.leagueId = "ColtsUnder16"
        match.date = datetime.date(2013, 3, 12)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "t3"
        match.awayTeamId = "t4"
        match.homeTeamName = "Charlton"
        match.awayTeamName = "Oxford"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 12
        innings.wickets = 5
        innings.balls = 9
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 11
        innings.wickets = 6
        innings.balls = 24

        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.leagueId = "Division1"
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(17, 15)
        match.court = "A"
        match.homeTeamId = "t5"
        match.awayTeamId = "t6"
        match.homeTeamName = "Birmingham"
        match.awayTeamName = "Plymouth"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 138
        innings.wickets = 5
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 144
        innings.wickets = 6
        innings.balls = 67
        
        report = DateResultsReport()
        report.matches = matches
        report.date = datetime.date(2013, 3, 5)
        
        result = DateResults("").getReportBody(report)

        expectedResult = """
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
        <tr>
            <td class="division" colspan="2">Division 1</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t5t6"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t6">Plymouth</a> 144 all out (11.1 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t5">Birmingham</a> 138 for 5 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Plymouth won by 6 runs
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 400 for 0 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 4 all out (3.4 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 396 runs
            </td>
        </tr>
        <tr>
            <td class="division" colspan="2">Colts Under-16</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t3t4"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Oxford</a> 11 all out (4 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Charlton</a> 12 for 5 (1.3 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Charlton won by 1 wicket
            </td>
        </tr>
        </table>
        """
        
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportContentWithMatches(self):
        matches = []
        
        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.leagueId = "Division1"
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(18, 15)
        match.court = "B"
        match.homeTeamId = "t1"
        match.awayTeamId = "t2"
        match.homeTeamName = "Rotherham"
        match.awayTeamName = "Reading"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = True
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 400
        innings.wickets = 0
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = False
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 4
        innings.wickets = 6
        innings.balls = 22
        
        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Colts Under-16"
        match.leagueId = "ColtsUnder16"
        match.date = datetime.date(2013, 3, 12)
        match.time = datetime.time(18, 15)
        match.court = "A"
        match.homeTeamId = "t3"
        match.awayTeamId = "t4"
        match.homeTeamName = "Charlton"
        match.awayTeamName = "Oxford"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 12
        innings.wickets = 5
        innings.balls = 9
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 11
        innings.wickets = 6
        innings.balls = 24

        match = MatchInReport()
        matches.append(match)
        match.leagueName = "Division 1"
        match.leagueId = "Division1"
        match.date = datetime.date(2013, 3, 5)
        match.time = datetime.time(17, 15)
        match.court = "A"
        match.homeTeamId = "t5"
        match.awayTeamId = "t6"
        match.homeTeamName = "Birmingham"
        match.awayTeamName = "Plymouth"
        match.innings = {}
        innings = InningsInMatch()
        match.innings[match.homeTeamId] = innings
        innings.first = False
        innings.teamId = match.homeTeamId
        innings.teamName = match.homeTeamName
        innings.runs = 138
        innings.wickets = 5
        innings.balls = 72
        innings = InningsInMatch()
        match.innings[match.awayTeamId] = innings
        innings.first = True
        innings.teamId = match.awayTeamId
        innings.teamName = match.awayTeamName
        innings.runs = 144
        innings.wickets = 6
        innings.balls = 67
        
        report = DateResultsReport()
        report.matches = matches
        report.date = datetime.date(2013, 3, 5)
        report.otherDates = [datetime.date(2013, 8, 26), datetime.date(2013, 10, 8)]
        
        result = DateResults("").getReportContent(report)

        expectedResult = """
        <h1>Results: 5th March 2013</h1>
        <ul id="datenav" class="noprint">
        <li>Results on other dates:</li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2013-10-08">8th Oct</a>
        </li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2013-08-26">26th Aug</a>
        </li>
        </ul>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
        <tr>
            <td class="division" colspan="2">Division 1</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t5t6"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t6">Plymouth</a> 144 all out (11.1 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t5">Birmingham</a> 138 for 5 (12 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Plymouth won by 6 runs
            </td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t1t2"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t1">Rotherham</a> 400 for 0 (12 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t2">Reading</a> 4 all out (3.4 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Rotherham won by 396 runs
            </td>
        </tr>
        <tr>
            <td class="division" colspan="2">Colts Under-16</td>
        </tr>
        <tr>
            <td class="teamscore">
                <a id="t3t4"></a>
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t4">Oxford</a> 11 all out (4 ov)
            </td>
            <td class="teamscore">
                <a href="/cgi-bin/page.py?id=teamFixtures&team=t3">Charlton</a> 12 for 5 (1.3 ov)
            </td>
        </tr>
        <tr>
            <td colspan="2" class="result">
                Charlton won by 1 wicket
            </td>
        </tr>
        </table>
        """
        
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportContentNoMatchesButOtherDates(self):
        matches = []
        
        report = DateResultsReport()
        report.matches = matches
        report.date = datetime.date(2013, 3, 5)
        report.otherDates = [datetime.date(2013, 8, 26), datetime.date(2013, 10, 8)]
        
        result = DateResults("").getReportContent(report)

        expectedResult = """
        <h1>Results: 5th March 2013</h1>
        <ul id="datenav" class="noprint">
        <li>Results on other dates:</li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2013-10-08">8th Oct</a>
        </li>
        <li>
            <a href="/cgi-bin/page.py?id=dateResults&date=2013-08-26">26th Aug</a>
        </li>
        </ul>
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
        </table>
        """
        
        self.assertMultiLineEqual(expectedResult, result)

    def testGetReportContentNoMatchesNoOtherDates(self):
        matches = []
        
        report = DateResultsReport()
        report.matches = matches
        report.date = datetime.date(2013, 3, 5)
        report.otherDates = []
        
        result = DateResults("").getReportContent(report)

        expectedResult = """
        <h1>Results: 5th March 2013</h1>
        <p>Results will be available once the season has started.</p>
        """
        
        self.assertMultiLineEqual(expectedResult, result)

    def testGetHeadingForDateReportNoDateSpecified(self):
        report = DateResultsReport()
        report.date = None
        result = DateResults("").getHeading(report)
        self.assertEquals("Results", result)
        
    def testGetHeadingForDateReportDateSpecified(self):
        report = DateResultsReport()
        report.date = datetime.date(1990, 3, 4)
        result = DateResults("").getHeading(report)
        self.assertEquals("Results: 4th March 1990", result)
        
    def testGetContentForDateNullDate(self):
        page = DateResults("")
        page.allParams = {"xmlFile": "data/2012-13.xml"}
        result = page.getContent()
        self.assertNotEqual("", result)

    def testGetContentForDateNonNullDate(self):
        page = DateResults("")
        page.allParams = {"xmlFile": "data/2012-13.xml", "date": "2012-12-23"}
        result = page.getContent()
        self.assertNotEqual("", result)

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOversNoRemainder']
    unittest.main()