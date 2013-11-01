'''
Created on 31 Jul 2013

@author: hicksj
'''

from utils.dateformat import DateFormatter

class LeagueFixturesReport:
    '''
    classdocs
    '''

    def __init__(self):
        self.leagueId = None
        self.leagueName = None
        self.matches = []
        
class MatchInReport:
     
    def __init__(self):
        self.date = None
        self.time = None
        self.court = None
        self.homeTeamId = None
        self.homeTeamName = None
        self.awayTeamId = None
        self.awayTeamName = None
        self.leagueId = None
        self.leagueName = None
        
class LeagueFixturesReportGenerator:

    def getReport(self, rootElement, leagueId):
        answer = LeagueFixturesReport()
        leagueElements = self.getLeagueElements(rootElement, leagueId)
        if leagueId is not None and len(leagueElements) == 1:
            answer.leagueId = leagueId
            answer.leagueName = leagueElements[0].find("name").text
        matches = []
        for l in leagueElements:
            matches = self.getIncompleteMatchElements(l)
            teams = self.getTeamNames(l)
            for m in matches:
                answer.matches.append(self.getMatch(m, teams, l if leagueId is None else None))
        return answer
    
    def getLeagueElements(self, rootElement, leagueId):
        allLeagues = rootElement.findall("league")
        if leagueId is None:
            answer = allLeagues
        else:
            answer = []
            for l in allLeagues:
                if l.get("id") == leagueId:
                    answer = [l]
                    break
        return answer
    
    def getTeamNames(self, leagueElement):
        answer = {}
        for t in leagueElement.findall("team"):
            answer[t.get("id")] = t.find("name").text
        return answer
    
    def getIncompleteMatchElements(self, leagueElement):
        answer = []
        for m in leagueElement.findall("match"):
            if not self.isMatchComplete(m):
                answer.append(m)
        return answer
    
    def isMatchComplete(self, matchElement):
        answer = matchElement.find("awardedMatch") is not None or\
            matchElement.find("playedMatch") is not None
        return answer
    
    def getInningsData(self, teamInMatchElement, maxBalls):
        answer = {}
        answer["batFirst"] = teamInMatchElement.find("battingFirst").text == "true"
        inningsElement = teamInMatchElement.find("innings")
        answer["runs"] = int(inningsElement.find("runsScored").text)
        wicketsElement = inningsElement.find("wicketsLost")
        answer["wickets"] = 6 if wicketsElement is None else int(wicketsElement.text)
        ballsElement = inningsElement.find("ballsBowled")
        answer["balls"] = maxBalls if ballsElement is None else int(ballsElement.text)
        return answer
    
    def getMatch(self, matchElement, teams, league):
        answer = MatchInReport()
        datetime = DateFormatter.parseDateTimeFromString(matchElement.find("date").text)
        answer.date = datetime.date()
        answer.time = datetime.time()
        answer.court = matchElement.find("pitch").text
        answer.homeTeamId = matchElement.find("homeTeam").get("id")
        answer.homeTeamName = teams[answer.homeTeamId]
        answer.awayTeamId = matchElement.find("awayTeam").get("id")
        answer.awayTeamName = teams[answer.awayTeamId]
        if league is not None:
            answer.leagueId = league.get("id")
            answer.leagueName = league.find("name").text
        return answer
    
