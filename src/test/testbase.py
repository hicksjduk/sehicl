'''
Created on 1 Aug 2013

@author: hicksj
'''
import unittest


class TestBase(unittest.TestCase):

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
        count = 1
        for e, a in zip(explines, actlines):
            self.assertEquals(e, a, "{0}: {1} != {2}".format(count, e, a))
            count = count + 1
        self.assertEqual(len(explines), len(actlines))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()