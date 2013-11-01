'''
Created on 12 Aug 2013

@author: hicksj
'''
from pages.users import UserRegistration
import unittest


class Test(unittest.TestCase):


    def testProcessRegistrationData(self):
        page = UserRegistration("")
        page.allParams = {"name": "Hello", "email": "email", "emailconf": "email", "password": "pw", "passwordconf": "pw"}
        page.processRegistrationData()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testProcessRegistration']
    unittest.main()