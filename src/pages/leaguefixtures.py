'''
Created on 31 Jul 2013

@author: hicksj
'''
from pages.page import Page
from pages.pageLink import PageLink
from xml.etree import ElementTree
import string
from utils.dateformat import DateFormatter
from reports.leaguefixturesreport import LeagueFixturesReportGenerator
from operator import attrgetter

class LeagueFixtures(Page):

    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.report = None

    def getReport(self):
        if not self.report:
            leagueId = self.allParams.get('league', None)
            rootElement = ElementTree.parse(self.allParams["xmlFile"])
            self.report = LeagueFixturesReportGenerator().getReport(rootElement, leagueId)
        return self.report
    
    def getTitle(self):
        report = self.getReport()
        if report.leagueName is None:
            answer = "SEHICL Fixtures"
        else:
            answer = "SEHICL Fixtures: {league}".format(league=report.leagueName)
        return answer

    def getContent(self):
        report = self.getReport()
        answer = self.getReportContent(report)
        return answer
    
    def getReportContent(self, report): 
        html = """
        <h1>{heading}</h1>
        {body}
        """
        if len(report.matches) == 0:
            reportBody = "<p>There are no outstanding fixtures at present.</p>"
        else:
            reportBody = self.getFixtureList(report)
        theHeading = "Fixtures" if report.leagueName is None else report.leagueName
        answer = html.format(heading=theHeading, body=reportBody)
        return answer

    def getFixtureList(self, report):
        html = """ 
        <p class="noprint">Click on a team to see all matches for that team.</p>
        <table id="fixlist">
            {matches}
        </table>
        """
        matchesByDate = {}
        for m in report.matches:
            matchDate = m.date
            matchesForDate = matchesByDate.get(matchDate, None)
            if matchesForDate is None:
                matchesForDate = []
                matchesByDate[matchDate] = matchesForDate
            matchesForDate.append(m)
        dateLines = [self.getMatchLines(k, v) for k, v in sorted(matchesByDate.items())]
        answer = html.format(matches=string.join(dateLines, "\n")) 
        return answer
            
    def getMatchLines(self, theDate, matches):
        html = """
        <tbody class="nobreak">
        <tr>
            <td class="date" colspan="3">{date}</td>
        </tr>
        {matchLines}
        </tbody>
        """
        answer = ""
        if len(matches) > 0:
            prevTime = None
            mLines = []
            for m in sorted(matches, key=attrgetter("time", "court")):
                mLines.append(self.getMatchLine(m, prevTime))
                prevTime = m.time
            dateStr = DateFormatter.formatDate(theDate, True, True)
            answer = html.format(date=dateStr, matchLines=string.join(mLines, "\n"))
        return answer

    def getMatchLine(self, match, prevTime):
        html = """
        <tr>
            <td class="time">{time}</td>
            <td class="court">{court}</td>
            <td class="teams">
                <a href="{homefix.url}">{homename}</a> 
                v
                <a href="{awayfix.url}">{awayname}</a>
            </td>
            {leaguefix}
        </tr>
        """
        mTime = DateFormatter.formatTime(match.time) if prevTime != match.time else ""
        mCourt = match.court
        mHomeFixLink = PageLink("teamFixtures", self, {"team": match.homeTeamId}, True)
        mHomeName = match.homeTeamName
        mAwayFixLink = PageLink("teamFixtures", self, {"team": match.awayTeamId}, True)
        mAwayName = match.awayTeamName
        mLeagueFix = ""
        if match.leagueId is not None:
            lfHtml = """
            <td>
                <a href="{leaguefix.url}">{leaguename}</a>
            </td>
            """
            lFixLink = PageLink("leagueFixtures", self, {"league": match.leagueId}, True)
            mLeagueFix = lfHtml.format(leaguefix=lFixLink, leaguename=match.leagueName)
        answer = html.format(time=mTime, court=mCourt, homefix = mHomeFixLink, homename=mHomeName, awayfix=mAwayFixLink, awayname=mAwayName, leaguefix=mLeagueFix)
        return answer;