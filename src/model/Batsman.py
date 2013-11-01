'''
Created on 25 Jul 2013

@author: hicksj
'''
from model.ModelObject import ModelObject

class Batsman(ModelObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.playerId = None
        self.runs = 0
        self.out = False
        
    @staticmethod
    def load(node):
        answer = Batsman()
        data = ModelObject.extractData(node)
        value = data.get('player', None)
        if value != None:
            answer.playerId = value
        value = data.get('runs', None)
        if value != None:
            answer.runs = int(value[0].text)
        value = data.get('out', None)
        if value != None:
            answer.out = value[0].text == 'true'
        return answer