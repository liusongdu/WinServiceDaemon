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

from ConfigParser import ConfigParser
PROD_CONFIGFILE = "D:\\GitHub\\repositories\\WinServiceDaemon\\setting\\prod_setting.cfg"
DEV_CONFIGFILE = "D:\\GitHub\\repositories\\WinServiceDaemon\\setting\\dev_setting.cfg"
config = ConfigParser()

# Switch prod and dev settings here:
# config.read(PROD_CONFIGFILE)
config.read(DEV_CONFIGFILE)

SETTING_NAME_svc_name = config.get('name', 'svc_name')
SETTING_NAME_svc_display_name = config.get('name', 'svc_display_name')
SETTING_NAME_svc_description = config.get('name', 'svc_description')
SETTING_NAME_logfile = config.get('path', 'logfile')
SETTING_NAME_service_restarted = config.get('path', 'service_restarted')

class WinServicesDaemon(win32serviceutil.ServiceFramework):
    """
    API docstring: win32serviceutil is a Python file (module) @ D:\Python34\Lib\site-packages\win32\lib\win32serviceutil.py.
    ServiceFramework is a class within win32serviceutil.py.
    Invoke class 'win32serviceutil.ServiceFramework'.
    """

    _svc_name_ = SETTING_NAME_svc_name
    _svc_display_name_ = SETTING_NAME_svc_display_name
    _svc_description_ = SETTING_NAME_svc_description

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
        self.main()

    def main(self):
        while 1:
            # Wait for service stop signal, if I timeout, loop again
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if self.stop_requested:
                # Stop signal encountered
                servicemanager.LogInfoMsg("NNIT_MonitorNRestartServices has stopped.")  # For Event Log
                break
            else:
                # |<-- Actual service code between rests
                try:
                    logging.basicConfig(filename=SETTING_NAME_logfile, filemode='a', level=logging.DEBUG)
                    # logging.debug("DEBUG. This msg should go to the log file. Remove this one when complete")
                    # logging.info("INFO. So should this one. Remove this one when complete")
                    # logging.warning("WARNING. And this one, too. Remove this one when complete")
                    # Use minidom Xlator to open XML doc
                    dom_tree = xml.dom.minidom.parse(SETTING_NAME_service_restarted)
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
                            service_name = each_service.getElementsByTagName('ServiceName')[0]
                            # print ("ServiceName: %s" % ServiceName.childNodes[0].data)
                            restart_period_sec = each_service.getElementsByTagName('RestartPeriodInSec')[0]
                            # print ("RestartPeriod in Sec: %s" % RestartPeriodInSec.childNodes[0].data)
                            restart_period_float = float(restart_period_sec.childNodes[0].data)
                            # print (Float_RestartPeriod)
                    win32serviceutil.RestartService(service_name.childNodes[0].data)
                    # print ("%s You should not see me. I\'m in main Func()" % time.asctime(time.localtime(time.time())))
                    logging.debug("%s : Service restarted" % time.asctime(time.localtime(time.time())))
                    time.sleep(restart_period_float)  # sleep time = self.timeout + Float_RestartPeriod
                    # t = time.time()
                except:
                    pass
                # actual service code between rests -->|

def ctrl_handler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrl_handler, True)
    win32serviceutil.HandleCommandLine(WinServicesDaemon)