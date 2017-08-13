#!/usr/bin/env python
from smtplib import SMTP, SMTPAuthenticationError
from datetime import datetime
from pytz import timezone
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from sys import exit
import os
import logging

fromaddr = os.environ['EMAIL_USER']
toaddr = os.environ['DEST_EMAIL']
logfile = os.environ['EMAIL_LOG_FILE']
timeft = '%Y-%m-%d %H:%M:%S %Z%z'

logger = logging.getLogger('emailstart')
hdlr = logging.FileHandler(logfile)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

logger.info('Server restarted. Sending email alert.')

server = SMTP('smtp.gmail.com', 587)
server.starttls()

try:
    logger.info('Logging in to smtp server.')
    server.login(fromaddr, os.environ['EMAIL_PASSWD'])
except SMTPAuthenticationError as err:
    logger.info('Unable to login.\n\nResponse: {}'.format(err))
    code = err[0]
    if code == 535:
        logger.info('Wrong username or password. Check your password.')
    if code == 534:
        logger.info('Google did not authorize access to smtp for this IP. Authorize on mobile/web account settings.')
    server.quit()
    exit(1)

logger.info('Successfully logged in.')

time_now = datetime.now(timezone('US/Eastern'))
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'RIA Server Restart Alert'
body = 'RIA FBI-API server has been restarted, at: ' + time_now.strftime(timeft)
msg.attach(MIMEText(body, 'plain'))

server.sendmail(fromaddr, toaddr, msg.as_string())

logger.info('Email sent. Goodbye!')

server.quit()
exit(0)
