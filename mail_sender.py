# -*- coding: utf-8 -*-
# mail_sender.py

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ConfigurationReader import ConfigurationReader  # 前面是模块名，后面是类名
c = ConfigurationReader()
SETTING_from_mailbox, SETTING_to_mailbox, SETTING_mail_server, SETTING_password = \
    c.read_configuration('mail', 'from_mailbox', 'to_mailbox', 'mail_server', 'password')
SETTING_environment = c.read_configuration('environment', 'environment')

def mail_sender(mail_subject="test", mail_content="test"):
    tolist = SETTING_to_mailbox.split('; ')
    msg = MIMEMultipart('alternative')
    msg['Subject'] = mail_subject
    msg['From'] = SETTING_from_mailbox
    msg['To'] = SETTING_to_mailbox
    # part1 = MIMEText(mail_content, 'plain')
    part2 = MIMEText(mail_content, 'html')
    # msg.attach(part1)
    msg.attach(part2)
    s = smtplib.SMTP(SETTING_mail_server)
    if 'develop' == SETTING_environment:
        s.starttls()
        s.login(SETTING_from_mailbox, SETTING_password)
    s.sendmail(SETTING_from_mailbox, tolist, msg.as_string())
    s.quit()

mail_sender(mail_subject="test of subject", mail_content="test of content")