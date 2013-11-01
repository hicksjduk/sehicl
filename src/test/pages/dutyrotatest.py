'''
Created on 11 Sep 2013

@author: hicksj
'''
import unittest
from pages.dutyrota import DutyRota


class Test(unittest.TestCase):


    def testDutyRotaNoDuties(self):
        page = DutyRota("");
        page.duties = []
        page.getContent()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDutyRotaNoDuties']
    unittest.main()