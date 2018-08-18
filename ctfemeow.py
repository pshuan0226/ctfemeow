#!/usr/bin/python

import smtplib
import urllib, json
import requests
import httplib2
import os
import oauth2client
import base64
import email.MIMEText
import email.MIMEBase
import icalendar
from email.MIMEMultipart import MIMEMultipart
from datetime import datetime
from oauth2client import client, tools


#check for date
today = datetime.today()
stime = datetime.today().strftime('%s')
etime = datetime(today.year, today.month + 1, 1).strftime('%s')

#grab ctf information and save to a dictionary
ctfs={}
limit = 5 #TODO: change to 100 
url = 'https://ctftime.org/api/v1/events/?limit=&%sstart=%s&finish=%s' % (limit, stime, etime)
response = urllib.urlopen(url)
ctfs = json.loads(response.read())

#create calendar file
cal = icalendar.Calendar()
for ctf in ctfs:
    #only add online ctfs
    if ctf['onsite'] == 'true':
        continue
    event = icalendar.Event()
    event.add('summary', ctf['title'])
    event.add('dstart', ctf['start'])
    event.add('dend', ctf['finish'])
    event.add('description', ctf['description'])
    cal.add_component(event)

filename = 'ctf_events_%s_%s' % (today.year, today.month)
f = open('%s.ics' % filename, 'wb')
f.write(cal.to_ical())
#close file
f.close()


SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'ctfemeow'

#send message
sender = 'sender@gmail.com'
to = 'receiver@gmail.com'
subject = 'CTFs of %s-%s' % (today.year, today.month)
msgHtml = 'monthly ctf icalendar invite'
msgPlain = 'monthly ctf icalendar invite'
attachmentFile = filename

SendMessage(sender, to, subject, msgHtml, msgPlain, '%s.ics' % filename)


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-email-send.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def SendMessage(sender, to, subject, msgHtml, msgPlain, attachmentFile=None):
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('gmail', 'v1', http=http)
	message1 = createMessageWithAttachment(sender, to, subject, msgHtml, msgPlain, attachmentFile)
	result = SendMessageInternal(service, "me", message1)

def SendMessageInternal(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return "Error"
    return "OK"

def createMessageWithAttachment(
    sender, to, subject, msgHtml, msgPlain, attachmentFile):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      msgHtml: Html message to be sent
      msgPlain: Alternative plain text message for older email clients          
      attachmentFile: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart('mixed')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    messageA = MIMEMultipart('alternative')
    messageR = MIMEMultipart('related')

    messageR.attach(MIMEText(msgHtml, 'html'))
    messageA.attach(MIMEText(msgPlain, 'plain'))
    messageA.attach(messageR)

    message.attach(messageA)

    print("create_message_with_attachment: file: %s" % attachmentFile)
    content_type, encoding = mimetypes.guess_type(attachmentFile)

	fp = open(attachmentFile, 'rb')
	msg = email.MIMEBase.MIMEBase('text', "calendar", method="REQUEST", name=filename)
	msg.set_payload(fp.read())
	fp.close()

    filename = os.path.basename(attachmentFile)
	msg.add_header('Content-Description', filename)
	msg.add_header('Content-class', 'urn:content-classes:calendarmessage')
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_string())}
