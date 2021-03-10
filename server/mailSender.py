#! /usr/local/bin/python
import sys
import os
import re

from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)

# old version
# from email.MIMEText import MIMEText
from email.mime.text import MIMEText

SMTPserver = 'smtp.gmail.com'
sender =     '*****@gmail.com'

USERNAME = "*****@gmail.com"
PASSWORD = "*****"

destination = []

def send(content, usr):
    destination.append(usr)

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    subject = "Do NOT respond. SNA  - Dump uploaded succesfully"

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender  # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string()+'. Please login to login into the app to see your graph')
        finally:
            conn.quit()

    except:
        sys.exit("mail failed; %s" % "CUSTOM_ERROR")  # give an error message
