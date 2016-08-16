# -*- coding: utf-8 -*-
# file_handler.py

from OldFileCleaner import *

def call_OldFileCleaner_func():
    c = OldFileCleaner()
    c.check_file_age()
    return
