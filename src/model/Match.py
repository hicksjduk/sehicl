'''
Created on 25 Jul 2013

@author: hicksj
'''
from model.ModelObject import ModelObject
from datetime import datetime

class Match(ModelObject):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.awarded = None
        self.innings = {}
        self.teams = []
        self.court = None
        self.datetime = None
        self.maxOvers = None
        
    @staticmethod
    def load(node):
        answer = Match() 
        data = ModelObject.extractData(node);
        value = data.get('date', None)
        if value != None:
            answer.datetime = datetime.strptime(value[0].text, "%Y-%m-%d.%H:%M")
        value = data.get('pitch')
        if value != None:
            answer.court = value[0].text
        for k in ['homeTeam', 'awayTeam']:
            value = data.get(k)
            if value != None:
                answer.teams.append(value[0].attrib['id'])
        value = data.get("awardedMatch", None)
        if value != None:
            winner = value[0].find("winner").attrib['id']
            reason = value[0].find("reason").text
            answer.awarded = [winner, reason]
        value = data.get("playedMatch", None)
        if value != None:
            
        return answer