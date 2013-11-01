'''
Created on 6 Sep 2013

@author: hicksj
'''
from pages.pageloader import PageLoader
import unittest
import sqlite3


class Test(unittest.TestCase):

    def testGetPageTokenSpecifiedAndRight(self):
        params = {"session": "abc"}
        conn = sqlite3.connect(":memory:")
        try:
            conn.cursor().execute("drop table session")
        except:
            pass
        conn.cursor().execute("create table session (id, token, expiry)")
        conn.cursor().execute("insert into session (id, token) values (1, 'abc')")
        result = PageLoader().getPage(params, conn)
        conn.close();
        redirectLink = """
            <meta http-equiv="refresh" content="0;url=/cgi-bin/page.py?id=home">        
        """
        self.assertEqual(-1, result.find(redirectLink.strip()))

    def testGetPageTokenSpecifiedAndWrongButNotRequired(self):
        params = {"session": "aaa"}
        conn = sqlite3.connect(":memory:")
        try:
            conn.cursor().execute("drop table session")
        except:
            pass
        conn.cursor().execute("create table session (id, token, expiry)")
        result = PageLoader().getPage(params, conn)
        conn.close();
        redirectLink = """
            <meta http-equiv="refresh" content="0;url=/cgi-bin/page.py">        
        """
        self.assertNotEqual(-1, result.find(redirectLink.strip()))

    def testGetPageTokenSpecifiedAndWrongAndRequired(self):
        params = {"session": "agsgas", "id": "fullContacts"}
        conn = sqlite3.connect(":memory:")
        try:
            conn.cursor().execute("drop table session")
        except:
            pass
        conn.cursor().execute("create table session (id, token, expiry)")
        result = PageLoader().getPage(params, conn)
        conn.close();
        redirectLink = """
            <meta http-equiv="refresh" content="0;url=/cgi-bin/page.py?id=fullContacts">        
        """
        self.assertNotEqual(-1, result.find(redirectLink.strip()))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetPage']
    unittest.main()