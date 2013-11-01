'''
Created on 29 Jul 2013

@author: hicksj
'''

import string
from pages.navigator import Navigator
from pages.pageLink import HtmlLink
from pages.settings import Settings

class Page():
    
    def __init__(self, pageId, params={}, role=None):
        self.pageId = pageId
        self.coreParams = params
        self.allParams = {}
        self.role = role
    
    def getHtml(self, params={}):
        html = """
        <html>
        <head>
        {header}
        </head>
        <body id=\"{pageId}\">
        {body}
        </body>
        </html>
        """
        self.allParams = {}
        self.allParams.update(self.coreParams)
        self.allParams.update(params)
        Settings.updateParams(self.allParams)
        theHeader = self.getHtmlHeader()
        thePageId = self.pageId
        theBody = self.getHtmlBody()
        answer = Page.stripWhitespace(html.format(header=theHeader, pageId=thePageId, body=theBody))
        return answer
    
    @staticmethod
    def stripWhitespace(thestring):
        lines = string.split(thestring, "\n")
        trimmedlines = [l.strip() for l in lines]
        answer = string.join(trimmedlines, "\n")
        return answer
    
    def getHtmlHeader(self):
        html= """
        <META http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link href="/sehicl2.css" rel="stylesheet" type="text/css">
        <script language="javascript" src="/sehicl2.js" type="text/javascript"></script>
        <title>{title}</title>
        """.format(title=self.getTitle())
        answer = html
        return answer
    
    def getHtmlBody(self):
        html = """
        <div id="page">
            <div id="leftNavigator">
            {navigator}
            </div>
            <div id="main">
                <div id="header">
                {header}
                </div>
                <div id="content">
                {content}
                </div>
                <div id="footer">
                {footer}
                </div>
            </div>
        </div>
        """
        theNavigator = self.getNavigator()
        theHeader = self.getPageHeader()
        theContent = self.getPageContent()
        theFooter = self.getPageFooter()
        answer = html.format(navigator=theNavigator, header=theHeader, content=theContent, footer=theFooter)
        return answer

    def getNavigator(self):
        navigator = Navigator()
        answer = navigator.getHtml(self)
        return answer
    
    def getPageHeader(self):
        html = """
        <p id="LeagueInfo">
            <img src="/graphics/leaguelogo_red.gif" align="left" hspace="20" alt="South-East Hampshire (Fareham) Indoor Cricket League">
            <span class="nolinewrap">South-East Hampshire (Fareham)</span> <span class="nolinewrap">Indoor Cricket League</span>
        </p>
        <p id="SponsorInfo">Sponsored by Game Set and Match
            {gsm.atag}
                <img src="/graphics/smallgsamlogo.gif" align="middle" hspace="15" border="0" alt="Sponsored by Game Set and Match">
            </a>
        </p>
        """
        theGsm = HtmlLink("http://www.gsam.co.uk")
        answer = html.format(gsm=theGsm)
        return answer
    
    def getPageContent(self):
        return self.getContent()
    
    def getPageFooter(self):
        html = """
        <p>
            <hr>
        </p>
        <p style="font-size: smaller">
            <span style="font-weight: bold">
                &copy; South-East Hampshire (Fareham) Indoor Cricket League
            </span>
            <br>
            All rights reserved.
        </p>
        <p>    
            {hcc.atag}
                <img src="/images/credit/hosted-white.gif" align="middle" width="154" height="70" border="0" alt="Web Space provided by Hampshire County Council">
            </a>
        </p>
        """
        theHcc = HtmlLink("http://www.hants.gov.uk")
        answer = html.format(hcc=theHcc)
        return answer