'''
Created on 30 Aug 2013

@author: hicksj
'''
from pages.page import Page

class StaticPage(Page):

    def __init__(self, pageId, pageFileName, title, role=None):
        Page.__init__(self, pageId, role=role)
        self.pageFileName = pageFileName
        self.title = title

    def getTitle(self):
        return self.title
    
    def getContent(self):
        with open(self.pageFileName) as f:
            answer = f.read()
        return answer 
        
