# -*- coding: utf-8 -*-
# mail_sender.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ConfigurationReader import ConfigurationReader

c = ConfigurationReader()
SETTING_from_mailbox, SETTING_to_mailbox, SETTING_mail_server = \
    (x for x in c.read_configuration('mail', 'from_mailbox', 'to_mailbox', 'mail_server'))
SETTING_environment, = \
    (x for x in c.read_configuration('environment', 'environment'))
    # MUST have comma after SETTING_environment, otherwise it would return generator-type data

def mail_sender(mail_subject="test", mail_content="test"):
    tolist = SETTING_to_mailbox.split('; ')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_subject
    msg['From'] = SETTING_from_mailbox
    msg['To'] = SETTING_to_mailbox
    msg.attach(MIMEText(mail_content, 'html'))
    s = smtplib.SMTP(SETTING_mail_server)
    if 'develop' == SETTING_environment:
        s.starttls()
        SETTING_password, = \
            (x for x in c.read_configuration('mail', 'password'))
        s.login(SETTING_from_mailbox, SETTING_password)
    s.sendmail(SETTING_from_mailbox, tolist, msg.as_string())
    s.quit()