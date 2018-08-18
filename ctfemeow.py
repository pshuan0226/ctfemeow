#!/usr/bin/python

import smtplib

config = {}
execfile('config.py', config)

session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(config['sender_email_id'], config['sender_email_id_password'])
message = 'test'
session.sendmail(config['sender_email_id'], config['sender_email_id_password'], message)
session.quit()
