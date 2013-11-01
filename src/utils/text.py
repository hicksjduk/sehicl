'''
Created on 9 Aug 2013

@author: hicksj
'''

class TextUtils:

    @staticmethod
    def getGrammaticalNumber(number, singular, plural):
        answer = singular if number == 1 else plural
        return answer