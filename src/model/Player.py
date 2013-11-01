'''
Created on 25 Jul 2013

@author: hicksj
'''
from model.ModelObject import ModelObject

class Player(ModelObject):
    '''
    classdocs
    '''
    
    @staticmethod
    def load(node):
        answer = Player()
        data = ModelObject.extractData(node)
        value = data.get('name', None)
        if value != None:
            answer.name = value[0].text
        value = data.get('id', None)
        if value != None:
            answer.id = value
        return answer
    
    def __init__(self):
        self.name = None
        self.id = None
    
    