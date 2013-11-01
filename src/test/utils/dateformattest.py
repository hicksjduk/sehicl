'''
Created on 31 Jul 2013

@author: hicksj
'''
import unittest
from utils.dateformat import DateFormatter
import datetime


class DateFormatterTest(unittest.TestCase):

    def testGetOrdinalSuffix(self):
        expectedResults = "st nd rd th th th th th th th th th th th th th th th th th st nd rd th th th th th th th st".split()
        count = len(expectedResults)
        self.assertEquals(31, count)
        results = [DateFormatter.getOrdinalSuffix(day) for day in range(1, count + 1)]
        self.assertEquals(expectedResults, results)

    def testFormatDateDatePassedMonthShortYearShort(self):
        date = datetime.date(2013, 1, 3)
        result = DateFormatter.formatDate(date, False, False)
        expectedResult = "3rd Jan 13"
        self.assertEqual(expectedResult, result)

    def testFormatDateDatePassedMonthShortYearLong(self):
        date = datetime.date(2013, 12, 22)
        result = DateFormatter.formatDate(date, False, True)
        expectedResult = "22nd Dec 2013"
        self.assertEqual(expectedResult, result)

    def testFormatDateDatePassedMonthLongYearShort(self):
        date = datetime.date(2013, 4, 12)
        result = DateFormatter.formatDate(date, True, False)
        expectedResult = "12th April 13"
        self.assertEqual(expectedResult, result)

    def testFormatDateDatePassedMonthLongYearLong(self):
        date = datetime.date(2013, 7, 1)
        result = DateFormatter.formatDate(date, True, True)
        expectedResult = "1st July 2013"
        self.assertEqual(expectedResult, result)

    def testFormatDateDateTimePassed(self):
        date = datetime.datetime(2013, 7, 31, 14, 13)
        result = DateFormatter.formatDate(date, True, True)
        expectedResult = "31st July 2013"
        self.assertEqual(expectedResult, result)

    def testFormatDateYearOmitted(self):
        date = datetime.datetime(2013, 7, 31, 14, 13)
        result = DateFormatter.formatDate(date, False, None)
        expectedResult = "31st Jul"
        self.assertEqual(expectedResult, result)
        
    def testFormatDateToISO(self):
        date = datetime.datetime(2013, 4, 7, 16, 25)
        result = DateFormatter.formatDateToISO(date)
        expectedResult = "2013-04-07"
        self.assertEqual(expectedResult, result)

    def testFormatTimeTimePassed(self):
        time = datetime.time(14, 13)
        result = DateFormatter.formatTime(time)
        expectedResult = "2:13"
        self.assertEqual(expectedResult, result)

    def testFormatTimeDateTimePassed(self):
        time = datetime.datetime(2013, 7, 26, 12, 13)
        result = DateFormatter.formatTime(time)
        expectedResult = "12:13"
        self.assertEqual(expectedResult, result)
    
    def testParseDateTimeFromString(self):
        theString = "2013-07-31.17:00"
        expectedResult = datetime.datetime(2013, 7, 31, 17, 0)
        result = DateFormatter.parseDateTimeFromString(theString)
        self.assertEqual(expectedResult, result)

    def testParseDateFromString(self):
        theString = "2013-07-31"
        expectedResult = datetime.date(2013, 7, 31)
        result = DateFormatter.parseDateFromString(theString)
        self.assertEqual(expectedResult, result)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGetOrdinalSuffix']
    unittest.main()