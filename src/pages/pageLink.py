'''
Created on 30 Jul 2013

@author: hicksj
'''
import string

class PageLink:
    '''
    classdocs
    '''

    def __init__(self, pageId, sourcePage, pageParams={}, includeSeason=False):
        url = "/cgi-bin/page.py{0}"
        nvpTemplate = "{0}={1}"
        parmList = []
        if pageId is not None:
            parmList.append(nvpTemplate.format("id", pageId))
        sessionId = None if sourcePage is None else sourcePage.allParams.get("session", None)
        if sessionId is not None:
            parmList.append(nvpTemplate.format("session", sessionId))
        if includeSeason:
            season = None if sourcePage is None else sourcePage.allParams.get("season", None)
            if season is not None:
                parmList.append(nvpTemplate.format("season", season))
        parmList.extend([nvpTemplate.format(k, pageParams[k]) for k in sorted(pageParams.keys())])
        pageParams = "" if len(parmList) == 0 else "?{0}".format(string.join(parmList, "&"))
        self.url = url.format(pageParams)

class HtmlLink:
    
    def __init__(self, link):
        if isinstance(link, PageLink):
            theUrl = link.url
            template = "<a href=\"{url}\">"
        else:
            theUrl = link
            template = "<a href=\"{url}\" target=\"_blank\">"
        self.atag = template.format(url=theUrl)
        