'''
Created on 7 Oct 2013

@author: hicksj
'''
from pages.page import Page
from xml.etree import ElementTree
from utils.dateformat import DateFormatter

class TeamInfo:
    def __init__(self, teamId, name, players):
        self.teamId = teamId
        self.name = name
        self.players = players 

class MatchInfo:
    def __init__(self, matchDate, court, leagueId, leagueName, teams):
        self.matchDate = matchDate
        self.court = court
        self.leagueId = leagueId
        self.leagueName = leagueName
        self.teams = teams

class PlayerSelect(Page):

    def __init__(self):
        self.matchData = None
        
    def getMatchData(self):
        if self.matchData is None:
            self.matchData = self.loadMatchData()
        return self.matchData
    
    def loadMatchData(self, fileName=None):
        fn = self.allParams.get("xmlfile") if fileName is None else fileName
        rootElement = ElementTree.parse(fn)
        answer = self.loadMatchInfo(rootElement, self.allParams.get("home", None), self.allParams.get("away", None))
        return answer
    
    def loadMatchInfo(self, rootElement, homeId, awayId):
        answer = None
        if homeId is not None and awayId is not None:
            for league in rootElement.findall("league"):
                teams = self.getTeams(league, homeId, awayId)
                if teams is not None:
                    for match in league.findall("match"):
                        if homeId == match.find("homeTeam").get("id") and awayId == match.find("awayTeam").get("id"):
                            matchDate = DateFormatter.parseDateTimeFromString(match.find("date").text)
                            court = match.find("pitch").text
                            leagueId = league.get("id")
                            leagueName = league.get("name").text
                            answer = MatchInfo(matchDate, court, leagueId, leagueName, teams) 
                            break
                if answer is not None:
                    break
        return answer
    
    def getTeams(self, league, homeId, awayId):
        answer = None
        for team in league.findall("team"):
            teamId = team.get("id")
            if teamId in (homeId, awayId):
                name = team.find("name").text
                if answer is None:
                    answer = []
                players = {}
                for player in team.findall("player"):
                    playerId = player.get("id")
                    playerName = player.find("name").text
                    players[playerId] = playerName
                answer[teamId] = TeamInfo(teamId, name, players)
                if len(answer) == 2:
                    break
        return answer
        