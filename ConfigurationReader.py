# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser

# Switch prod and dev settings here
ENVIRONMENT = 'develop'
# ENVIRONMENT = 'production'

class ConfigurationReader():

    if 'develop' == ENVIRONMENT:
        CONFIGFILE = "D:\\GitHub\\repositories\\WinServiceDaemon\\setting\\dev_setting.cfg"
    else:
        # CONFIGFILE = "D:\\NNIT_APP\\WinServiceDaemon\\setting\\prod_setting.cfg"  # real production env
        CONFIGFILE = "D:\\GitHub\\repositories\\WinServiceDaemon\\setting\\prod_setting.cfg"  # fake production env
    config = ConfigParser()
    config.read(CONFIGFILE)

    def __init__(self):
        # self.config = config
        return

    def read_configuration(self, section, *args):
        if 1 == len(args):  # good habit
            # if only one param, then no need to be a list type
            s = self.config.get(section, args[0])
            return s
        else:
            # if move than one param have been passed here, then use list type
            l = []
            for i in args:
                i = self.config.get(section, i)
                l.append(i)
            return l

# c = ConfigurationReader()
# d = c.read_configuration('path', 'base_dir', 'service_restarted')

# class A(object):
#     def b(self):
#         pass
# if A.b is A.b:
#     # Python3
# else:
#     # Python2