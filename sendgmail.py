#USAGE: python3 sendgmail.py email.json
 
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys
import json


def email_Info(email_json):
    print('---email_json---')
    print('  User: ',email_json['User'])
    print('  Subject: ',email_json['Subject'])
    print('  Content: ',email_json['Content'])
    print('  Receivers: ',email_json['Receivers'])
    print('  Attachment: ',email_json['Attachment'])
    print('---email_json---\n')



email_json = json.load(open(sys.argv[1],'r'))
email_Info(email_json)

sender = email_json['User']['sender']
passwd = email_json['User']['passed']
receivers = email_json['Receivers']
 
emails = receivers.split(',')
msg = MIMEMultipart()
msg['Subject'] = email_json['Subject']
msg['From'] = sender
msg['To'] = receivers

# load content.txt
msg.preamble = 'Multipart massage.\n'
content = MIMEText(open(email_json['Content']).read())
msg.attach(content)

# load attachments
attachs = email_json['Attachment'].split(',')
for attach in attachs:
    print(attach)
    part = MIMEApplication(open(attach,"rb").read())
    part.add_header('Content-Disposition', 'attachment', filename=attach)
    msg.attach(part)


if len(emails) > 0:
    smtp = smtplib.SMTP("smtp.gmail.com:587")
    smtp.ehlo()
    smtp.starttls()
    smtp.login(sender, passwd)
    smtp.sendmail(msg['From'], emails , msg.as_string())
    print ('Send mails to',msg['To'])
    
