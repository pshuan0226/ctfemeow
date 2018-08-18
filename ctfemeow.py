#!/usr/bin/python

import smtplib
import requests
import email.MIMEText
import email.MIMEBase
from email.MIMEMultipart import MIMEMultipart
from datetime import datetime
from icalendar import Calendar, Events


#check for date
stime = datetime.today().strftime('%s')
etime = datetime(today.year, today.month + 1, 1).strftime('%s')

#grab ctf information and save to a dictionary
ctfs={}
limit = 100
url = 'https://ctftime.org/api/v1/events/?limit=' + limit + '&start=' + stime + '&finish=' + etime
response = requests.get(url)
ctfs = response.json()

#create calendar file
cal = Calendar()
for ctf in ctfs:
    #only add online ctfs
    if ctf['onsite'] == 'true':
        continue
    event = Event()
    event.add('summary', ctf['title'])
    event.add('dstart', ctf['start'])
    event.add('dend', ctf['finish'])
    event.add('description', ctf['description'])
    cal.add_component(event)

filename = 'ctf_events_' + today.year + '_' + today.month
f = open('%s.ics' % filename, 'wb')
f.write(cal.to_ical())
f.close()

#grab email credentials for sender
config = {}
execfile('config.py', config)

#craft message
msg = MIMEMultipart('alternative')
msg['Subject'] = 'CTFs of %s-%s' % (today.year, today.month)
msg['From'] = config['sender_email_id'] + '@gmail.com'
msg['To'] = config['sender_email_id'] + '@gmail.com'

#attach .ics file
icsfile = email.MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
email.Encoders.encode_base64(icsfile)
icsfile.add_header('Content-Description', filename)
icsfile.add_header('Content-class', 'urn:content-classes:calendarmessage')
msg.attach(icsfile)

#create session to send email
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(config['sender_email_id'], config['sender_email_id_password'])
session.sendmail(config['sender_email_id'], config['sender_email_id_password'], msg)
session.quit()
