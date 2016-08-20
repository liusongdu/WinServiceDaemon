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
    mail_body = '''<html><head></head><body>
    <p>An automatic job has run completely, which is to clean up old backup file(s) more than 2 days.<br/>
    Refer to below report.</p>
    <p><table width = "900" border ="1" cellspacing = "0" cellpadding = "2">
    <tr><td>Deleted file(s):</td><td>Backup file create date:</td></tr>''' + mail_content \
                + "</table></p><p>Powered by LEOD.</p></body></html>"
    msg.attach(MIMEText(mail_body, 'html'))
    s = smtplib.SMTP(SETTING_mail_server)
    if 'develop' == SETTING_environment:
        s.starttls()
        SETTING_password, = \
            (x for x in c.read_configuration('mail', 'password'))
        s.login(SETTING_from_mailbox, SETTING_password)
    s.sendmail(SETTING_from_mailbox, tolist, msg.as_string())
    s.quit()