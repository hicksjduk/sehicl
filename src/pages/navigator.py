'''
Created on 30 Jul 2013

@author: hicksj
'''
from xml.etree import ElementTree
from string import strip
import string
from pages.navigatoritem import NavigatorItem


class Navigator:
    
    xml = """
    <navigator>
        <item pageId="home"/>
        <item id="contacts" pageId="contacts">
            <item id="fullContacts" pageId="fullContacts">Full details</item>
        </item>
        <item id="fixtures" pageId="allFixtures">
            Fixtures
            <item pageId="leagueFixtures" league="Division1">Division 1</item>
            <item pageId="leagueFixtures" league="Division2">Division 2</item>
            <item pageId="leagueFixtures" league="Division3">Division 3</item>
            <item pageId="leagueFixtures" league="Division4">Division 4</item>
            <item pageId="leagueFixtures" league="ColtsUnder16">Colts Under-16</item>
            <item pageId="leagueFixtures" league="ColtsUnder13">Colts Under-13</item>
            <item pageId="fixturesDutyRota">Duty team rota</item>
        </item>
        <item id="results" pageId="latestResults">
            Results
            <item pageId="leagueResults" league="Division1">Division 1</item>
            <item pageId="leagueResults" league="Division2">Division 2</item>
            <item pageId="leagueResults" league="Division3">Division 3</item>
            <item pageId="leagueResults" league="Division4">Division 4</item>
            <item pageId="leagueResults" league="ColtsUnder16">Colts Under-16</item>
            <item pageId="leagueResults" league="ColtsUnder13">Colts Under-13</item>
        </item>
        <item id="tables" pageId="tables">
            <item pageId="leagueTable" league="Division1">Division 1</item>
            <item pageId="leagueTable" league="Division2">Division 2</item>
            <item pageId="leagueTable" league="Division3">Division 3</item>
            <item pageId="leagueTable" league="Division4">Division 4</item>
            <item pageId="leagueTable" league="ColtsUnder16">Colts Under-16</item>
            <item pageId="leagueTable" league="ColtsUnder13">Colts Under-13</item>
        </item>
        <item id="averages" pageId="averagesIndex">
            Averages
            <item pageId="battingAverages">Senior Batting</item>
            <item pageId="bowlingAverages">Senior Bowling</item>
            <item pageId="leagueBattingAverages" league="ColtsUnder16">Colts Under-16 Batting</item>
            <item pageId="leagueBowlingAverages" league="ColtsUnder16">Colts Under-16 Bowling</item>
            <item pageId="leagueBattingAverages" league="ColtsUnder13">Colts Under-13 Batting</item>
            <item pageId="leagueBowlingAverages" league="ColtsUnder13">Colts Under-13 Bowling</item>
            <item pageId="teamAveragesIndex">By team</item>
        </item>
        <item id="resources" pageId="resources"/>
        <item id="rules" pageId="rules"/>
        <item id="records" pageId="records">
            <item pageId="recordsPerformances">Record Performances</item>
            <item pageId="recordsWinners">Divisional Winners</item>
            <item pageId="recordsAwards">Individual Awards</item>
            <item pageId="recordsFairplay">Sporting and Efficiency</item>
        </item>
        <item id="archive" pageId="archive">
            <item pageId="archive15">2014-15</item>
            <item pageId="archive14">2013-14</item>
            <item pageId="archive13">2012-13</item>
            <item pageId="archive12">2011-12</item>
            <item pageId="archive11">2010-11</item>
            <item pageId="archive10">2009-10</item>
            <item pageId="archive9">2008-09</item>
            <item pageId="archive8">2007-08</item>
            <item pageId="archive7">2006-07</item>
            <item pageId="archive6">2005-06</item>
            <item pageId="archive5">2004-05</item>
            <item pageId="archive4">2003-04</item>
        </item>
    </navigator>
    """
    __items = None

    def __init__(self, html=None):
        if html is not None:
            rootElement = ElementTree.fromstring(html)
            self.items = self.getItems(rootElement)
        else:
            if self.__items is None:
                theHtml = self.xml if html is None else html
                rootElement = ElementTree.fromstring(theHtml)
                self.__items = self.getItems(rootElement)
            self.items = self.__items

    def getItems(self, element):
        answer = [self.getItem(i) for i in element.findall("item")]
        return answer
    
    def getItem(self, itemElement):
        itemId = itemElement.get("id", None)
        pageId = itemElement.get("pageId", None)
        text = itemElement.text
        if text is not None:
            text = strip(text)
            if text == "":
                text = None
        url = itemElement.get("url")
        params = {}
        for k in itemElement.keys():
            if k not in ("pageId", "url", "id"):
                params[k] = itemElement.get(k)
        items = self.getItems(itemElement)
        answer = NavigatorItem(itemId=itemId, pageId=pageId, params=params, text=text, items=items, url=url)
        return answer
    
    def getHtml(self, currentPage):
        html = """
        <ul class="navigator">
            {items}
        </ul>
        """
        theItems = [i.getHtml(currentPage) for i in self.items]
        answer = html.format(items=string.join(theItems, "\n"))
        return answer