'''
Created on 8 Aug 2013

@author: hicksj
'''
from utils.dateformat import DateFormatter
from operator import attrgetter
import string

class LeagueTableReport:
    
    def __init__(self):
        self.tables = []

class LeagueTableInReport:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.leagueName = None
        self.promoted = 0
        self.relegated = 0
        self.tableRows = {}
        self.lastCompleteMatchDate = None
        self.lastScheduledMatchDate = None
        self.toCome = 0
        self.complete = False
        self.notes = []
        
class PointsDeduction:
        
        def __init__(self, points, reason):
            self.points = points
            self.reason = reason

class TableRow:
    
    def __init__(self, teamId, teamName):
        self.teamId = teamId
        self.teamName = teamName
        self.played = 0
        self.won = 0
        self.tied = 0
        self.lost = 0
        self.runs = 0
        self.balls = 0
        self.runrate = -1
        self.batpoints = 0
        self.bowlpoints = 0
        self.points = 0
        self.deductions = []
        self.minPosition = 0
        self.maxPosition = 0
        self.champions = False
        self.promoted = False
        self.relegated = False
        self.remainingOpponents = []
        self.maintainInvariants()
        
    def maintainInvariants(self):
        self.played = self.won + self.tied + self.lost
        self.runrate = -1 if self.balls == 0 else self.runs * 6.0 / self.balls
        points = 12 * self.won + 6 * self.tied + self.batpoints + self.bowlpoints
        for d in self.deductions:
            points = points - d.points
        self.points = points
        self.sortKey = "{0}{1:.15f}{2}".format(999-self.points, 98-self.runrate, self.teamName)

class LeagueTableReportGenerator:
    
    def __init__(self, awardedBatPts=3, awardedBowlPts=6):
        self.awardedBatPts = awardedBatPts
        self.awardedBowlPts = awardedBowlPts
        
    def getReport(self, rootElement, leagueId):
        answer = LeagueTableReport()
        for l in rootElement.findall("league"):
            if leagueId is None or l.get("id") == leagueId:
                answer.tables.append(self.getLeagueTable(l))
        return answer
    
    def getLeagueTable(self, leagueElement):
        answer = LeagueTableInReport()
        answer.leagueName = leagueElement.find("name").text
        elem = leagueElement.find("teamsPromoted")
        answer.promoted = 0 if elem is None else int(elem.text)
        elem = leagueElement.find("teamsRelegated")
        answer.relegated = 0 if elem is None else int(elem.text)
        answer.tableRows = self.createTableRows(leagueElement)
        lastCompleteMatchDate = None
        lastScheduledMatchDate = None
        incompleteMatchesByDate = {} 
        for m in leagueElement.findall("match"):
            complete = self.updateTableRowsFromMatch(m, answer.tableRows)
            date = DateFormatter.parseDateTimeFromString(m.find("date").text).date()
            if lastScheduledMatchDate is None or lastScheduledMatchDate < date:
                lastScheduledMatchDate = date
            if complete:
                if lastCompleteMatchDate is None or lastCompleteMatchDate < date:
                    lastCompleteMatchDate = date
            else:
                incompleteMatchesByDate[date] = incompleteMatchesByDate.get(date, 0) + 1
        answer.lastCompleteMatchDate = lastCompleteMatchDate
        answer.lastScheduledMatchDate = lastScheduledMatchDate
        answer.complete = len(incompleteMatchesByDate) == 0
        if lastCompleteMatchDate is not None:
            toCome = 0
            for d in sorted(incompleteMatchesByDate.keys()):
                if d > lastCompleteMatchDate:
                    break
                toCome = toCome + incompleteMatchesByDate[d]
            answer.toCome = toCome
        self.markPromotedRelegatedChampions(answer)
        tableNotesElement = leagueElement.find("tableNotes")
        tableNotesText = None if tableNotesElement is None else tableNotesElement.text
        if tableNotesText is not None:
            tableNotesText = tableNotesText.strip()
            answer.notes = [s.strip() for s in string.split(tableNotesText, "\n")]
        return answer
    
    def createTableRows(self, leagueElement):
        answer = {}
        for t in leagueElement.findall("team"):
            if t.find("excludedFromTables") is None:
                teamId = t.get("id")
                row = TableRow(teamId, t.find("name").text)
                answer[teamId] = row
                for d in t.findall("pointsDeduction"):
                    row.deductions.append(PointsDeduction(int(d.find("points").text), d.find("reason").text))
        return answer

    def updateTableRowsFromMatch(self, matchElement, tableRows):
        answer = False
        playedMatchElement = matchElement.find("playedMatch")
        if playedMatchElement is not None:
            answer = True
            for tableRow in self.getTableRowsForMatch(matchElement, tableRows):
                self.updateTableRowFromPlayedMatch(tableRow, playedMatchElement)
        else:
            awardedMatchElement = matchElement.find("awardedMatch")
            if awardedMatchElement is not None:
                answer = True
                for tableRow in self.getTableRowsForMatch(matchElement, tableRows):
                    self.updateTableRowFromAwardedMatch(tableRow, awardedMatchElement)
            else:
                for tableRow in self.getTableRowsForMatch(matchElement, tableRows):
                    self.updateTableRowFromUnplayedMatch(tableRow, matchElement)
        return answer
    
    def getTableRowsForMatch(self, matchElement, tableRows):
        answer = []
        for elem in ["homeTeam", "awayTeam"]:
            teamId = matchElement.find(elem).get("id")
            tableRow = tableRows.get(teamId)
            if tableRow is not None:
                answer.append(tableRow)
        return answer
    
    def updateTableRowFromPlayedMatch(self, tableRow, playedMatchElement):
        batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken = self.getScoreData(playedMatchElement, tableRow.teamId)
        self.updateTableRowFromMatchData(tableRow, batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken)
        
    def updateTableRowFromMatchData(self, tableRow, batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken):
        wonBattingSecond = False
        if scoreFor > scoreAgainst:
            tableRow.won = tableRow.won + 1
            wonBattingSecond = not batFirst
        elif scoreFor < scoreAgainst:
            tableRow.lost = tableRow.lost + 1
        else:
            tableRow.tied = tableRow.tied + 1
        tableRow.runs = tableRow.runs + scoreFor
        tableRow.balls = tableRow.balls + ballsFaced
        batPoints = self.calculateBattingPoints(scoreFor, wicketsLost if wonBattingSecond else None)
        tableRow.batpoints = tableRow.batpoints + batPoints
        tableRow.bowlpoints = tableRow.bowlpoints + wicketsTaken
        tableRow.maintainInvariants()
        
    def getScoreData(self, playedMatchElement, theTeamId):
        overLimitElement = playedMatchElement.find("overLimit")
        maxBalls = 6 * (12 if overLimitElement is None else int(overLimitElement.text))
        for t in playedMatchElement.findall("teamInMatch"):
            teamId = t.find("teamRef").get("id")
            inningsElement = t.find("innings")
            if teamId == theTeamId:
                batFirst = t.find("battingFirst").text == "true"
                scoreFor = int(inningsElement.find("runsScored").text)
                wicketsElement = inningsElement.find("wicketsLost")
                wicketsLost = 6 if wicketsElement is None else int(wicketsElement.text)
                if wicketsLost == 6:
                    ballsFaced = maxBalls
                else:
                    ballsElement = inningsElement.find("ballsBowled")
                    ballsFaced = maxBalls if ballsElement is None else int(ballsElement.text)
            else:
                scoreAgainst = int(inningsElement.find("runsScored").text)
                wicketsElement = inningsElement.find("wicketsLost")
                wicketsTaken = 6 if wicketsElement is None else int(wicketsElement.text)
        answer = [batFirst, scoreFor, ballsFaced, wicketsLost, scoreAgainst, wicketsTaken]
        return answer

    def calculateBattingPoints(self, runsScored, wicketsLost):
        runsPoints = max(runsScored - 60, 0) / 10
        wicketsPoints = 0 if wicketsLost is None else 6 - wicketsLost
        answer = min(runsPoints + wicketsPoints, 6)
        return answer
    
    def updateTableRowFromAwardedMatch(self, tableRow, awardedMatchElement):
        if awardedMatchElement.find("winner").get("id") == tableRow.teamId:
            tableRow.won = tableRow.won + 1
            tableRow.batpoints = tableRow.batpoints + self.awardedBatPts
            tableRow.bowlpoints = tableRow.bowlpoints + self.awardedBowlPts
        else:
            tableRow.lost = tableRow.lost + 1
        tableRow.maintainInvariants()
        
    def updateTableRowFromUnplayedMatch(self, tableRow, matchElement):
        homeTeam = matchElement.find("homeTeam").get("id")
        awayTeam = matchElement.find("awayTeam").get("id")
        if tableRow.teamId == homeTeam:
            tableRow.remainingOpponents.append(awayTeam)
        elif tableRow.teamId == awayTeam: 
            tableRow.remainingOpponents.append(homeTeam)
        
    def markPromotedRelegatedChampions(self, leagueTable):
        if leagueTable.complete:
            maxPromotedPos = leagueTable.promoted
            minRelegatedPos = len(leagueTable.tableRows) - leagueTable.relegated + 1
            pos = 0
            for row in sorted(leagueTable.tableRows.values(), key=attrgetter("sortKey")):
                pos = pos + 1
                row.champions = pos == 1
                row.promoted = pos <= maxPromotedPos
                row.relegated = pos >= minRelegatedPos
                