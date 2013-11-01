'''
Created on 30 Jul 2013

@author: hicksj
'''

class Mailto:
    '''
    classdocs
    '''


    def __init__(self, userid, linkText, domain="", description=""):
        '''
        Constructor
        '''
        html = """<script language="javascript">
            document.write(mailTo("{theId}", "{theDomain}", "{theDescription}", "{theLinkText}"));
        </script>
        <noscript>{theLinkText}<i> (Javascript not enabled: cannot display mail link)</i>
        </noscript>"""
        self.html = html.format(theId = userid, theDomain = domain, theDescription = description, theLinkText = linkText)
