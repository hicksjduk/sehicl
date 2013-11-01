#!/usr/bin/python

import xml.etree.ElementTree as ET
from cgi import FieldStorage
xml = ET.fromstring('<hello>Bonjour</hello>')


print ("Content-type:text/html\r\n\r\n")
print ('<html>')
print ('<head>')
print ('<title>Hello Word - First CGI Program</title>')
print ('</head>')
print ('<body>')
print ('<h2>Hello Word! This is my first CGI program</h2>')
print ('<p>' + xml.text + '</p>')
print (FieldStorage())
print ('</body>')
print ('</html>')