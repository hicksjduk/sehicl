'''
Created on 30 Jul 2013

@author: hicksj
'''
import unittest
from pages.mailto import Mailto


class Test(unittest.TestCase):


    def testMailtoConstructorDomainAbsentDescriptionAbsent(self):
        mailto = Mailto("jeremy", "Jeremy Hicks")
        result = mailto.html
        expectedResult = """<script language="javascript">
            document.write(mailTo("jeremy", "", "", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>"""
        self.assertEqual(expectedResult, result)

    def testMailtoConstructorDomainPresentDescriptionAbsent(self):
        mailto = Mailto("jeremy", "Jeremy Hicks", domain="nds.com")
        result = mailto.html
        expectedResult = """<script language="javascript">
            document.write(mailTo("jeremy", "nds.com", "", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>"""
        self.assertEqual(expectedResult, result)

    def testMailtoConstructorDomainAbsentDescriptionPresent(self):
        mailto = Mailto("jeremy", "Jeremy Hicks", description="aaasaas")
        result = mailto.html
        expectedResult = """<script language="javascript">
            document.write(mailTo("jeremy", "", "aaasaas", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>"""
        self.assertEqual(expectedResult, result)

    def testMailtoConstructorDomainPresentDescriptionPresent(self):
        mailto = Mailto("jeremy", "Jeremy Hicks", domain="nds.com", description="ajghsad")
        result = mailto.html
        expectedResult = """<script language="javascript">
            document.write(mailTo("jeremy", "nds.com", "ajghsad", "Jeremy Hicks"));
        </script>
        <noscript>Jeremy Hicks<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>"""
        self.assertEqual(expectedResult, result)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMailtoConstructor']
    unittest.main()