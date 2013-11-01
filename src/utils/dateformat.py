'''
Created on 31 Jul 2013

@author: hicksj
'''

from datetime import datetime
import string

class DateFormatter(object):
    '''
    classdocs
    '''

    @staticmethod
    def formatDate(date, longMonth, longYear):
        monthTerm = "%B" if longMonth else "%b"
        yearTerm = "" if longYear is None else "%Y" if longYear else "%y"
        ordinalSuffix = DateFormatter.getOrdinalSuffix(date.day)
        dateFormat = "%d{0} {1} {2}".format(ordinalSuffix, monthTerm, yearTerm)
        answer = string.lstrip(date.strftime(dateFormat), "0").strip()
        return answer;
    
    @staticmethod
    def formatDateToISO(date):
        dateFormat = "%Y-%m-%d"
        answer = date.strftime(dateFormat)
        return answer;
    
    @staticmethod
    def getOrdinalSuffix(day):
        answer = "th"
        if day < 11 or day > 13:
            unit = day % 10
            if unit == 1:
                answer = "st"
            elif unit == 2:
                answer = "nd"
            elif unit == 3:
                answer = "rd"
        return answer

    @staticmethod
    def formatTime(time):
        timeFormat = "%I:%M"
        answer = string.lstrip(time.strftime(timeFormat), "0")
        return answer;

    @staticmethod
    def parseDateTimeFromString(theString):
        dateFormat = "%Y-%m-%d.%H:%M"
        answer = datetime.strptime(theString, dateFormat)
        return answer
    
    @staticmethod
    def parseDateFromString(theString):
        dateFormat = "%Y-%m-%d"
        answer = datetime.strptime(theString, dateFormat).date()
        return answer
                