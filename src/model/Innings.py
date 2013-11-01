'''
Created on 25 Jul 2013

@author: hicksj
'''
from model.ModelObject import ModelObject
from model.Batsman import Batsman
from model.Bowler import Bowler

class Innings(ModelObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.runs = 0
        self.wickets = None
        self.balls = 0
        self.first = False
        self.batsmen = {}
        self.bowlers = {}
        
    @staticmethod
    def load(node, first):
        answer = Innings()
        data = ModelObject.extractData(node)
        value = data.get('runsScored', None)
        if value != None:
            answer.runs = int(value[0].text)
        value = data.get("wicketsLost", None)
        if value != None:
            answer.wickets = int(value[0].text)
        value = data.get("ballsBowled", None)
        if value != None:
            answer.balls = int(value[0].text)
        value = data.get("wicketsLost", None)
        if value != None:
            answer.wickets = int(value[0].text)
        answer.first = first
        value = data.get("batsman")
        if (value != None):
            for child in value:
                batsman = Batsman.load(child)
                answer.batsmen[batsman.playerId] = batsman
        value = data.get("bowler")
        if (value != None):
            for child in value:
                bowler = Bowler.load(child)
                answer.bowlers[bowler.playerId] = bowler
        return answer
