'''
Created on 30 Jul 2013

@author: hicksj
'''
from pages.home import HomePage
from pages.settings import Settings
import unittest
import string


class Test(unittest.TestCase):


    def testGetNewsEmptyNewsDir(self):
        Settings.setRootDirectory("testData/news/empty")
        result = HomePage("").getNews()
        self.assertEquals("", result)

    def testGetNewsExpiredNewsDir(self):
        Settings.setRootDirectory("testData/news/expired")
        result = HomePage("").getNews()
        self.assertEquals("", result)

    def testGetNewsNonEmptyNewsDir(self):
        Settings.setRootDirectory("testData/news/notexpired")
        result = HomePage("").getNews()
        self.assertEquals(1, string.count(result, "<p>"))
        
    def testGetNewsDefaultNews(self):
        Settings.setRootDirectory(".")
        result = HomePage("").getNews()
        self.assertTrue(result is not None)
        print(result)
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()