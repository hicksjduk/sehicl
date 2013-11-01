'''
Created on 30 Aug 2013

@author: hicksj
'''
import unittest
from pages.staticpage import StaticPage


class Test(unittest.TestCase):


    def testGetTitle(self):
        page = StaticPage("hello", "statichtml/rules.html", "SEHICL Rules and Playing Conditions")
        result = page.getTitle()
        self.assertEquals("SEHICL Rules and Playing Conditions", result)

    def testGetContent(self):
        page = StaticPage("hello", "statichtml/rules.html", "SEHICL Rules and Playing Conditions")
        result = page.getContent()
        self.assertNotEqual(None, result)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetTitle']
    unittest.main()