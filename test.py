# -*- coding: utf-8 -*-

"""
"""

"""
Test ConfigurationReader module. Test case verified.
"""
# from ConfigurationReader import ConfigurationReader
# c = ConfigurationReader()
# config1, config2 = (x for x in c.read_configuration('path', 'base_dir', 'service_restarted'))
# print(config1)
# print(config2)

"""
Test WinServicesDaemon module.
"""
# from file_handler import call_OldFileCleaner_func
# call_OldFileCleaner_func()

"""
Test OldFileCleaner module.
"""
from OldFileCleaner import OldFileCleaner
c = OldFileCleaner()
c.check_file_age()

"""
Test mail_sender module. Test case verified.
"""
# from mail_sender import mail_sender
# mail_sender(mail_subject="test of subject", mail_content="test of content")