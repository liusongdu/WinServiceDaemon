# -*- coding: utf-8 -*-
# WinServicesDaemon
# Usage: python WinServiceDaemon.py install (or / then start, stop, remove)

from xml.dom.minidom import parse
from concurrent.futures import *
import xml.dom.minidom
import logging
import os
import pywintypes
import sys, string
import time
import warnings, win32api, win32con, winerror, win32event, win32evtlogutil, win32service, win32serviceutil
import servicemanager
from ConfigurationReader import ConfigurationReader  # 前面是模块名，后面是类名
# from file_handler import call_OldFileCleaner_func

APP_BASE_DIR = r"D:\GitHub\repositories\WinServiceDaemon"
c = ConfigurationReader()
SETTING_svc_name, SETTING_svc_display_name, SETTING_svc_description = \
    (x for x in c.read_configuration('name', 'svc_name', 'svc_display_name', 'svc_description'))
SETTING_logfile, SETTING_service_restarted = \
    ((APP_BASE_DIR + x) for x in c.read_configuration('path', 'logfile', 'service_restarted'))
logging.basicConfig(filename=SETTING_logfile, filemode='a', level=logging.DEBUG)
APP_BASE_DIR = os.path.split(os.path.realpath(sys.argv[0]))[0]
# print(os.path.abspath(sys.argv[0]))

class WinServiceDaemon(win32serviceutil.ServiceFramework):
    """
    API docstring: win32serviceutil is a Python file (module) @ D:\Python34\Lib\site-packages\win32\lib\win32serviceutil.py.
    ServiceFramework is a class within win32serviceutil.py.
    Invoke class 'win32serviceutil.ServiceFramework'.
    """

    _svc_name_ = SETTING_svc_name
    _svc_display_name_ = SETTING_svc_display_name
    _svc_description_ = SETTING_svc_description

    def __init__(self, args):
        """
        API docstring: This is an initialization function, a special method treated by Python.
        The parameter 'self' is to cite the exact object who transfer this method/function.
        The first parameter MUST be 'self' if it is within a class.
        :param args:
        :return:
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.stop_requested = False
        self.timeout = 10000    # in milliseconds
        logging.debug("Initiated")

    def SvcStop(self):
        logging.debug("stop")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True

    def SvcDoRun(self):
        logging.debug("start1")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        # This is how long the service will wait to run / refresh itself (see script below)

        logging.debug("DEBUG. This msg should go to the log file. Remove this one when complete")
        # logging.info("INFO. So should this one. Remove this one when complete")
        # logging.warning("WARNING. And this one, too. Remove this one when complete")
        while True:  # 1st while cycle.
            # Wait for service stop signal, if timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if win32event.WAIT_OBJECT_0 == rc:
            # if self.stop_requested:
                # Stop signal encountered
                servicemanager.LogInfoMsg("%s service has stopped." % SETTING_svc_name)  # For Event Log
                break
            else:
                while True:  # 2nd while cycle
                    dom_tree = xml.dom.minidom.parse(SETTING_service_restarted)
                    collection = dom_tree.documentElement
                    services = collection.getElementsByTagName("Service")
                    restart_period_float = 0
                    for each_service in services:
                        if each_service.hasAttribute("title"):
                            restart_period_sec = each_service.getElementsByTagName('RestartPeriodInSec')[0]
                            restart_period_float = float(restart_period_sec.childNodes[0].data)

                    # |<-- Between lines are for fixing this installed service cannot stop issue
                    # The stop attempt would time out if there is long time of sleep
                    # from OldFileCleaner import OldFileCleaner
                    # c1 = OldFileCleaner()
                    # c1.check_file_age()
                    interval = 20
                    t = restart_period_float / interval  # cycle times
                    while t > 0:  # 3rd while cycle
                        t -= 1
                        time.sleep(interval)
                        if self.stop_requested:
                            servicemanager.LogInfoMsg("%s service has stopped." % SETTING_svc_name)
                            break  # break the 3rd while cycle
                    break  # break the 2nd while cycle
            # break  # break the 1st while cycle
                    # -->|

    # def service_restart(self):
    #      # Use minidom Xlator to open XML doc
    #     dom_tree = xml.dom.minidom.parse(SETTING_service_restarted)
    #     collection = dom_tree.documentElement
    #     if collection.hasAttribute("shelf"):
    #         logging.debug("Root element : %s #Remove this one when complete"
    #                       % collection.getAttribute("shelf"))
    #     # Obtain all services from collection
    #     services = collection.getElementsByTagName("Service")
    #     # Print all services' detail info
    #     for each_service in services:
    #         if each_service.hasAttribute("title"):
    #             # print ("Title: %s" % Service.getAttribute("title"))
    #             service_name = each_service.getElementsByTagName('ServiceName')[0].childNodes[0].data
    #             # print ("ServiceName: %s" % ServiceName.childNodes[0].data)
    #             restart_period_sec = each_service.getElementsByTagName('RestartPeriodInSec')[0]
    #             # print ("RestartPeriod in Sec: %s" % RestartPeriodInSec.childNodes[0].data)
    #             restart_period_float = float(restart_period_sec.childNodes[0].data)
    #             # print (Float_RestartPeriod)
    #     win32serviceutil.RestartService(service_name)
    #     # print ("%s You should not see me. I\'m in main Func()" % time.asctime(time.localtime(time.time())))
    #     logging.debug("%s : Service restarted" % time.asctime(time.localtime(time.time())))
    #     time.sleep(restart_period_float)  # sleep time = self.timeout + Float_RestartPeriod

def ctrl_handler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrl_handler, True)
    win32serviceutil.HandleCommandLine(WinServiceDaemon)