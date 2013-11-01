'''
Created on 30 Jul 2013

@author: hicksj
'''
from pages.home import HomePage
import unittest
import string


class Test(unittest.TestCase):


    def testGetNewsEmptyNewsSpecified(self):
        news = []
        result = HomePage("").getNews(news)
        self.assertEquals("", result)

    def testGetNewsNonEmptyNewsSpecified(self):
        news = ["Hello"]
        result = HomePage("").getNews(news)
        self.assertEquals(1, string.count(result, "<p>"))
        
    def testGetNewsDefaultNews(self):
        result = HomePage("").getNews()
        self.assertTrue(result is not None)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()