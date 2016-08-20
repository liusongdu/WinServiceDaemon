# -*- coding: utf-8 -*-

"""
"""

"""
Test module. Test case verified.
ConfigurationReader
"""
from ConfigurationReader import ConfigurationReader
import os
import sys

c = ConfigurationReader()
APP_BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
config1, config2 = (x for x in c.read_configuration('path', 'base_dir', 'service_restarted'))
print(os.path.normpath(APP_BASE_DIR + "/setting/dev_setting.cfg"))
print(config1)
print(config2)

"""
Test WinServicesDaemon module.
"""
# from file_handler import call_OldFileCleaner_func
# call_OldFileCleaner_func()

"""
Test module.
file_handler
"""
# from file_handler import call_OldFileCleaner_func
# call_OldFileCleaner_func()

"""
Test OldFileCleaner module.
"""
# from OldFileCleaner import OldFileCleaner
# c = OldFileCleaner()
# c.check_file_age()

"""
Test module. Test case verified.
TimeConversion
"""
import time
from datetime import datetime
# from TimeConversion import TimeConversion
# t = TimeConversion()

# Test dt to float
# time_ori_dt = datetime.now()
# t.time_conversion_dt_float = time_ori_dt
# print (t.time_conversion_dt_float)  # Result e.g. : 1471484558.0

# Test float to str
# time_ori = 1471484558.0
# t.time_conversion_float_str = time_ori
# print(t.time_conversion_float_str)  # Result e.g. : 2016-08-18 09:42:38

# Test str to float
# time_ori = '2016-08-18 09:42:38'
# t.time_conversion_str_float = time_ori
# print(t.time_conversion_str_float)  # Result e.g. : 1471484558.0

# Special consideration
# time_ori = time.strptime("30 Jun 1997 22:59:60", "%d %b %Y %H:%M:%S")
# t = time.strptime("30 Jun 1997 22:59:60", "%d %b %Y %H:%M:%S")  # second ecapse?

"""
Test module. Test case verified.
mail_sender
"""
# from mail_sender import mail_sender
# mail_sender(mail_subject="test of subject",
#             mail_content='''<tr><td>Test of mail body</td>
#             <td>Test of mail body</td></tr>''')