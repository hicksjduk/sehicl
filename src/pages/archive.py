'''
Created on 2 Sep 2013

@author: hicksj
'''
from pages.page import Page
import string
from pages.pageLink import PageLink
import re

class ArchiveUtils():
    
    @staticmethod
    def getSeasonText(season):
        answer = "{0}-{1:02d}".format(season + 1999, season)
        return answer

class ArchiveIndex(Page):
    
    def __init__(self, pageId, maxSeason, params={}):
        Page.__init__(self, pageId, params)
        self.minSeason = 4
        self.maxSeason = maxSeason
        
    def getTitle(self):
        answer = "SEHICL Archive"
        return answer
    
    def getContent(self):
        html = """
        <h1>Archive</h1>
        <p>Click one of the links below to view archived information from the relevant season.</p>
        <ul>
            {seasons}
        </ul>
        """
        answer = html.format(seasons=string.join(self.getSeasonLinks(), "\n"))
        return answer
    
    def getSeasonLinks(self):
        html = """
        <li>
            <a href="{page.url}">{season}</a>
        </li>
        """
        answer = []
        for s in range(self.maxSeason, self.minSeason - 1, -1):
            season = ArchiveUtils.getSeasonText(s)
            page = PageLink("archive{0}".format(s), self)
            answer.append(html.format(page=page, season=season))
        return answer
    
class ArchiveSeasonIndex(Page):
    
    def __init__(self, pageId, params={}):
        Page.__init__(self, pageId, params)
        self.season = int(re.sub("[^0-9]", "", pageId))
        self.presentation = self.season >= 8

    def getTitle(self):
        answer = "SEHICL Archive: Season {0}".format(ArchiveUtils.getSeasonText(self.season))
        return answer
    
    def getContent(self):
        html = """
        <h1>Archive: Season {season}</h1>
        <table>
            <thead>
                <tr>
                    <th>Tables</th>
                    <th></th>
                    <th>Averages</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <ul>
                            <li>
                                <a href="{d1tab.url}">Division 1</a>
                            </li>
                            <li>
                                <a href="{d2tab.url}">Division 2</a>
                            </li>
                            <li>
                                <a href="{d3tab.url}">Division 3</a>
                            </li>
                            <li>
                                <a href="{d4tab.url}">Division 4</a>
                            </li>
                            <li>
                                <a href="{u16tab.url}">Colts Under-16</a>
                            </li>
                            <li>
                                <a href="{u13tab.url}">Colts Under-13</a>
                            </li>
                        </ul>
                    </td>
                    <td width="30"></td>
                    <td>
                        <ul>
                            <li>
                                <a href="{sbat.url}">Senior Batting</a>
                            </li>
                            <li>
                                <a href="{sbowl.url}">Senior Bowling</a>
                            </li>
                            <li>
                                <a href="{u16bat.url}">Colts Under-16 Batting</a>
                            </li>
                            <li>
                                <a href="{u16bowl.url}">Colts Under-16 Bowling</a>
                            </li>
                            <li>
                                <a href="{u13bat.url}">Colts Under-13 Batting</a>
                            </li>
                            <li>
                                <a href="{u13bowl.url}">Colts Under-13 Bowling</a>
                            </li>
                        </ul>
                    </td>
                </tr>
                {presentation}
            </tbody>
        </table>
        """
        d1tab = PageLink("archive{0}Division1Table".format(self.season), self)
        d2tab = PageLink("archive{0}Division2Table".format(self.season), self)
        d3tab = PageLink("archive{0}Division3Table".format(self.season), self)
        d4tab = PageLink("archive{0}Division4Table".format(self.season), self)
        u16tab = PageLink("archive{0}ColtsUnder16Table".format(self.season), self)
        u13tab = PageLink("archive{0}ColtsUnder13Table".format(self.season), self)
        sbat = PageLink("archive{0}SeniorBatting".format(self.season), self)
        sbowl = PageLink("archive{0}SeniorBowling".format(self.season), self)
        u16bat = PageLink("archive{0}ColtsUnder16Batting".format(self.season), self)
        u16bowl = PageLink("archive{0}ColtsUnder16Bowling".format(self.season), self)
        u13bat = PageLink("archive{0}ColtsUnder13Batting".format(self.season), self)
        u13bowl = PageLink("archive{0}ColtsUnder13Bowling".format(self.season), self)
        presentation = ""
        if (self.presentation):
            presHtml = """
            <tr>
                <td colspan="3" style="text-align: center">
                    <a href="{link.url}">Presentation Evening</a>
                </td>
            </tr>            
            """
            presLink = PageLink("archive{0}Presentation".format(self.season), self)
            presentation = presHtml.format(link=presLink)
        answer = html.format(season=ArchiveUtils.getSeasonText(self.season), \
                             d1tab=d1tab, d2tab=d2tab, d3tab=d3tab, d4tab=d4tab, u16tab=u16tab, u13tab=u13tab, \
                             sbat=sbat, sbowl=sbowl, u16bat=u16bat, u16bowl=u16bowl, u13bat=u13bat, u13bowl=u13bowl, \
                             presentation=presentation)
        return answer
