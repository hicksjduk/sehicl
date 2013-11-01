'''
Created on 1 Aug 2013

@author: hicksj
'''
import unittest


class Test(unittest.TestCase):

    def assertMultiLineEqual(self, expected, actual):
        explines = []
        for s in expected.split("\n"):
            ss = s.strip()
            if ss:
                explines.append(ss)
        actlines = []
        for s in actual.split("\n"):
            ss = s.strip()
            if ss:
                actlines.append(ss)
#        self.assertEquals(len(explines), len(actlines))
        count = 1
        for e, a in zip(explines, actlines):
            self.assertEquals(e, a, "{0}: {1} != {2}".format(count, e, a))
            count = count + 1
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()