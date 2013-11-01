'''
Created on 29 Jul 2013

@author: hicksj
'''
from pages.mailto import Mailto
from pages.page import Page
from pages.pageLink import PageLink, HtmlLink
import string

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
        VIII. {presentation.atag}The 2013 presentation
            evening</a> was on Sunday 24th March; click the link for details of the
        evening. In 2014, the presentation evening will be on Sunday 6th April.
    </p>
    <p>
        Please report any broken links, mis-spelled names or other errors to {webmaster.html}.
    </p>
    """

    def getNewsItems(self):    
        answer = []
        answer.append("""
            All players are reminded of <a href="{rules.url}#sectionN">the rules on clothing</a>,
            and in particular that <b>shoes must be predominantly white in colour</b>.
        """.format(rules=PageLink("rules", self)))
        answer.append("""
            <b>The new version of the website</b> is now live. If you encounter an error,
            please contact {webmaster.html} giving the URL of the page on which the error
            occurred.
            <br>The "Members' area" link is no longer present. Full contact details
            for committee and club contacts are still available, but are accessed by clicking
            the "Contacts" link in the navigation bar to the left, and then clicking "Full details".
            This page remains password-protected: if you require access you must register and then login.
            Note that if you applied for a login to the members' area last season, that login will
            no longer work, and you must re-register.
            """.format(webmaster=Mailto("website", "the Webmaster")))
        answer.append("""
            <b>The League needs to recruit some more umpires.</b> If you would be
            willing to umpire your help would be greatly appreciated. Please
            speak to any umpire on match nights, or contact the umpires'
            co-ordinator, {umpires.html}.
            """.format(umpires=Mailto("umpires", "Andy Anthony")))
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
    
    def getNews(self, news=None):
        theNews = news if news != None else self.getNewsItems()
        answer = ""
        if theNews:
            nString = string.join(["<p>{0}</p>".format(n) for n in theNews], "\n")
            answer = """<div id="news">
            {0}
            </div>""".format(nString)
        return answer
        