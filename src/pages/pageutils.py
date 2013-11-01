'''
Created on 30 Jul 2013

@author: hicksj
'''
import string
class PageUtils():
    
    @staticmethod
    def getPageUrl(pageId, parms={}):
        url = "/cgi-bin/page.py?id={pId}{extraParms}"
        parmList = string.join([k + "=" + v for k, v in parms], "&")
        answer = url.format(pId=pageId, extraParms=parmList)
        return answer 
    