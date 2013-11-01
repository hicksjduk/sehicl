#!/usr/bin/python
import sys
sys.path.insert(0, sys.path[0] + "/../../python")
from sehicl.email.emailsender import EmailSender

print ("Content-Type: text/html\n")
addressees = ["jeremy@thehickses.org.uk", "jerhicks@cisco.com"]
subject = "Another test"
message = "This is another test message"
EmailSender().sendMessage(addressees, subject, message)
print("Message sent successfully")
