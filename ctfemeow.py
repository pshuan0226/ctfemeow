#!/usr/bin/python

import smtplib
import requests
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

#grab email credentials for sender
config = {}
execfile('config.py', config)

#create session to send email
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(config['sender_email_id'], config['sender_email_id_password'])
message = 'test'
session.sendmail(config['sender_email_id'], config['sender_email_id_password'], message)
session.quit()
