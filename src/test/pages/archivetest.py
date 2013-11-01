'''
Created on 2 Sep 2013

@author: hicksj
'''
import unittest
from pages.archive import ArchiveSeasonIndex


class Test(unittest.TestCase):


    def testSeasonArchiveIndexConstructorNoPresentation(self):
        page = ArchiveSeasonIndex("archive7")
        self.assertEquals(7, page.season)
        self.assertEquals(False, page.presentation)

    def testSeasonArchiveIndexConstructorWithPresentation(self):
        page = ArchiveSeasonIndex("archive8")
        self.assertEquals(8, page.season)
        self.assertEquals(True, page.presentation)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testSeasonArchiveIndexConstructorNotDynamicNoPresentation']
    unittest.main()