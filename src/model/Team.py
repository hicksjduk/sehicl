'''
Created on 25 Jul 2013

@author: hicksj
'''
from model.ModelObject import ModelObject
from model.Player import Player

class Team(ModelObject):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.name = None
        self.id = None
        self.players = {}
        self.deductions = []
        
    @staticmethod
    def load(node):
        answer = Team();
        data = ModelObject.extractData(node)
        value = data.get('name', None)
        if value != None:
            answer.name = value[0].text
        value = data.get('id', None)
        if value != None:
            answer.id = value
        value = data.get('player', None)
        if value != None:
            for child in value:
                player = Player.load(child)
                answer.players[player.id] = player
        value = data.get("pointsDeduction")
        if value != None:
            for child in value:
                points = int(child.find("points").text)
                reason = child.find("reason").text
                answer.deductions.append([points, reason])
        return answer
