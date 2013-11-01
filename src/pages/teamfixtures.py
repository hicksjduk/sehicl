'''
Created on 31 Jul 2013

@author: hicksj
'''
from pages.page import Page
from pages.pageLink import PageLink
from xml.etree import ElementTree
import string
from utils.dateformat import DateFormatter
from reports.teamfixturesreport import TeamFixturesReportGenerator

class TeamFixtures(Page):

    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.report = None
    
    def getReport(self):
        if not self.report:
            teamId = self.allParams.get('team', None)
            if not teamId:
                raise NameError("Team ID not specified")
            rootElement = ElementTree.parse(self.allParams["xmlFile"])
            self.report = TeamFixturesReportGenerator().getReport(rootElement, teamId)
        return self.report
    
    def getTitle(self):
        report = self.getReport()
        answer = "SEHICL Fixtures: {team} ({league})".format(team=report.teamName, league=report.leagueName)
        return answer

    def getContent(self):
        report = self.getReport()
        answer = self.getReportContent(report)
        return answer
    
    def getReportContent(self, report): 
        html = """
        <h1>{teamname} (<a href="{leaguefix.url}">{leaguename}</a>)</h1>
        {body}
        """

        leagueFixLink = PageLink("leagueFixtures", self, {"league": report.leagueId})
        if len(report.matches) == 0:
            reportBody = "<p>The fixtures for the coming season have not yet been published.</p>"
        else:
            reportBody = self.getFixtureList(report)
        answer = html.format(teamname=report.teamName, leaguefix=leagueFixLink, leaguename=report.leagueName, body=reportBody)
        return answer

    def getFixtureList(self, report):
        html = """ 
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
                {matches}
            </tbody>
        </table>
        """
        
        leagueResLink = PageLink("leagueResults", self, {"league": report.leagueId})
        matchLines = [self.getMatchLine(match, report.teamId, leagueResLink) for match in report.getSortedMatches()]
        answer = html.format(matches=string.join(matchLines, "\n")) 
        return answer
            
    def getMatchLine(self, match, teamId, leagueResLink):
        html = """
        <tr>
            <td class="date">{date}</td>
            <td class="time">{time}</td>
            <td class="court">{court}</td>
            <td class="opponent"><a href="{oppfix.url}">{oppname}</a></td>
            <td class="homeAway">{homeaway}</td>
            <td class="result">{result}</td>
        </tr>
        """
        mDate = DateFormatter.formatDate(match.datetime, False, False)
        mTime = DateFormatter.formatTime(match.datetime)
        mCourt = match.court
        mOppFixLink = PageLink("teamFixtures", self, {"team": match.opponentId})
        mOppName = match.opponentName
        mHomeAway = "H" if match.home else "A"
        mOppId = match.opponentId
        mHomeId = teamId if match.home else mOppId
        mAwayId = mOppId if match.home else teamId 
        if match.result:
            if match.margin:
                res = "{0} by {1}".format(match.result, match.margin)
            else:
                res = "{0}".format(match.result)
            mResult = "<a href=\"{leaguefix.url}#{homeid}{awayid}\">{result}</a>".format(leaguefix=leagueResLink, teamid=teamId, homeid=mHomeId, awayid=mAwayId, result=res)
        else:
            mResult = ""
        answer = html.format(date=mDate, time=mTime, court=mCourt, oppfix = mOppFixLink, oppname=mOppName, homeaway=mHomeAway, result=mResult)
        return answer;