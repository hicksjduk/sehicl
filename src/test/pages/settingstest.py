'''
Created on 12 Aug 2013

@author: hicksj
'''
import unittest
from pages.settings import Settings


class Test(unittest.TestCase):


    def testSettingsLoad(self):
        Settings()
        
    def testUpdateParamsNoSeasonSpecified(self):
        params = {}
        Settings.defaultSeason = 8
        Settings.setRootDirectory("/home/sehicl")
        Settings.updateParams(params)
        self.assertEquals("/home/sehicl/data/2007-08.xml", params["xmlFile"])

    def testUpdateParamsSeasonSpecified(self):
        params = {"season": "10"}
        Settings.updateParams(params)
        Settings.setRootDirectory("/home/sehicl")
        self.assertEquals("/home/sehicl/data/2009-10.xml", params["xmlFile"])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()