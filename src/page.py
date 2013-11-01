#!/usr/bin/python
from cgi import FieldStorage
import sys
import os

root = os.environ("HOME")
sys.path.insert(0, root + "/python")

from pages.settings import Settings
Settings.setRootDirectory(root)

from pages.pageloader import PageLoader

import cgitb; cgitb.enable()

print ("Content-Type: text/html\n")

parms = FieldStorage()
paramDict = {} 
for k in parms.keys():
    paramDict[k] = parms.getvalue(k)

print (PageLoader().getPage(paramDict))

