'''
Created on 6 Aug 2013

@author: hicksj
'''
from pages.page import Page
from xml.etree import ElementTree
from reports.resultsreport import ResultsReportGenerator
from utils.dateformat import DateFormatter
from operator import attrgetter
import string
from pages.pageLink import PageLink
import re
from utils.text import TextUtils

class Results(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.report = None
        
    def getReport(self):
        if not self.report:
            rootElement = ElementTree.parse(self.allParams["xmlFile"])
            self.report = self.loadReport(rootElement)
        return self.report

    def getOversText(self, balls):
        overs = balls // 6
        remainder = balls % 6
        if remainder == 0:
            answer = "{0}".format(overs)
        else:
            answer = "{0}.{1}".format(overs, remainder)
        return answer

    def getBattingHighlight(self, highlight):
        xml = """
        <span class="nolinewrap">{name} {runs}{notout}</span> {notes}        
        """
        theName = highlight.playerName
        theRuns = highlight.runs
        notOutStar = "" if highlight.out else "*"
        theNotes = "" if highlight.notes is None else "({0})".format(highlight.notes)
        answer = xml.format(name=theName, runs=theRuns, notout=notOutStar, notes=theNotes).strip()
        return answer

    def getBowlingHighlight(self, highlight):
        xml = """
        <span class="nolinewrap">{name} {wickets}/{runs}</span> {notes}
        """
        theName = highlight.playerName
        theRuns = highlight.runs
        theWickets = highlight.wickets
        theNotes = "" if highlight.notes is None else "({0})".format(highlight.notes)
        answer = xml.format(name=theName, runs=theRuns, wickets=theWickets, notes=theNotes).strip()
        return answer
        
    def getScoreText(self, runs, wickets):
        wicketText = "all out" if wickets == 6 else "for {0}".format(wickets)
        answer = "{0} {1}".format(runs, wicketText)
        return answer
    
    def getScoreLine(self, innings1, innings2, homeTeamId, awayTeamId):
        html = """
        <tr>
            <td class="teamscore">
                {anchor}
                {score1}
            </td>
            <td class="teamscore">
                {score2}
            </td>
        </tr>
        """
        answer = html.format(anchor=self.getMatchAnchor(homeTeamId, awayTeamId), score1=self.getScore(innings1), score2=self.getScore(innings2))
        return answer

    def getScore(self, innings):
        html = """
        <a href="{teamlink.url}">{name}</a> {score} ({overs} ov)
        """
        theLink = PageLink("teamFixtures", self, {"team": innings.teamId})
        theName = innings.teamName
        theScore = self.getScoreText(innings.runs, innings.wickets)
        theOvers = self.getOversText(innings.balls)
        answer = html.format(teamlink=theLink, name=theName, score=theScore, overs=theOvers)
        return answer
    
    def getHighlightsLine(self, innings1, innings2):
        html = """
        <tr>
            <td class="highlights">
                {highlights1}
            </td>
            <td class="highlights">
                {highlights2}
            </td>
        </tr>
        """
        h1 = self.getInningsHighlights(innings1)
        h2 = self.getInningsHighlights(innings2)
        answer = html.format(highlights1=h1, highlights2=h2) if h1 or h2 else ""
        return answer
        
    def getInningsHighlights(self, innings):
        highlights = []
        for h in sorted(innings.batHighlights, key=attrgetter("sortKey")):
            highlights.append(self.getBattingHighlight(h))
        for h in sorted(innings.bowlHighlights, key=attrgetter("sortKey")):
            highlights.append(self.getBowlingHighlight(h))
        answer = string.join(highlights, ",\n")
        return answer

    def getResultLine(self, innings1, innings2):
        html = """
        <tr>
            <td colspan="2" class="result">
                {result}
            </td>
        </tr>
        """
        answer = html.format(result=self.getResultText(innings1, innings2))
        return answer
    
    def getResultText(self, innings1, innings2):
        difference = innings1.runs - innings2.runs
        if difference == 0:
            answer = "Match tied"
        elif difference > 0:
            answer = "{0} won by {1} {2}".format(innings1.teamName, difference, TextUtils.getGrammaticalNumber(difference, "run", "runs"))
        else:
            wicketsInHand = 6 - innings2.wickets
            answer = "{0} won by {1} {2}".format(innings2.teamName, wicketsInHand, TextUtils.getGrammaticalNumber(wicketsInHand, "wicket", "wickets"))
        return answer
    
    def getPlayedMatchResult(self, match):
        html = """
            {scores}
            {highlights}
            {result}
        """
        innings1, innings2 = sorted(match.innings.values(), key=attrgetter("first"), reverse=True)
        theScores = self.getScoreLine(innings1, innings2, match.homeTeamId, match.awayTeamId)
        theHighlights = self.getHighlightsLine(innings1, innings2)
        theResult = self.getResultLine(innings1, innings2)
        answer = html.format(scores=theScores, highlights=theHighlights, result=theResult)
        return answer
    
    def getAwardedMatchResult(self, match):
        html = """
        <tr>
            <td colspan="2" class="teamscore">
                {anchor}
                <a href="{winnerlink.url}">{winnername}</a>
                beat
                <a href="{loserlink.url}">{losername}</a>
                by default ({reason})
            </td>
        </tr>
        """
        theAnchor = self.getMatchAnchor(match.homeTeamId, match.awayTeamId)
        awardedDetails = match.award
        theWinnerLink = PageLink("teamFixtures", self, {"team": awardedDetails.winnerId})
        theWinnerName = awardedDetails.winnerName
        theLoserLink = PageLink("teamFixtures", self, {"team": awardedDetails.loserId})
        theLoserName = awardedDetails.loserName
        theReason = awardedDetails.reason
        answer = html.format(anchor=theAnchor, winnerlink = theWinnerLink, winnername=theWinnerName, loserlink=theLoserLink, losername=theLoserName, reason=theReason)
        return answer
        
    def getMatchAnchor(self, homeTeamId, awayTeamId):
        html = """
        <a id="{homeid}{awayid}"></a>
        """
        answer = html.format(homeid=homeTeamId, awayid=awayTeamId)
        return answer
    
    def getMatchResult(self, match):
        if match.innings is not None:
            answer = self.getPlayedMatchResult(match)
        elif match.award is not None:
            answer = self.getAwardedMatchResult(match)
        return answer
    
class LeagueResults(Results):
    
    def __init__(self, pageId, params={}):
        Results.__init__(self, pageId, params)

    def loadReport(self, rootElement):
        leagueId = self.allParams.get('league', None)
        if not leagueId:
            raise NameError("League ID not specified")
        answer = ResultsReportGenerator().getLeagueResultsReport(rootElement, leagueId)
        return answer
    
    def getTitle(self):
        report = self.getReport()
        answer = "SEHICL Results: {0}".format(report.leagueName)
        return answer
    
    def getContent(self):
        report = self.getReport()
        answer = self.getReportContent(report)
        return answer
    
    def getReportContent(self, report):
        html = """
        <h1>{leaguename}</h1>
        {body}
        """
        if len(report.matches) == 0:
            reportBody = "<p>Results will be available once the season has started.</p>"
        else:
            reportBody = self.getReportBody(report)
        answer = html.format(leaguename=report.leagueName, body=reportBody)
        return answer
    
    def getReportBody(self, report):
        html = """
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
            {results}
        </table>
        """
        matchesByDate = {} 
        for m in report.matches:
            matches = matchesByDate.get(m.date, None)
            if matches is None:
                matches = []
                matchesByDate[m.date] = matches
            matches.append(m)
        resList = []
        for d in sorted(matchesByDate.keys(), reverse=True):
            resList.append(self.getResultsForDate(d, matchesByDate[d]))
        answer = html.format(results=string.join(resList, "\n"))
        return answer
    
    def getResultsForDate(self, theDate, matches):
        html = """
        <tr>
            <td class="date" colspan="2">{date}</td>
        </tr>
        {results}
        """
        resList = []
        for m in sorted(matches, key=attrgetter("time", "court")):
            resList.append(self.getMatchResult(m))
        answer = html.format(date=DateFormatter.formatDate(theDate, True, True), results=string.join(resList, "\n"))
        return answer
    
class DateResults(Results):
    
    def __init__(self, pageId, params={}):
        Results.__init__(self, pageId, params)

    def loadReport(self, rootElement):
        dateStr = self.allParams.get('date', None)
        date = None if dateStr is None else DateFormatter.parseDateFromString(dateStr)
        answer = ResultsReportGenerator().getDateResultsReport(rootElement, date)
        return answer

    def getTitle(self):
        report = self.getReport()
        if report.date is None:
            answer = "SEHICL Results"
        else:
            answer = "SEHICL Results: {0}".format(DateFormatter.formatDate(report.date, True, True))
        return answer
    
    def getContent(self):
        report = self.getReport()
        answer = self.getReportContent(report)
        return answer

    def getReportContent(self, report):
        html = """
        <h1>{heading}</h1>
        {otherdates}
        {body}
        """
        if len(report.matches) == 0 and len(report.otherDates) == 0:
            reportBody = "<p>Results will be available once the season has started.</p>"
        else:
            reportBody = self.getReportBody(report)
        answer = html.format(heading=self.getHeading(report), otherdates=self.getOtherDateLinks(report), body=reportBody)
        return answer
    
    def getHeading(self, report):
        if report.date is None:
            answer = "Results"
        else:
            answer = "Results: {0}".format(DateFormatter.formatDate(report.date, True, True))
        return answer
    
    def getOtherDateLinks(self, report):
        html = """
        <ul id="datenav" class="noprint">
        <li>Results on other dates:</li>
        {datelinks}
        </ul>
        """
        linkHtml = """
        <li>
            <a href="{datelink.url}">{date}</a>
        </li>
        """ 
        dates = {}
        for d in report.otherDates:
            isoDate = DateFormatter.formatDateToISO(d)
            dateStr = DateFormatter.formatDate(d, False, None)
            dates[isoDate] = dateStr
        if len(dates) == 0:
            answer = ""
        else:
            linkData = []
            for isoDate in sorted(dates.keys(), reverse=True):
                dateStr = dates[isoDate]
                if len(linkData) == 0 and self.allParams.get("date", None) is not None:
                    link = PageLink("latestResults", self)
                else:
                    link = PageLink("dateResults", self, {"date": isoDate})
                linkData.append(linkHtml.format(datelink=link, date=dateStr))
            answer = html.format(datelinks=string.join(linkData, "\n"))
        return answer
                
    def getReportBody(self, report):
        html = """
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="reslist">
            {results}
        </table>
        """
        matchesByLeague = {} 
        for m in report.matches:
            key = self.getLeagueSortKey(m.leagueName)
            matches = matchesByLeague.get(key, None)
            if matches is None:
                matches = []
                matchesByLeague[key] = matches
            matches.append(m)
        resList = []
        for k in sorted(matchesByLeague.keys()):
            resList.append(self.getResultsForLeague(matchesByLeague[k]))
        answer = html.format(results=string.join(resList, "\n"))
        return answer
        
    def getLeagueSortKey(self, leagueName):
        numerics = re.findall("[0-9]+", leagueName)
        if len(numerics) == 0:
            answer = 0
        else:
            num = int(numerics[0])
            answer = num if num < 10 else 30 - num
        return answer
    
    def getResultsForLeague(self, matches):
        html = """
        <tr>
            <td class="division" colspan="2">{leaguename}</td>
        </tr>
        {results}
        """
        theLeagueName = matches[0].leagueName
        resList = []
        for m in sorted(matches, key=attrgetter("time", "court")):
            resList.append(self.getMatchResult(m))
        answer = html.format(leaguename=theLeagueName, results=string.join(resList, "\n"))
        return answer
    