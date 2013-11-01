'''
Created on 3 Sep 2013

@author: hicksj
'''
import unittest
from pages.pageList import PageList


class Test(unittest.TestCase):


    def testPageList(self):
        PageList.pages


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testPageList']
    unittest.main()