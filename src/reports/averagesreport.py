import string
from utils.dateformat import DateFormatter

class PlayerInReport:
    def getPlayerSortKey(self):
        answer = ""
        if self.playerName is not None:
            words = string.split(self.playerName, " ", 1)
            answer = string.join(reversed(words), "")
        return answer

class BatsmanInReport(PlayerInReport):
    def __init__(self, playerId, playerName, teamId, teamName):
        self.playerId = playerId
        self.playerName = playerName
        self.teamId = teamId
        self.teamName = teamName
        self.innings = 0
        self.notout = 0
        self.runs = 0
        self.average = -1
        self.highScore = 0
        self.highScoreOut = False
        self.sortKey = None
        
    def maintainInvariants(self):
        outs = self.innings - self.notout
        self.average = -1 if outs == 0 else self.runs * 1.0 / outs
        self.sortKey = "{0}{1}".format(999 - self.runs, self.getPlayerSortKey())
        
class BowlerInReport(PlayerInReport):
    def __init__(self, playerId, playerName, teamId, teamName):
        self.playerId = playerId
        self.playerName = playerName
        self.teamId = teamId
        self.teamName = teamName
        self.balls = 0
        self.runs = 0
        self.wickets = 0
        self.bestWickets = -1
        self.bestRuns = 99999
        self.bestBalls = 0
        self.averagePerWicket = -1
        self.averagePerOver = -1
        self.sortKey = None
        
    def maintainInvariants(self):
        self.averagePerWicket = -1 if self.wickets == 0 else self.runs * 1.0 / self.wickets
        self.averagePerOver = -1 if self.balls == 0 else self.runs * 6.0 / self.balls
        self.sortKey = "{0}{1:.15f}{2}".format(99 - self.wickets, 11 + self.averagePerOver, self.getPlayerSortKey())

class AveragesReport:
    pass

class AveragesReportGenerator:
    
    def getLeaguesTeamsAndPlayers(self, rootElement, leagueIds=None, teamId=None):
        leagues, teams, players = {}, {}, {}
        if (leagueIds is not None and teamId is None) or (teamId is not None and leagueIds is None):
            for leagueElement in rootElement.findall("league"):
                lId = leagueElement.get("id")
                if leagueIds is None or lId in leagueIds:
                    leagueName = leagueElement.find("name").text
                    for teamElement in leagueElement.findall("team"):
                        tId = teamElement.get("id")
                        if teamId is None or tId == teamId:
                            teamName = teamElement.find("name").text
                            teams[tId] = teamName
                            leagues[lId] = leagueName
                            for playerElement in teamElement.findall("player"):
                                pId = playerElement.get("id")
                                playerName = playerElement.find("name").text
                                players[pId] = playerName
                        if teamId is not None and len(teams) > 0:
                            break
                if teamId is not None and len(teams) > 0:
                    break
        return (leagues, teams, players)
    
    def getAverages(self, rootElement, leagues, teams, players, batting=False, bowling=False):
        answer = AveragesReport()
        lastCompleteMatchDate = None
        lastScheduledMatchDate = None
        incompleteMatchesByDate = {} 
        battingAverages = None if not batting else {}
        bowlingAverages = None if not bowling else {}
        if batting or bowling:
            for leagueElement in rootElement.findall("league"):
                leagueId = leagueElement.get("id")
                if leagueId in leagues.keys():
                    for matchElement in leagueElement.findall("match"):
                        relevant, complete = self.updateAveragesFromMatch(matchElement, teams, players, battingAverages, bowlingAverages)
                        if relevant:
                            date = DateFormatter.parseDateTimeFromString(matchElement.find("date").text).date()
                            if lastScheduledMatchDate is None or lastScheduledMatchDate < date:
                                lastScheduledMatchDate = date
                            if complete:
                                if lastCompleteMatchDate is None or lastCompleteMatchDate < date:
                                    lastCompleteMatchDate = date
                            else:
                                count = incompleteMatchesByDate.get(date, 0)
                                incompleteMatchesByDate[date] = count + 1
        answer.lastCompleteMatchDate = lastCompleteMatchDate
        answer.lastScheduledMatchDate = lastScheduledMatchDate
        if lastCompleteMatchDate is not None:
            toCome = 0
            for d in sorted(incompleteMatchesByDate.keys()):
                if d > lastCompleteMatchDate:
                    break
                toCome = toCome + incompleteMatchesByDate[d]
            answer.toCome = toCome
        if batting:
            answer.battingAverages = battingAverages.values()
        if bowling:
            answer.bowlingAverages = bowlingAverages.values()
        answer.leagueName = leagues.values()[0] if len(leagues) == 1 else None
        answer.teamName = teams.values()[0] if len(teams) == 1 else None
        return answer

    def updateAveragesFromMatch(self, matchElement, teams, players, battingAverages, bowlingAverages):    
        matchRelevant, matchComplete = False, False
        for elem in ("homeTeam", "awayTeam"):
            matchRelevant = matchElement.find(elem).get("id") in teams.keys()
            if matchRelevant:
                break
        if matchRelevant:
            playedMatchElement = matchElement.find("playedMatch")
            matchComplete = playedMatchElement is not None or matchElement.find("awardedMatch") is not None
            if playedMatchElement is not None:
                if battingAverages is not None:
                    self.updateBattingAveragesFromMatch(playedMatchElement, teams, players, battingAverages)
                if bowlingAverages is not None:
                    self.updateBowlingAveragesFromMatch(playedMatchElement, teams, players, bowlingAverages)
        return (matchRelevant, matchComplete)

    def updateBattingAveragesFromMatch(self, playedMatchElement, teams, players, battingAverages):
        for teamInMatchElement in playedMatchElement.findall("teamInMatch"):
            teamId = teamInMatchElement.find("teamRef").get("id")
            if teamId in teams.keys():
                for batsmanElement in teamInMatchElement.findall("innings/batsman"):
                    self.updateBattingAveragesFromPerformance(batsmanElement, teamId, teams, players, battingAverages)

    def updateBattingAveragesFromPerformance(self, batsmanElement, teamId, teams, players, battingAverages):
        playerId = batsmanElement.get("player")
        details = battingAverages.get(playerId, None)
        if details is None:
            details = BatsmanInReport(playerId, players[playerId], teamId, teams[teamId])
            battingAverages[playerId] = details
        details.innings = details.innings + 1
        runs = int(batsmanElement.find("runs").text)
        details.runs = details.runs + runs
        out = batsmanElement.find("out").text == "true"
        if not out:
            details.notout = details.notout + 1
        if runs == details.highScore:
            details.highScoreOut = out and details.highScoreOut 
        elif runs > details.highScore:
            details.highScore = runs
            details.highScoreOut = out 
        details.maintainInvariants()

    def updateBowlingAveragesFromMatch(self, playedMatchElement, teams, players, bowlingAverages):
        teamList = []
        inningsList = []
        for teamInMatchElement in playedMatchElement.findall("teamInMatch"):
            teamId = teamInMatchElement.find("teamRef").get("id")
            teamList.append(teamId)
            inningsList.insert(0, teamInMatchElement.find("innings"))
        for teamId, innings in zip(teamList, inningsList):
            if teamId in teams.keys():
                for bowlerElement in innings.findall("bowler"):
                    self.updateBowlingAveragesFromPerformance(bowlerElement, teamId, teams, players, bowlingAverages)

    def updateBowlingAveragesFromPerformance(self, bowlerElement, teamId, teams, players, bowlingAverages):
        playerId = bowlerElement.get("player")
        details = bowlingAverages.get(playerId, None)
        if details is None:
            details = BowlerInReport(playerId, players[playerId], teamId, teams[teamId])
            bowlingAverages[playerId] = details
        balls, runs, wickets = [int(bowlerElement.find(elem).text) for elem in ("ballsBowled", "runs", "wickets")]
        details.balls = details.balls + balls
        details.runs = details.runs + runs
        details.wickets = details.wickets + wickets
        newBest = False
        if details.bestWickets < wickets:
            newBest = True
        elif details.bestWickets == wickets:
            bestRR = -1 if details.bestBalls == 0 else details.bestRuns * 1.0 / details.bestBalls
            thisRR = -1 if balls == 0 else runs / balls
            newBest = thisRR < bestRR
        if newBest:
            details.bestBalls = balls
            details.bestRuns = runs
            details.bestWickets = wickets
        details.maintainInvariants()

    def getLeagueBattingAveragesReport(self, rootElement, leagueIds):
        leagues, teams, players = self.getLeaguesTeamsAndPlayers(rootElement, leagueIds=leagueIds)
        answer = self.getAverages(rootElement, leagues, teams, players, True, False)
        return answer

    def getLeagueBowlingAveragesReport(self, rootElement, leagueIds):
        leagues, teams, players = self.getLeaguesTeamsAndPlayers(rootElement, leagueIds=leagueIds)
        answer = self.getAverages(rootElement, leagues, teams, players, False, True)
        return answer

    def getTeamAveragesReport(self, rootElement, teamId):
        leagues, teams, players = self.getLeaguesTeamsAndPlayers(rootElement, teamId=teamId)
        answer = self.getAverages(rootElement, leagues, teams, players, True, True)
        return answer

    def getAllTeamsByLeague(self, rootElement):
        answer = {}
        for league in rootElement.findall("league"):
            leagueId = league.get("id")
            leagueName = league.find("name").text
            teams = []
            answer[(leagueId, leagueName)] = teams
            for team in league.findall("team"):
                teamId = team.get("id")
                teamName = team.find("name").text
                teams.append((teamId, teamName))
        return answer