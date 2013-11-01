'''
Created on 30 Jul 2013

@author: hicksj
'''
import unittest
from pages.pageLink import PageLink
from pages.page import Page


class Test(unittest.TestCase):


    def testPageLinkNoParameters(self):
        result = PageLink("hello", Page(""), {}).url
        self.assertEqual("/cgi-bin/page.py?id=hello", result)

    def testPageLinkWithParameters(self):
        result = PageLink("hello", Page(""), {"team": "aasa", "league": "afafa"}).url
        self.assertEqual("/cgi-bin/page.py?id=hello&league=afafa&team=aasa", result)

    def testPageLinkWithParametersAndPreExistingSession(self):
        page = Page("")
        page.allParams = {"session": "aaaaa"}
        result = PageLink("hello", page, {"team": "aasa", "league": "afafa"}).url
        self.assertEqual("/cgi-bin/page.py?id=hello&session=aaaaa&league=afafa&team=aasa", result)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPageLinkNoParameters']
    unittest.main()