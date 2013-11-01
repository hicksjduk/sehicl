'''
Created on 8 Aug 2013

@author: hicksj
'''
from xml.etree import ElementTree
from pages.page import Page
from reports.tablesreport import LeagueTableReportGenerator
import string
from utils.dateformat import DateFormatter
from operator import attrgetter
from pages.pageLink import PageLink
from utils.text import TextUtils
from pages.archive import ArchiveUtils

class LeagueTable(Page):

    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.report = None
        
    def getReport(self):
        if not self.report:
            rootElement = ElementTree.parse(self.allParams["xmlFile"])
            leagueId = self.allParams.get('league', None)
            self.report = LeagueTableReportGenerator().getReport(rootElement, leagueId)
        return self.report

    def getTitle(self):
        report = self.getReport()
        if self.allParams.get("archive", "no") == "yes":
            answer = "SEHICL Archive: Season {0}".format(ArchiveUtils.getSeasonText(self.allParams.get("season")))
        elif len(report.tables) != 1:
            answer = "SEHICL Tables"
        else:
            answer = "SEHICL Table: {0}".format(report.tables[0].leagueName)
        return answer
    
    def getContent(self):
        report = self.getReport()
        answer = self.getReportContent(report)
        return answer
    
    def getReportContent(self, report):
        html = """
        {body}
        {footer}
        """
        answer = html.format(body=self.getReportBody(report), footer=self.getReportFooter())
        return answer
        
    def getReportBody(self, report):
        tables = []
        for t in report.tables:
            tables.append(self.getLeagueTable(t))
        answer = string.join(tables, "\n")
        return answer
    
    def getReportFooter(self):
        html = """
        <p class="calctext noprint">
        <b>How the points are worked out:</b>
        <br>
            12 points for a win, 6 points for a tie, 0 points for a loss.<br>
            Batting points: 1 point for every 10 runs scored in excess of 60, plus (only for teams
            batting second and winning) 1 point for each wicket in
            hand. A maximum of 6 points per innings.<br>
            Bowling points: 1 point per wicket taken. If the batting side has fewer than six players,
            and the missing player(s) would have been required to bat if present, a bowling bonus point is awarded
            for each missing player.<br>
            In a game won by default, the winning team receives 3 batting points and
            6 bowling points as well as 12 points for winning.
        <br>
        Teams level on points are ranked by
        <b>run rate</b>, which is the total number of runs scored, divided by the total
        number of overs faced. For this purpose, an innings where the batting
        side is all out counts as lasting the full number of available overs, even if it is actually shorter.</p>
        """
        answer = "" if self.allParams.get("archive", "no") == "yes" else html
        return answer
    
    def getLeagueTable(self, table):
        html = """
        <div class="nobreak">
        <h1>{heading}</h1>
        {status}
        {click}
        <table id="table">
            <thead>
                <tr>
                    <th class="position number"></th>
                    <th class="teamname"></th>
                    <th class="played number">P</th>
                    <th class="won number">W</th>
                    <th class="tied number">T</th>
                    <th class="lost number">L</th>
                    <th class="batpoints number">Bat</th>
                    <th class="bowlpoints number">Bowl</th>
                    <th class="runrate number">RR</th>
                    <th colspan="2">Ded</th>
                    <th class="points number">Pts</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
        {deductions}
        {notes}
        </div>
        """
        if self.allParams.get("archive", "no") == "yes":
            heading = "{0}: Season {1}".format(table.leagueName, ArchiveUtils.getSeasonText(self.allParams.get("season")))
            clickMessage = ""
        else:
            heading = table.leagueName
            clickMessage = "<p class=\"noprint\">Click on a team to see all matches for that team.</p>"
        statusMessage = self.getStatusMessage(table)
        deductionReasons = []
        tableRows = self.getRows(table, deductionReasons)
        theDeductions = self.getDeductionInfoForTable(deductionReasons)
        noteList = []
        for n in table.notes:
            note = "<p class=\"tablenotes\">{0}</p>".format(n)
            noteList.append(note)
        notes = string.join(noteList, "\n")
        answer = html.format(heading=heading, status=statusMessage, rows=tableRows, deductions=theDeductions, click=clickMessage, notes=notes)
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
            if table.lastCompleteMatchDate == table.lastScheduledMatchDate:
                message = "Final table"
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

    def getRows(self, table, deductionReasons):
        rows = []
        position = 0
        linePos = []
        if table.lastCompleteMatchDate is not None and table.lastCompleteMatchDate != table.lastScheduledMatchDate:
            if table.promoted != 0:
                linePos.append(table.promoted)
            if table.relegated != 0:
                linePos.append(len(table.tableRows) - table.relegated)
        prevPoints = 0
        prevRunRate = 0
        for tr in sorted(table.tableRows.values(), key=attrgetter("sortKey")):
            position = position + 1
            rows.append(self.getRow(tr, position, prevPoints, prevRunRate, deductionReasons))
            if position in linePos:
                rows.append(self.getLine())
            prevPoints, prevRunRate = tr.points, tr.runrate
        answer = string.join(rows, "\n")
        return answer

    def getLine(self):
        html = """
        <tr>
            <td colspan="12" class="linebelow">&nbsp;</td>
        </tr>
        """
        return html
    
    def getRow(self, tableRow, position, prevPoints, prevRunRate, deductionReasons):
        html = """
        <tr>
            <td class="position number">{position}</td>
            <td class="teamname {classes}">
                {team}
            </td>
            <td class="played number">{row.played}</td>
            <td class="won number">{row.won}</td>
            <td class="tied number">{row.tied}</td>
            <td class="lost number">{row.lost}</td>
            <td class="batpoints number">{row.batpoints}</td>
            <td class="bowlpoints number">{row.bowlpoints}</td>
            <td class="runrate number">{runrate}</td>
            <td class="dedpoints number">{dedpoints}</td>
            <td class="dedkeys">{dedkeys}</td>
            <td class="points number">{row.points}</td>
        </tr>
        """
        if position > 1 and tableRow.points == prevPoints and tableRow.runrate == prevRunRate:
            thePosition = ""
        else:
            thePosition = position
        theClasses = self.getMarkerClasses(tableRow, position)
        deductionKeys, deductedPoints = self.getDeductionInfoForRow(tableRow, deductionReasons)
        theRunRate = "" if tableRow.runrate == -1 else "{0:.2f}".format(tableRow.runrate)
        if self.allParams.get("archive", "no") == "yes":
            theTeam = tableRow.teamName
        else:
            theTeamFixLink = PageLink("teamFixtures", self, {"team": tableRow.teamId})
            theTeam = """
            <a href="{teamfix.url}">{row.teamName}</a>
            """.format(teamfix=theTeamFixLink, row=tableRow)
        answer = html.format(position=thePosition, classes=theClasses, team=theTeam, row=tableRow, dedpoints=deductedPoints, dedkeys=deductionKeys, runrate=theRunRate)
        return answer

    def getMarkerClasses(self, tableRow, position):
        classList = []
        if tableRow.champions:
            classList.append("champions")
        if tableRow.promoted or position in self.allParams.get("additionalPromotions", []):
            classList.append("promoted")
        if tableRow.relegated:
            classList.append("relegated")
        answer = string.join(classList)
        return answer
    
    def getDeductionReason(self, deduction):
        template = "{ded.reason} - {ded.points} {pointstext} deducted"
        answer = template.format(ded=deduction, pointstext=TextUtils.getGrammaticalNumber(deduction.points, "point", "points"))
        return answer

    def getDeductionInfoForRow(self, tableRow, deductionReasons):
        deductedPoints = 0
        deductionKeys = []
        for d in tableRow.deductions:
            deductedPoints = deductedPoints + d.points
            reason = self.getDeductionReason(d)
            if not reason in deductionReasons:
                deductionReasons.append(reason)
            deductionKeys.append(deductionReasons.index(reason) + 1)
        if len(deductionKeys) == 0:
            answer = ["", ""]
        else:
            deductionKeys = ["{0}".format(k) for k in sorted(deductionKeys)]
            answer = ["({0})".format(string.join(deductionKeys, ",")), deductedPoints]
        return answer
    
    def getDeductionInfoForTable(self, deductionReasons):
        html = """
        <ul class="deductions">
            {deductions}
        </ul>
        """
        if len(deductionReasons) == 0:
            answer = ""
        else:
            deductionList = []
            for i in range(0, len(deductionReasons)):
                deductionList.append(self.getDeductionListItem(deductionReasons[i], i + 1))
            answer = html.format(deductions=string.join(deductionList, "\n"))
        return answer

    def getDeductionListItem(self, deduction, index):
        html = """
        <li>
            <span class="dedkeys">({key})</span>
            {ded}.
        </li>
        """
        answer = html.format(key=index, ded=deduction)
        return answer