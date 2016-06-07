'''
Created on 29 Jul 2013

@author: hicksj
'''
class Settings:
    defaultPage = "home"
    defaultSeason = 16
    
    rootDirectory = None
    dataDirectory = None
    staticHtmlDirectory = None
    usersDirectory = None
    newsDirectory = None
    
    @staticmethod
    def setRootDirectory(root):
        Settings.rootDirectory = root
        Settings.dataDirectory = "{0}/data".format(root)
        Settings.staticHtmlDirectory = "{0}/statichtml".format(root)
        Settings.usersDirectory = "{0}/users".format(root)
        Settings.newsDirectory = Settings.staticHtmlDirectory + "/news"

    @staticmethod
    def updateParams(params):
        season = int(params.get("season", Settings.defaultSeason))
        xmlFile = "{2}/{0}-{1:02d}.xml".format(1999 + season, season, Settings.dataDirectory)
        params["xmlFile"] = xmlFile;
        