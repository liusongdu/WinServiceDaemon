# -*- coding: utf-8 -*-

from datetime import datetime
import time

timeformat = '%Y-%m-%d %H:%M:%S'

class TimeConversion(object):
    """convert datetime to float

    """
    def __init__(self):
        self.__time_conversion_dt_float = None
        self.time_datetime = None
        self.__time_conversion_float_str = None
        self.time_float = None
        self.__time_conversion_str_float = None
        self.time_str = None

    # time data type convert from datetime.datetime to float
    @property
    def time_conversion_dt_float(self):
        """Get the current time_convert_result."""
        return self.__time_conversion_dt_float

    @time_conversion_dt_float.setter
    def time_conversion_dt_float(self, time_datetime):
        self.__time_conversion_dt_float = time.mktime(time.strptime
                                                      (time_datetime.strftime(timeformat), timeformat))

    # time data type convert from float to str
    @property
    def time_conversion_float_str(self):
        """Get the current time_convert_result."""
        return self.__time_conversion_float_str

    @time_conversion_float_str.setter
    def time_conversion_float_str(self, time_float):
        # str(datetime.datetime.fromtimestamp(v))
        # time_str = time_datetime.strftime(timeformat)   # type is converted to str
        self.__time_conversion_float_str = datetime.fromtimestamp(time_float).\
            strftime(timeformat)
        # self.__time_convert_float_str = time.strftime(timeformat, time.localtime(time_float))

    # time data type convert from str to float
    @property
    def time_conversion_str_float(self):
        """Get the current time_convert_result."""
        return self.__time_conversion_str_float

    @time_conversion_str_float.setter
    def time_conversion_str_float(self, time_str):
        self.__time_conversion_str_float = time.mktime(
            time.strptime(time_str, timeformat))

    # t = time.strptime("30 Jun 1997 22:59:60", "%d %b %Y %H:%M:%S")
    # datetime(*t[:5] + (min(t[5], 59), ))
