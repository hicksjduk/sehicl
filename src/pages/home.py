'''
Created on 29 Jul 2013

@author: hicksj
'''
from pages.mailto import Mailto
from pages.page import Page
from pages.pageLink import PageLink, HtmlLink
import string
import glob
import re
from datetime import date, datetime
from pages.settings import Settings

class HomePage(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
    
    xml = """
    <h1>Welcome!</h1>
    {news}
    <p>
        <b>South East Hampshire (Fareham) Indoor Cricket League</b> is a
        {hcb.atag}Hampshire Cricket Board</a>
         affiliated indoor cricket league which holds its
        matches at the Main Hall, {flc.atag}Fareham
            Leisure Centre</a>, Park Lane, Fareham ({map.atag}map</a>).
        Matches are held on Sunday evenings, generally from 4.15 p.m. to 10.15
        p.m., from the beginning of October to March.
    </p>
    <p>
        At the end of each season the League holds a presentation evening. All
        division winning teams are invited to play a match, and to receive
        their trophies (club and personal). The League's Patron, the
        Worshipful the Mayor of Fareham, presents the senior teams' awards,
        and the evening culminates with an eight-a-side challenge match
        between the Mayor of Fareham's VIII and the Division 1 champions'
        VIII.
        <!-- 
        The 2016 presentation evening will be on Sunday 20th March.
        -->
        {presentation.atag}The 2016 presentation
            evening</a> was on Sunday 20th March; click the link for details of the
        evening.
        </p>
    <p>
        Please report any broken links, mis-spelled names or other errors to {webmaster.html}.
    </p>
    """

    def is_expired(self, filename):
        answer = False
        bits = filename.rsplit('.', 1)
        lastbit = bits[-1 if len(bits) == 1 else -2]
        regex = r'.*?(\d{8})$'
        mo = re.match(regex, lastbit)
        if mo is not None:
            answer = datetime.strptime(mo.group(1), '%Y%m%d').date() < date.today()
        return answer

    def getNewsItems(self):    
        answer = []
        for f in sorted(glob.glob(Settings.newsDirectory + "/*")):
            if not self.is_expired(f):
                with open(f) as fl:
                    answer.append(''.join(fl).strip())
        return answer

    def getTitle(self):
        answer = "South East Hampshire (Fareham) Indoor Cricket League"
        return answer
    
    def getContent(self):
        theNews = self.getNews()
        theWebmaster = Mailto("website", "the Webmaster", description="SEHICL Webmaster")
        thePresentation = HtmlLink(PageLink("presentation", self))
        theHcb = HtmlLink("http://www.ageasbowl.com/pages/community/")
        theFlc = HtmlLink("http://www.fareham.gov.uk/leisure/sport_and_fitness/leisurecentre.aspx")
        theMap = HtmlLink("http://www.multimap.com/map/browse.cgi?db=pc&amp;pc=PO167JU")
        answer = self.xml.format(news=theNews, webmaster=theWebmaster, presentation=thePresentation, hcb=theHcb, flc=theFlc, map=theMap)
        return answer
    
    def getNews(self):
        theNews = self.getNewsItems()
        answer = ""
        if theNews:
            nString = string.join(["<p>{0}</p>".format(n) for n in theNews], "\n")
            answer = """<div id="news">
            {0}
            </div>""".format(nString)
        return answer
        