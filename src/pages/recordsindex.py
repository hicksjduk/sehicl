from pages.staticpage import StaticPage
from pages.pageLink import PageLink

class RecordsIndex(StaticPage):
    
    def __init__(self, pageId, pageFileName):
        StaticPage.__init__(self, pageId, pageFileName, "SEHICL Records")
        
    def getContent(self):
        html = StaticPage.getContent(self)
        performances = PageLink("recordsPerformances", self)
        winners = PageLink("recordsWinners", self)
        awards = PageLink("recordsAwards", self)
        fairplay = PageLink("recordsFairplay", self)
        answer = html.format(performances=performances, winners=winners, awards=awards, fairplay=fairplay)
        return answer