# -*- coding: utf-8 -*-

# Check current Python version: Python 2 or 3 ?
class A(object):
    def b(self):
        pass
if A.b is A.b:
    # Python3
    from configparser import ConfigParser
else:
    # Python2
    from ConfigParser import ConfigParser
import os
import sys

# Switch prod and dev settings here
# ENVIRONMENT = 'production'
ENVIRONMENT = 'develop'
# ENVIRONMENT = 'demo'

class ConfigurationReader(object):

    APP_BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    if 'production' == ENVIRONMENT:
        CONFIGFILE = APP_BASE_DIR + "/setting/prod_setting.cfg"
    elif 'develop' == ENVIRONMENT:
        CONFIGFILE = APP_BASE_DIR + "/setting/dev_setting.cfg"
    else:
        CONFIGFILE = APP_BASE_DIR + "/setting/demo_setting.cfg"
    config = ConfigParser()
    config.read(CONFIGFILE)

    # def __init__(self):
    #     return

    # def read_configuration(self, section, *args):
    #     if 1 == len(args):  # good habit
    #         # if only one param, then no need to be a list type
    #         s = self.config.get(section, args[0])
    #         return s
    #     else:
    #         # if move than one param have been passed here, then use list type
    #         l = []
    #         for i in args:
    #             i = self.config.get(section, i)
    #             l.append(i)
    #         return l

    def read_configuration(self, section, *args):
        for i in args:
            c = self.config.get(section, i)
            yield c