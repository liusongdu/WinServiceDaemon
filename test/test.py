# -*- coding: utf-8 -*-

"""
"""

"""
Test ConfigurationReader module.
"""
from ConfigurationReader import ConfigurationReader
c = ConfigurationReader()
d = c.read_configuration('path', 'base_dir', 'service_restarted')
print(d)

"""
Test WinServicesDaemon module.
"""

"""
Test WinServicesDaemon module.
"""
from file_handler import call_OldFileCleaner_func
call_OldFileCleaner_func()

"""
Test OldFileCleaner module.
"""

"""
Test mail_sender module.
"""
from mail_sender import mail_sender
mail_sender(mail_subject="test of subject", mail_content="test of content")