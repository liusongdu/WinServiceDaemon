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
# from ConfigParser import ConfigParser
import os
import sys

# Switch prod and dev settings here
# ENVIRONMENT = 'production'
ENVIRONMENT = 'develop'
# ENVIRONMENT = 'demo'

class ConfigurationReader(object):

    # sys.path.append(r"D:\GitHub\repositories\WinServiceDaemon")
    # APP_BASE_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))
    # APP_BASE_DIR = os.path.split(os.path.realpath(sys.argv[0]))[0]
    APP_BASE_DIR = r"D:\GitHub\repositories\WinServiceDaemon"

    if 'production' == ENVIRONMENT:
        CONFIGFILE = APP_BASE_DIR + "/setting/prod_setting.cfg"
    elif 'develop' == ENVIRONMENT:
        CONFIGFILE = os.path.normpath(APP_BASE_DIR + "/setting/dev_setting.cfg")  # 规范path字符串形式
        # CONFIGFILE = r"D:\GitHub\repositories\WinServiceDaemon\setting\dev_setting.cfg"
    else:
        CONFIGFILE = APP_BASE_DIR + "/setting/demo_setting.cfg"
    config = ConfigParser()
    config.read(CONFIGFILE)

    # def __init__(self):
    #     return

    def read_configuration(self, section, *args):
        for i in args:
            c = self.config.get(section, i)
            yield c

if __name__ == "__main__":
    print(os.path.realpath(sys.argv[0]))
    print(os.path.split(os.path.realpath(sys.argv[0])))
    print(os.path.split(os.path.realpath(sys.argv[0]))[0])