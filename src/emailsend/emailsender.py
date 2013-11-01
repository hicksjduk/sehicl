'''
Created on 4 Sep 2013

@author: hicksj
'''
import smtplib
from email.mime.text import MIMEText
import string
from emailsend.settings import Settings

class EmailSender:

    def sendMessage(self, addressees, subject, message):
        fromaddr = "website@sehicl.org.uk"
        toaddrs = addressees
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["To"] = string.join(addressees, ", ")
        server = smtplib.SMTP(Settings.serverName)
        server.starttls()
        server.login(Settings.userId, Settings.password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()