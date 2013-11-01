'''
Created on 25 Jul 2013

@author: hicksj
'''

class ModelObject:
    '''
    classdocs
    '''

    @staticmethod
    def extractData(node):
        answer = {}
        for k, v in node.items():
            answer[k] = v
        for child in node:
            tag = child.tag
            if tag not in answer:
                answer[tag] = []
            answer[tag].append(child)
        return answer
        