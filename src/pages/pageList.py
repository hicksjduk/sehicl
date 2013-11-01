'''
Created on 29 Jul 2013

@author: hicksj
'''
from pages.home import HomePage
from pages.leaguefixtures import LeagueFixtures
from pages.results import LeagueResults, DateResults
from pages.teamfixtures import TeamFixtures
from pages.users import UserRegistration, UserActivation, UserLogin
from pages.tables import LeagueTable
from pages.averages import BattingAverages, BowlingAverages, TeamAverages,\
    TeamAveragesIndex, AveragesIndex
from pages.staticpage import StaticPage
from pages.recordsindex import RecordsIndex
from pages.archive import ArchiveIndex, ArchiveSeasonIndex
import re
from pages.dutyrota import DutyRota
from pages.useradmin import UserAdmin
from pages.contacts import PartialContacts, FullContacts
from pages.settings import Settings

class PageList:
    '''
    classdocs
    '''
    
    defaultPage = "home"
    
    pageList = []
    pageList.append(HomePage("home"))
    pageList.append(StaticPage("notfound", "{0}/notfound.html".format(Settings.staticHtmlDirectory), "Page not found!"))
    pageList.append(UserAdmin("userAdmin", role="admin"))
    pageList.append(PartialContacts("contacts"))
    pageList.append(FullContacts("fullContacts", role=""))
    pageList.append(StaticPage("presentation", "{0}/archive13/PresentationEvening.html".format(Settings.staticHtmlDirectory), "SEHICL Presentation Evening"))
    pageList.append(TeamFixtures("teamFixtures"))
    pageList.append(LeagueFixtures("allFixtures"))
    pageList.append(LeagueFixtures("leagueFixtures"))
    pageList.append(LeagueResults("leagueResults"))
    pageList.append(DateResults("latestResults"))
    pageList.append(DateResults("dateResults"))
    pageList.append(LeagueTable("tables"))
    pageList.append(LeagueTable("leagueTable"))
    pageList.append(AveragesIndex("averagesIndex"))
    pageList.append(BattingAverages("battingAverages"))
    pageList.append(BowlingAverages("bowlingAverages"))
    pageList.append(BattingAverages("leagueBattingAverages"))
    pageList.append(BowlingAverages("leagueBowlingAverages"))
    pageList.append(TeamAverages("teamAverages"))
    pageList.append(TeamAveragesIndex("teamAveragesIndex"))
    pageList.append(StaticPage("rules", "{0}/rules.html".format(Settings.staticHtmlDirectory), "SEHICL Rules and Playing Conditions"))
    pageList.append(DutyRota("fixturesDutyRota"))
    pageList.append(StaticPage("resources", "{0}/resources.html".format(Settings.staticHtmlDirectory), "SEHICL Resources"))
    pageList.append(RecordsIndex("records", "{0}/records/recordsindex.html".format(Settings.staticHtmlDirectory)))
    pageList.append(StaticPage("recordsPerformances", "{0}/records/recordperformances.html".format(Settings.staticHtmlDirectory), "SEHICL Records: Record Performances"))
    pageList.append(StaticPage("recordsWinners", "{0}/records/divwinners.html".format(Settings.staticHtmlDirectory), "SEHICL Honours Board: Divisional Winners"))
    pageList.append(StaticPage("recordsAwards", "{0}/records/individualawards.html".format(Settings.staticHtmlDirectory), "SEHICL Honours Board: Individual Awards"))
    pageList.append(StaticPage("recordsFairplay", "{0}/records/fairplay.html".format(Settings.staticHtmlDirectory), "SEHICL Honours Board: Sporting and Efficiency"))
    pageList.append(ArchiveIndex("archive"))
    additionalPromotions = {}
    additionalPromotions[6] = {"Division3": [3], "Division4": [3]}
    additionalPromotions[7] = {"Division3": [3, 4], "Division4": [3, 4]}
    additionalPromotions[10] = {"Division4": [4]}
    additionalPromotions[12] = {"Division4": [3, 4]}
    additionalPromotions[13] = {"Division3": [3], "Division4": [3]}
    for s in range(4, 14):
        index = ArchiveSeasonIndex("archive{0}".format(s))
        title = index.getTitle()
        pageList.append(index)
        for divName in ("Division 1", "Division 2", "Division 3", "Division 4", "Colts Under-16", "Colts Under-13"):
            divId = re.sub("[ -]", "", divName)
            pageId = "archive{0}{1}Table".format(s, divId)
            if s < 6:
                pageFile = "{2}/archive{0}/{1}.html".format(s, divId, Settings.staticHtmlDirectory)
                pageList.append(StaticPage(pageId, pageFile, title))
            else:
                params = {"season": s, "league": divId, "archive": "yes"}
                ap = additionalPromotions.get(s, {}).get(divId, None)
                if ap is not None:
                    params["additionalPromotions"] = ap
                pageList.append(LeagueTable(pageId, params))
        for section in ("Senior", "Colts Under-16", "Colts Under-13"):
            for activity in ("Batting", "Bowling"):
                sectionId = re.sub("[ -]", "", section)
                pageId = "archive{0}{1}{2}".format(s, sectionId, activity)
                if s < 6:
                    pageFile = "{3}/archive{0}/{1}{2}.html".format(s, sectionId, activity, Settings.staticHtmlDirectory)
                    pageList.append(StaticPage(pageId, pageFile, title))
                else:
                    parms = {"season": s, "archive": "yes"}
                    if (sectionId != "Senior"):
                        parms["league"] = sectionId
                    if activity == "Batting":
                        pageList.append(BattingAverages(pageId, parms))
                    else:
                        pageList.append(BowlingAverages(pageId, parms))
        if index.presentation:
            pageId = "archive{0}Presentation".format(s)
            pageFile = "{0}/archive{1}/PresentationEvening.html".format(Settings.staticHtmlDirectory, s)
            pageList.append(StaticPage(pageId, pageFile, title))
    pageList.append(UserRegistration("register"))
    pageList.append(UserActivation("activate"))
    pageList.append(UserLogin("login"))

    pages = {}
    for p in pageList:
        pages[p.pageId] = p
