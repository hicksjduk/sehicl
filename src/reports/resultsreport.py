'''
Created on 5 Aug 2013

@author: hicksj
'''
from utils.dateformat import DateFormatter
import string

class ResultsReport:
    '''
    classdocs
    '''
    def __init__(self):
        self.matches = []
        
class LeagueResultsReport(ResultsReport):
    
    def __init__(self):
        self.leagueId = None
        self.leagueName = None
        
class DateResultsReport(ResultsReport):
    
    def __init__(self):
        self.date = None
        self.otherDates = None
        
class MatchInReport:
    
    def __init__(self):
        self.date = None
        self.time = None
        self.court = None
        self.homeTeamId = None
        self.homeTeamName = None
        self.awayTeamId = None
        self.awayTeamName = None
        self.leagueName = None
        self.innings = None
        self.award = None
        
class InningsInMatch:
    
    def __init__(self):
        self.first = False
        self.teamId = None
        self.teamName = None
        self.runs = 0
        self.wickets = 0
        self.balls = 0
        self.batHighlights = []
        self.bowlHighlights = []
        
class AwardDetails:
    
    def __init__(self):
        self.winnerId = None
        self.winnerName = None
        self.loserId = None
        self.loserName = None
        self.reason = None

class Performance:
    
    def __init__(self, playerName):
        self.playerName = playerName

    def getPlayerSortKey(self):
        answer = ""
        if self.playerName is not None:
            words = string.split(self.playerName, " ", 1)
            answer = string.join(reversed(words), "")
        return answer
        
class BattingPerformance(Performance):
    
    def __init__(self, playerName, runs, out, notes):
        Performance.__init__(self, playerName)
        self.runs = runs
        self.out = out
        self.notes = notes
        self.sortKey = "{0}{1}".format(999-runs, self.getPlayerSortKey())
        
class BowlingPerformance(Performance):
    
    def __init__(self, playerName, runs, wickets, notes):
        Performance.__init__(self, playerName)
        self.runs = runs
        self.wickets = wickets
        self.notes = notes
        self.sortKey = "{0}{1}".format((9 - wickets) * 1000 + runs, self.getPlayerSortKey())

class ResultsReportGenerator:
    
    def getLeagueResultsReport(self, rootElement, leagueId):
        answer = LeagueResultsReport()
        leagueElement = None
        for l in rootElement.findall("league"):
            if l.get("id") == leagueId:
                leagueElement = l;
                break
        if leagueElement is not None:
            answer.leagueId = leagueId;
            answer.leagueName = leagueElement.find("name").text
            answer.matches = self.getCompletedMatchesForLeague(leagueElement)
        return answer
    
    def getDateResultsReport(self, rootElement, date):
        answer = DateResultsReport()
        if date is None:
            allDates = self.getAllMatchDatesWithCompletedMatches(rootElement)
            if len(allDates) > 0:
                date = sorted(allDates, reverse=True)[0]
        answer.date = date
        answer.otherDates = self.getAllMatchDatesWithCompletedMatches(rootElement, date)
        answer.matches = self.getCompletedMatchesForDate(rootElement, date)
        return answer

    def getCompletedMatchesForDate(self, rootElement, date):
        answer = []
        for l in rootElement.findall("league"):
            teams, players = self.getTeamsAndPlayers(l)
            answer.extend(self.getCompletedMatches(l, teams, players, date))
        return answer
    
    def getCompletedMatches(self, leagueElement, teams, players, date=None):
        answer = []
        for m in leagueElement.findall("match"):
            if (date is None or self.isOnDate(m, date)) and self.isComplete(m):
                answer.append(self.getMatch(m, teams, players, leagueElement.find("name").text))
        return answer
    
    def getCompletedMatchesForLeague(self, leagueElement):
        teams, players = self.getTeamsAndPlayers(leagueElement)
        answer = self.getCompletedMatches(leagueElement, teams, players)
        return answer
    
    def getAllMatchDatesWithCompletedMatches(self, rootElement, dateToExclude=None):
        answer = set()
        for l in rootElement.findall("league"):
            for m in l.findall("match"):
                if self.isComplete(m):
                    date = DateFormatter.parseDateTimeFromString(m.find("date").text).date()
                    if date != dateToExclude: 
                        answer.add(date)
        return answer
    
    def getTeamsAndPlayers(self, leagueElement):
        teams = {}
        players = {}
        for t in leagueElement.findall("team"):
            teams[t.get("id")] = t.find("name").text
            for p in t.findall("player"):
                players[p.get("id")] = p.find("name").text
        answer = (teams, players)
        return answer
            
    def isOnDate(self, matchElement, date):
        mDate = DateFormatter.parseDateTimeFromString(matchElement.find("date").text).date()
        answer = mDate == date
        return answer
    
    def isComplete(self, matchElement):
        answer = matchElement.find("playedMatch") is not None or\
                matchElement.find("awardedMatch") is not None
        return answer
    
    def getMatch(self, matchElement, teams, players, leagueName):
        answer = MatchInReport()
        dateTime = DateFormatter.parseDateTimeFromString(matchElement.find("date").text)
        answer.date = dateTime.date()
        answer.time = dateTime.time()
        answer.court = matchElement.find("pitch").text
        htElement = matchElement.find("homeTeam")
        homeTeamId = htElement.get("id")
        answer.homeTeamId = homeTeamId
        answer.homeTeamName = teams.get(homeTeamId) 
        awayTeamId = matchElement.find("awayTeam").get("id")
        answer.awayTeamId = awayTeamId
        answer.awayTeamName = teams.get(awayTeamId)
        answer.leagueName = leagueName
        playedMatchElement = matchElement.find("playedMatch")
        if playedMatchElement is not None:
            answer.innings = self.getInningsList(playedMatchElement, teams, players)
        awardedMatchElement = matchElement.find("awardedMatch")
        if awardedMatchElement is not None:
            answer.award = self.getAwardedMatchDetails(awardedMatchElement, homeTeamId, awayTeamId, teams)
        return answer
    
    def getInningsList(self, playedMatchElement, teams, players):
        answer = {}
        maxOversElement = playedMatchElement.find("overLimit")
        maxOvers = 12 if maxOversElement is None else int(maxOversElement.text)
        for t in playedMatchElement.findall("teamInMatch"):
            teamId = t.find("teamRef").get("id")
            teamName = teams[teamId]
            inningsElement = t.find("innings")
            if inningsElement is not None:
                answer[teamId] = self.getInnings(inningsElement, teamId, teamName, t.find("battingFirst").text == "true", 6 * maxOvers, players)
        return answer
    
    def getInnings(self, inningsElement, teamId, teamName, batFirst, maxBalls, players):
        answer = InningsInMatch()
        answer.first = batFirst
        answer.teamId = teamId
        answer.teamName = teamName
        answer.runs = int(inningsElement.find("runsScored").text)
        wicketsElement = inningsElement.find("wicketsLost")
        answer.wickets = 6 if wicketsElement is None else int(wicketsElement.text)
        ballsElement = inningsElement.find("ballsBowled")
        answer.balls = maxBalls if ballsElement is None else int(ballsElement.text)
        answer.batHighlights = self.getBattingHighlights(inningsElement, players)
        answer.bowlHighlights = self.getBowlingHighlights(inningsElement, players)
        return answer
    
    def getBattingHighlights(self, inningsElement, players):
        answer = []
        for b in inningsElement.findall("batsman"):
            runs = int(b.find("runs").text)
            if runs >= 20:
                name = players.get(b.get("player"))
                out = b.find("out").text == "true"
                notesElement = b.find("notes")
                notes = None if notesElement is None else notesElement.text
                answer.append(BattingPerformance(name,runs, out, notes))
        return answer
    
    def getBowlingHighlights(self, inningsElement, players):
        answer = []
        for b in inningsElement.findall("bowler"):
            wickets = int(b.find("wickets").text)
            if wickets >= 2:
                name = players.get(b.get("player"))
                runs = int(b.find("runs").text)
                notesElement = b.find("notes")
                notes = None if notesElement is None else notesElement.text
                answer.append(BowlingPerformance(name, runs, wickets, notes))
        return answer
    
    def getAwardedMatchDetails(self, awardedMatchElement, homeTeamId, awayTeamId, teams):
        answer = AwardDetails()
        answer.reason = awardedMatchElement.find("reason").text
        winnerId = awardedMatchElement.find("winner").get("id")
        answer.winnerId = winnerId
        answer.winnerName = teams[winnerId]
        loserId = homeTeamId if winnerId == awayTeamId else awayTeamId
        answer.loserId = loserId
        answer.loserName = teams[loserId]
        return answer
    