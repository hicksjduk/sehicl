'''
Created on 12 Sep 2013

@author: hicksj
'''

class RedirectException(Exception):
    def __init__(self, link):
        self.link = link        
                

class Redirect:
    def __init__(self, pageLink):
        self.pageLink = pageLink
        
    def getHtml(self, params={}):
        html = """
        <html>
            <head>
                <meta http-equiv="refresh" content="0;url={page.url}">
            </head>
        </html>
        """
        answer = html.format(page=self.pageLink)
        return answer
        