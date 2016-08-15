# -*- coding: utf-8 -*-
# WinServicesDaemon

### Usage : python ***.py install (or / then start, stop, remove)
# Run Python scripts as WinService
# Register as WinService: ...>RestartServiceSchedule.py install

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
c = ConfigurationReader()
SETTING_svc_name, SETTING_svc_display_name, SETTING_svc_description = \
    c.read_configuration('name', 'svc_name', 'svc_display_name', 'svc_description')
SETTING_logfile, SETTING_service_restarted = \
    c.read_configuration('path', 'logfile', 'service_restarted')

class WinServicesDaemon(win32serviceutil.ServiceFramework):
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
        # self.timeout = 640000  # 640 seconds / 10 minutes (value is in milliseconds)
        self.timeout = 10000    # 120 seconds / 2 minutes

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        # This is how long the service will wait to run / refresh itself (see script below)
        logging.basicConfig(filename=SETTING_logfile, filemode='a', level=logging.DEBUG)
        # logging.debug("DEBUG. This msg should go to the log file. Remove this one when complete")
        # logging.info("INFO. So should this one. Remove this one when complete")
        # logging.warning("WARNING. And this one, too. Remove this one when complete")
        self.main()

    def service_restart(self):
         # Use minidom Xlator to open XML doc
        dom_tree = xml.dom.minidom.parse(SETTING_service_restarted)
        collection = dom_tree.documentElement
        if collection.hasAttribute("shelf"):
            logging.debug("Root element : %s #Remove this one when complete"
                          % collection.getAttribute("shelf"))
        # Obtain all services from collection
        services = collection.getElementsByTagName("Service")
        # Print all services' detail info
        for each_service in services:
            if each_service.hasAttribute("title"):
                # print ("Title: %s" % Service.getAttribute("title"))
                service_name = each_service.getElementsByTagName('ServiceName')[0].childNodes[0].data
                # print ("ServiceName: %s" % ServiceName.childNodes[0].data)
                restart_period_sec = each_service.getElementsByTagName('RestartPeriodInSec')[0]
                # print ("RestartPeriod in Sec: %s" % RestartPeriodInSec.childNodes[0].data)
                restart_period_float = float(restart_period_sec.childNodes[0].data)
                # print (Float_RestartPeriod)
        win32serviceutil.RestartService(service_name)
        # print ("%s You should not see me. I\'m in main Func()" % time.asctime(time.localtime(time.time())))
        logging.debug("%s : Service restarted" % time.asctime(time.localtime(time.time())))
        time.sleep(restart_period_float)  # sleep time = self.timeout + Float_RestartPeriod
        self.main()

    def clean_old_file(self):
        while True:
            dom_tree = xml.dom.minidom.parse(SETTING_service_restarted)
            collection = dom_tree.documentElement
            services = collection.getElementsByTagName("Service")
            for each_service in services:
                if each_service.hasAttribute("title"):
                    restart_period_sec = each_service.getElementsByTagName('RestartPeriodInSec')[0]
                    restart_period_float = float(restart_period_sec.childNodes[0].data)
            if not self.stop_requested:
                from file_handler import call_OldFileCleaner_func
                call_OldFileCleaner_func()
                time.sleep(restart_period_float)
            else:
                self.main()

    def main(self):
        while True:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if self.stop_requested:
                # Stop signal encountered
                servicemanager.LogInfoMsg("%s service has stopped." % SETTING_svc_name)  # For Event Log
                break
            else:
                try:
                    # cmd = 'self.' + 'service_restart' + '()'
                    cmd = 'self.' + 'clean_old_file' + '()'
                    exec(cmd)
                    # self.clean_old_file()
                except:
                    pass

def ctrl_handler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrl_handler, True)
    win32serviceutil.HandleCommandLine(WinServicesDaemon)