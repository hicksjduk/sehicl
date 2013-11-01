'''
Created on 26 Jul 2013

@author: hicksj
'''
from datetime import datetime
from operator import attrgetter
from utils.text import TextUtils

class TeamFixturesReport:

    def getSortedMatches(self):
        return sorted(self.matches, key=attrgetter("datetime", "opponentName"))  

class MatchInReport:
    pass

class TeamFixturesReportGenerator():
    '''
    classdocs
    '''

    def getReport(self, rootElement, teamId):
        answer = TeamFixturesReport()
        answer.matches = []
        leagueElement = self.getLeagueElement(rootElement, teamId)
        teams = self.getTeams(leagueElement)
        matchElements = self.getMatchElements(leagueElement, teamId)
        answer.teamId = teamId
        answer.teamName = teams[teamId]
        answer.leagueId = leagueElement.get('id')
        answer.leagueName = leagueElement.find('name').text
        for matchElement in matchElements:
            answer.matches.append(self.getMatch(matchElement, teamId, teams))
        return answer
    
    def getMatch(self, matchElement, teamId, teams):
        answer = MatchInReport()
        self.setOpponentInfo(teamId, matchElement, answer, teams)
        self.setWinLossInfo(teamId, matchElement, answer)
        answer.court = matchElement.find("pitch").text
        answer.datetime = datetime.strptime(matchElement.find("date").text, "%Y-%m-%d.%H:%M")
        return answer
            
    def setOpponentInfo(self, teamId, matchElement, match, teams):
        homeTeam = matchElement.find("homeTeam")
        awayTeam = matchElement.find("awayTeam")
        match.home = (homeTeam.get('id') == teamId)
        opponent = awayTeam if match.home else homeTeam
        match.opponentId = opponent.get('id')
        match.opponentName = teams[match.opponentId]
            
    def setWinLossInfo(self, teamId, matchElement, match):
        match.result = None
        match.margin = None
        if not self.setWinLossInfoGamePlayed(teamId, matchElement, match):
            self.setWinLossInfoGameAwarded(teamId, matchElement, match)
        
    def setWinLossInfoGamePlayed(self, teamId, matchElement, match):
        playedMatchElement = matchElement.find('playedMatch')
        answer = playedMatchElement != None
        if answer:
            ourScore = None
            ourWickets = None
            batFirst = None
            theirScore = None
            theirWickets = None
            for teamInMatchElement in playedMatchElement.findall("teamInMatch"):
                tRef = teamInMatchElement.find("teamRef").get("id")
                inns = teamInMatchElement.find("innings")
                if tRef == teamId:
                    batFirst = teamInMatchElement.find("battingFirst").text == "true" 
                    ourScore = int(inns.find("runsScored").text)
                    wktsElement = inns.find("wicketsLost")
                    ourWickets = 6 if wktsElement == None else int(wktsElement.text)
                else:
                    theirScore = int(inns.find("runsScored").text)
                    wktsElement = inns.find("wicketsLost")
                    theirWickets = 6 if wktsElement == None else int(wktsElement.text)
            if ourScore > theirScore:
                match.result = "Won"
            elif ourScore < theirScore:
                match.result = "Lost"
            else:
                match.result = "Tied"
            if batFirst:
                match.margin = self.getMargin(ourScore, theirScore, theirWickets)
            else:
                match.margin = self.getMargin(theirScore, ourScore, ourWickets)
        return answer
    
    def getMargin(self, batFirstScore, batSecondScore, batSecondWickets):
        answer = None
        runsDifference = batFirstScore - batSecondScore
        if runsDifference > 0:
            answer = "{0} {1}".format(runsDifference, TextUtils.getGrammaticalNumber(runsDifference, "run", "runs"))
        elif runsDifference < 0:
            wicketsInHand = 6 - batSecondWickets
            answer = "{0} {1}".format(wicketsInHand, TextUtils.getGrammaticalNumber(wicketsInHand, "wicket", "wickets"))
        return answer
    
    def setWinLossInfoGameAwarded(self, teamId, matchElement, match):
        awardedMatchElement = matchElement.find('awardedMatch')
        answer = awardedMatchElement != None
        if answer:
            won = awardedMatchElement.find("winner").get("id") == teamId
            match.result = "Won" if won else "Lost"
            match.margin = "default"
        return answer
    
    def getLeagueElement(self, modelElement, teamId):
        answer = None
        for l in modelElement.findall("league"):
            for t in l.findall("team"):
                if t.get("id") == teamId:
                    answer = l
                    break;
                if answer is not None:
                    break
            if answer is not None:
                break
        return answer
    
    def getTeams(self, leagueElement):
        answer = {}
        for elem in leagueElement.findall("team"):
            answer[elem.get('id')] = elem.find("name").text
        return answer
    
    def getMatchElements(self, leagueElement, teamId):
        answer = []
        for m in leagueElement.findall("match"):
            match = None
            for ha in ["homeTeam", "awayTeam"]:
                if m.find(ha).get("id") == teamId:
                    match = m
                    break
            if match is not None:
                answer.append(match)
        return answer
    
