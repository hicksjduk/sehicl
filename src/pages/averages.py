'''
Created on 19 Aug 2013

@author: hicksj
'''
from pages.page import Page
from xml.etree import ElementTree
from reports.averagesreport import AveragesReportGenerator
from operator import itemgetter, attrgetter
import string
from pages.pageLink import PageLink
from utils.dateformat import DateFormatter
from utils.text import TextUtils
import re
from pages.archive import ArchiveUtils

class Averages(Page):

    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.report = None
        
    def getReport(self):
        if not self.report:
            rootElement = ElementTree.parse(self.allParams["xmlFile"])
            self.report = self.loadReport(rootElement)
        return self.report
    
    def getContent(self):
        report = self.getReport()
        answer = self.getReportContent(report)
        return answer
    
    def getReportContent(self, report):
        html = """
        <h1>{heading}</h1>
        {body}
        """
        answer = html.format(heading=self.getReportHeading(report), body=self.getReportBody(report))
        return answer
    
    def getReportBody(self, report):
        if report.lastCompleteMatchDate == None:
            answer = "<p>Averages will be available once the season has started.</p>"
        else:
            html = """
            {status}
            {data}
            """
            answer = html.format(status=self.getStatusMessage(report), data=self.getReportData(report))
        return answer
    
    def getStatusMessage(self, table):
        html = """
        <p class="statusMessage">{status}.</p>
        """
        if table.lastCompleteMatchDate is None:
            answer = ""
        elif self.allParams.get("archive", "no") == "yes":
            answer = ""
        else:
            if table.complete:
                message = "Final averages"
            else:
                dateStr = DateFormatter.formatDate(table.lastCompleteMatchDate, True, True)
                if table.toCome == 0:
                    template = "Includes all games up to and including {0}"
                    message = template.format(dateStr)
                else:
                    template = "Date of last game included: {0} ({1} {2} to come)"
                    message = template.format(dateStr, table.toCome, TextUtils.getGrammaticalNumber(table.toCome, "result", "results"))
            answer = html.format(status=message)
        return answer

    def getTeamNameHeader(self):
        html = """
        <th class="teamName name">Team</th>
        """
        answer = html
        return answer
        
    def getTeamNameColumn(self, row):
        html = """
        <td class="teamName name">
            {team}
        </td>
        """
        if self.allParams.get("archive", "no") == "yes":
            team = row.teamName
        else:
            link = PageLink("teamAverages", self, {"team": row.teamId})
            team = """
            <a href="{teamfix.url}#{anchor}">{row.teamName}</a>
            """.format(teamfix=link, row=row, anchor=self.getAnchorName())
        answer = html.format(team=team, row=row)
        return answer
        
class BattingAverages(Averages):
    
    def __init__(self, pageId, params={}):
        Averages.__init__(self, pageId, params)
    
    def loadReport(self, rootElement):
        leagueId = self.allParams.get("league", None)
        if leagueId == None:
            leagueIds = ["Division{0}".format(i) for i in range(1, 5)]
        else:
            leagueIds = [leagueId]
        answer = AveragesReportGenerator().getLeagueBattingAveragesReport(rootElement, leagueIds)
        if leagueId == None:
            answer.leagueName = "Senior"
        return answer
    
    def getTitle(self):
        if self.allParams.get("archive", "no") == "yes":
            answer = "SEHICL Archive: Season {0}".format(ArchiveUtils.getSeasonText(self.allParams.get("season")))
        else:
            report = self.getReport()
            answer = "SEHICL Averages: {0} Batting".format(report.leagueName)
        return answer
    
    def getReportHeading(self, report):
        if self.allParams.get("archive", "no") == "yes":
            answer = "{0} Batting: Season {1}".format(report.leagueName, ArchiveUtils.getSeasonText(self.allParams.get("season")))
        else:
            answer = "{0} Batting".format(report.leagueName)
        return answer
    
    def getReportData(self, report, maxRows=50):
        html = """
        <p>Players are ranked by runs scored.</p>
        {click}
        <table id="batav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    {team}
                    <th class="innings number">Inns</th>
                    <th class="notout number">NO</th>
                    <th class="runs number">Runs</th>
                    <th class="highscore number">HS</th>
                    <th class="average number">Average</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """
        teamHeader = self.getTeamNameHeader() if report.teamName is None else ""
        if report.teamName != None or self.allParams.get("archive", "no") == "yes":
            clickMessage = ""
        else:
            clickMessage = "<p class=\"noprint\">Click on a team to see the batting averages for that team.</p>" 
        answer = html.format(rows=self.getTableRows(report, maxRows), team=teamHeader, click=clickMessage)
        return answer
    
    def getTableRows(self, report, maxRows):
        rows = []
        count = 0
        lastRow = None
        for row in sorted(report.battingAverages, key=attrgetter("sortKey")):
            count = count + 1
            if lastRow is None or lastRow.runs != row.runs:
                if maxRows is not None and count > maxRows:
                    break
                row.position = count
            else:
                row.position = lastRow.position
            rows.append(self.getTableRow(row, row.position == count, report.teamName == None))
            lastRow = row
        answer = string.join(rows, "\n")
        return answer
    
    def getTableRow(self, row, includePosition, includeTeam):
        html = """
        <tr>
            <td class="position number">{position}</td>
            <td class="name">{row.playerName}</td>
            {team}
            <td class="innings number">{row.innings}</td>
            <td class="notout number">{row.notout}</td>
            <td class="runs number">{row.runs}</td>
            <td class="highscore number">{highscore}</td>
            <td class="average number">{average}</td>
        </tr>
        """
        thePosition = row.position if includePosition else ""
        theHighscore = "{0}{1}".format(row.highScore[0], "" if row.highScore[1] else "*")
        theAverage = "" if row.average == -1 else "{0:.2f}".format(row.average)
        theTeam = self.getTeamNameColumn(row) if includeTeam else ""
        answer = html.format(row=row, position=thePosition, highscore=theHighscore, average=theAverage, team=theTeam)
        return answer
    
    def getAnchorName(self):
        return "Batting"
    
class BowlingAverages(Averages):
    
    def __init__(self, pageId, params={}):
        Averages.__init__(self, pageId, params)

    def loadReport(self, rootElement):
        leagueId = self.allParams.get("league", None)
        if leagueId == None:
            leagueIds = ["Division{0}".format(i) for i in range(1, 5)]
        else:
            leagueIds = [leagueId]
        answer = AveragesReportGenerator().getLeagueBowlingAveragesReport(rootElement, leagueIds)
        if leagueId == None:
            answer.leagueName = "Senior"
        return answer
    
    def getTitle(self):
        if self.allParams.get("archive", "no") == "yes":
            answer = "SEHICL Archive: Season {0}".format(ArchiveUtils.getSeasonText(self.allParams.get("season")))
        else:
            report = self.getReport()
            answer = "SEHICL Averages: {0} Bowling".format(report.leagueName)
        return answer
    
    def getReportHeading(self, report):
        if self.allParams.get("archive", "no") == "yes":
            answer = "{0} Bowling: Season {1}".format(report.leagueName, ArchiveUtils.getSeasonText(self.allParams.get("season")))
        else:
            answer = "{0} Bowling".format(report.leagueName)
        return answer

    def getReportData(self, report, maxRows=50):
        html = """
        <p>Players (and bowling performances, for determining best bowling) are ranked by wickets taken, then average runs per over.</p>
        {click}
        <table id="bowlav">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="name">Name</th>
                    {team}
                    <th class="overs number">Overs</th>
                    <th class="runs number">Runs</th>
                    <th class="runs number">Wickets</th>
                    <th class="bestBowling number">Best</th>
                    <th class="averagePerWicket number">Runs/wkt</th>
                    <th class="averagePerOver number">Runs/over</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        """
        nameHeader = self.getTeamNameHeader() if report.teamName is None else ""   
        if report.teamName != None or self.allParams.get("archive", "no") == "yes":
            clickMessage = ""
        else:
            clickMessage = "<p class=\"noprint\">Click on a team to see the bowling averages for that team.</p>" 
        answer = html.format(rows=self.getTableRows(report, maxRows), team=nameHeader, click=clickMessage)
        return answer
    
    def getTableRow(self, row, includePosition, includeTeam):
        html = """
        <tr>
            <td class="position number">{position}</td>
            <td class="name">{row.playerName}</td>
            {team}
            <td class="overs number">{overs}</td>
            <td class="runs number">{row.runs}</td>
            <td class="wickets number">{row.wickets}</td>
            <td class="bestBowling number">{row.best[0]}/{row.best[1]}</td>
            <td class="averagePerWicket number">{avgPerWicket}</td>
            <td class="averagePerOver number">{avgPerOver}</td>
        </tr>
        """
        position = row.position if includePosition else ""
        overCount = row.balls / 6
        ballCount = row.balls % 6
        overs = overCount if ballCount == 0 else overCount + 0.1 * ballCount
        avgPerWicket, avgPerOver = ["" if avg == -1 else "{0:.2f}".format(avg) for avg in [row.averagePerWicket, row.averagePerOver]]
        team = self.getTeamNameColumn(row) if includeTeam else ""
        answer = html.format(row=row, position=position, overs=overs, avgPerWicket=avgPerWicket, avgPerOver=avgPerOver, team=team)
        return answer
    
    def getTableRows(self, report, maxRows):
        rows = []
        count = 0
        lastRow = None
        for row in sorted(report.bowlingAverages, key=attrgetter("sortKey")):
            count = count + 1
            if lastRow is None or lastRow.wickets != row.wickets or lastRow.averagePerOver != row.averagePerOver:
                if maxRows is not None and count > maxRows:
                    break
                row.position = count
            else:
                row.position = lastRow.position
            rows.append(self.getTableRow(row, row.position == count, report.teamName is None))
            lastRow = row
        answer = string.join(rows, "\n")
        return answer
    
    def getAnchorName(self):
        return "Bowling"

class TeamAverages(Averages):
    
    def __init__(self, pageId, params={}):
        Averages.__init__(self, pageId, params)

    def loadReport(self, rootElement):
        teamId = self.allParams.get("team")
        answer = AveragesReportGenerator().getTeamAveragesReport(rootElement, teamId)
        return answer

    def getTitle(self):
        report = self.getReport()
        answer = "SEHICL Averages: {0} ({1})".format(report.teamName, report.leagueName)
        return answer

    def getReportHeading(self, report):
        answer = "{0} ({1})".format(report.teamName, report.leagueName)
        return answer
    
    def getReportData(self, report):
        html = """
        <h2>
            <a id="Batting">Batting</a>
        </h2>
        {batting}
        <h2>
            <a id="Bowling">Bowling</a>
        </h2>
        {bowling}
        """
        batting = BattingAverages("").getReportData(report, None)
        bowling = BowlingAverages("").getReportData(report, None)
        answer = html.format(batting=batting, bowling=bowling)
        return answer

class TeamAveragesIndex(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.report = None
        
    def getReport(self):
        if not self.report:
            rootElement = ElementTree.parse(self.allParams["xmlFile"])
            self.report = self.loadReport(rootElement, self.allParams)
        return self.report
    
    def loadReport(self, rootElement, params):
        answer = AveragesReportGenerator().getAllTeamsByLeague(rootElement)
        return answer
    
    def getTitle(self):
        answer = "SEHICL Averages: By team"
        return answer
    
    def getContent(self):
        html = """
        <h1>Averages by team</h1>
        <table id="avgeindex">
        {rows}
        </table>
        """
        report = self.getReport()
        answer = html.format(rows=self.getRows(report))
        return answer
    
    def getRows(self, report):
        rows = []
        leaguesPerRow = 2
        leaguesBySortKey = {}
        for league in report.keys():
            sk = self.getLeagueSortKey(league[1])
            leaguesBySortKey[sk] = league
        leaguesForRow = []
        for sk in sorted(leaguesBySortKey.keys()):
            league = leaguesBySortKey[sk]
            leaguesForRow.append(league)
            if len(leaguesForRow) == leaguesPerRow:
                rows.append(self.getRow(report, leaguesForRow))
                leaguesForRow = []
        if len(leaguesForRow) > 0:
            rows.append(self.getRow(report, leaguesForRow))
        answer = string.join(rows, "\n")
        return answer

    def getLeagueSortKey(self, leagueName):
        numerics = re.findall("[0-9]+", leagueName)
        if len(numerics) == 0:
            answer = 0
        else:
            num = int(numerics[0])
            answer = num if num < 10 else 30 - num
        return answer

    def getRow(self, report, leagues):
        html = """
        <tr>
        {leagues}
        </tr>
        """
        cells = [self.getLeagueCell(report, league) for league in leagues]
        answer = html.format(leagues=string.join(cells, "\n"))
        return answer
    
    def getLeagueCell(self, report, league):
        html = """
        <td>
            <h3 class="divheading">{name}</h3>
            <table>
                {teams}
            </table>
        </td>
        """
        teamCells = [self.getTeamCell(team) for team in sorted(report[league], key=itemgetter(1))]
        teams = string.join(teamCells, "\n")
        answer = html.format(name=league[1], teams=teams)
        return answer
    
    def getTeamCell(self, team):
        html = """
        <tr>
            <td class="teamName">
                <a href="{link.url}">{name}</a>
            </td>
            <td class="batLink">
                <a href="{link.url}#Batting">Batting</a>
            </td>
            <td class="bowlLink">
                <a href="{link.url}#Bowling">Bowling</a>
            </td>
        </tr>
        """
        answer = html.format(name=team[1], link=PageLink("teamAverages", self, {"team": team[0]}))
        return answer
    
class AveragesIndex(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)

    def getTitle(self):
        answer = "SEHICL Averages"
        return answer
    
    def getContent(self):
        html="""
        <h1>Averages</h1>
        <p>Click one of the links below to view the current league averages.</p>
        <ul>
            <li>
                <a href="{seniorbat.url}">Senior batting</a>
            </li>
            <li>
                <a href="{seniorbowl.url}">Senior bowling</a>
            </li>
            <li>
                <a href="{u16bat.url}">Colts Under-16 batting</a>
            </li>
            <li>
                <a href="{u16bowl.url}">Colts Under-16 bowling</a>
            </li>
            <li>
                <a href="{u13bat.url}">Colts Under-13 batting</a>
            </li>
            <li>
                <a href="{u13bowl.url}">Colts Under-13 bowling</a>
            </li>
            <li>
                <a href="{byteam.url}">Averages for a specific team</a>
            </li>
        </ul>
        """
        seniorbat = PageLink("battingAverages", self)
        seniorbowl = PageLink("bowlingAverages", self)
        u16bat = PageLink("leagueBattingAverages", self, {"league": "ColtsUnder16"})
        u16bowl = PageLink("leagueBowlingAverages", self, {"league": "ColtsUnder16"})
        u13bat = PageLink("leagueBattingAverages", self, {"league": "ColtsUnder13"})
        u13bowl = PageLink("leagueBowlingAverages", self, {"league": "ColtsUnder13"})
        byteam = PageLink("teamAveragesIndex", self)
        answer = html.format(seniorbat=seniorbat, seniorbowl=seniorbowl, u16bat=u16bat, u16bowl=u16bowl, u13bat=u13bat, u13bowl=u13bowl, byteam=byteam)
        return answer