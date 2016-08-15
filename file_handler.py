# -*- coding: utf-8 -*-
# file_handler.py

from OldFileCleaner import *
from ConfigurationReader import ConfigurationReader  # 前面是模块名，后面是类名

c = ConfigurationReader()
SETTING_subfolder = c.read_configuration('path', 'subfolder')
subfolder_list = SETTING_subfolder.split(', ')

def call_OldFileCleaner_func():
    c = OldFileCleaner()
    c.check_file_age(age_day=2, age_hour=0, subfolder_list=subfolder_list)
    return

if __name__ == "__main__":
    call_OldFileCleaner_func()