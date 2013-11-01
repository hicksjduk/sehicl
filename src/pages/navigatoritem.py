'''
Created on 30 Jul 2013

@author: hicksj
'''
import string
from pages.pageLink import HtmlLink, PageLink

class NavigatorItem:
    
    def __init__(self, itemId=None, text=None, pageId=None, params={}, items=[], url=None):
        if text is not None:
            self.text = text
        elif itemId is not None:
            self.text = itemId.capitalize()
        elif pageId is not None:
            self.text = pageId.capitalize()
        else:
            self.text = None
        self.itemId = itemId
        self.pageId = pageId
        pageParams = params
        self.pageParams = pageParams
        self.items = items
        self.url = url
        
    def isSelected(self, currentPage):
        answer = self.pageId is not None and self.pageId == currentPage.pageId
        if answer:
            for k, v in self.pageParams.items():
                pageParam = currentPage.allParams.get(k, None)
                answer = pageParam == v
                if not answer:
                    break
        return answer
    
    def containsSelected(self, currentPage):
        answer = self.isSelected(currentPage)
        if not answer:
            answer = self.itemId is not None and currentPage.pageId.lower().find(self.itemId.lower()) != -1
            if not answer:
                for item in self.items:
                    answer = item.containsSelected(currentPage)
                    if answer:
                        break
        return answer
    
    def getItemLink(self, currentPage):
        html = """
        {content}
        """
        contentHtml = ""
        if self.isSelected(currentPage):
            contentHtml = "<span class=\"current\">{0}</span>".format(self.text)
        else:
            if self.url is None:
                theLink = HtmlLink(PageLink(self.pageId, currentPage, self.pageParams))
            else:
                theLink = HtmlLink(self.url)
            contentHtml = "{link.atag}{text}</a>".format(link=theLink, text=self.text)
        answer = html.format(content=contentHtml)
        return answer        

    def getHtml(self, currentPage):
        html = """
        <li>
            {itemLink}
            {items}
        </li>
        """
        linkHtml = self.getItemLink(currentPage)
        itemHtml = ""
        if len(self.items) > 0:
            listHtml = """
            <ul id="currentMenu">
                {itemHtml}
            </ul>
            """
            containsSelected = self.containsSelected(currentPage)
            if containsSelected:
                itemHtmlStrings = string.join([item.getHtml(currentPage) for item in self.items])
                itemHtml = listHtml.format(itemHtml=itemHtmlStrings)
            else:
                itemHtml = "" 
        answer = html.format(items=itemHtml, itemLink=linkHtml)
        return answer
