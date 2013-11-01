'''
Created on 25 Jul 2013

@author: hicksj
'''
from model.ModelObject import ModelObject

class Bowler(ModelObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.playerId = None
        self.balls = 0
        self.runs = 0
        self.wickets = 0
        
    @staticmethod
    def load(node):
        answer = Bowler()
        data = ModelObject.extractData(node)
        value = data.get('player', None)
        if value != None:
            answer.playerId = value
        value = data.get('ballsBowled', None)
        if value != None:
            answer.balls = int(value[0].text)
        value = data.get('runs', None)
        if value != None:
            answer.runs = int(value[0].text)
        value = data.get('wickets', None)
        if value != None:
            answer.wickets = int(value[0].text)
        return answer