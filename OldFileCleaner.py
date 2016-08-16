# -*- coding: utf-8 -*-
# old file clean up

import datetime
# import mail_sender
import os
import time
from ConfigurationReader import ConfigurationReader  # 前面是模块名，后面是类名
from mail_sender import mail_sender

timeformat = '%Y-%m-%d %H:%M:%S'

c = ConfigurationReader()
SETTING_base_dir, SETTING_subfolder = c.read_configuration('path', 'base_dir', 'subfolder')
subfolder_list = SETTING_subfolder.split(', ')

class Timeconvert(object):
    """convert datetime to float

    """
    def __init__(self):
        self.__time_convert_result = None
        self.time_datetime = None

    @property
    def time_convert_result(self):
        """Get the current time_convert_result."""
        return self.__time_convert_result

    @time_convert_result.setter
    def time_convert_result(self, time_datetime):
        time_str = time_datetime.strftime(timeformat)   # type is converted to str
        self.__time_convert_result = time.mktime(time.strptime(time_str, timeformat))  # type is converted to float

class OldFileCleaner(object):
    def __init__(self):
        self.age_day = 0
        self.age_hour = 0
        self.subfolder_list = []

    def list_path(self, subfolder_list):
        """ list all file names including full paths to them
        path_list: only full path

        :return:
        path_list is something like ['D:\\pyRegularExpression\\Results\\test\\1', 'D:\\pyRegularExpression\\Results\\test\\2']
        """
        path_list_internal = []
        for i in range(0, len(subfolder_list)):  # at first, i = 0
            path1 = os.path.join(SETTING_base_dir, subfolder_list[i])
            # D:/pyRegularExpression/Results/test/1
            if os.path.isdir(path1):
                # os.path.isdir(path)判断path是不是一个目录，path不是目录就返回false
                path_list_internal.append(path1)
        return path_list_internal

    def list_file(self, subfolder_list):
        """list all file names including full paths to them
        file_list: full path and file name

        :return:
        file_list is something like:
        ['D:\\pyRegularExpression\\Results\\test\\1\\New Text Document (2).txt',
        'D:\\pyRegularExpression\\Results\\test\\1\\New Text Document1.txt',
        'D:\\pyRegularExpression\\Results\\test\\2\\New Text Document (2).txt']
        """
        file_list_internal = []
        path_list = self.list_path(subfolder_list)
        for i in range(0, len(path_list)):
            list1 = os.listdir(path_list[i])
            for j in range(0, len(list1)):
                path2 = os.path.join(path_list[i], list1[j])
                if os.path.isfile(path2):
                    # os.path.isfile(path)判断path是不是一个文件，不存在path也返回false
                    file_list_internal.append(path2)
        return file_list_internal

    '''
    list = os.listdir(base_dir)  # 列出base_dir下的目录和文件, type is list
    filelist = []

    for i in range(0, len(list)):  # at first, i = 0
        path = os.path.join(base_dir, list[i])
        if os.path.isfile(path):  # os.path.isfile(path)判断path是不是一个文件，不存在path也返回false
            filelist.append(list[i])
    '''

    def check_file_age(self):
        age_day = 2
        age_hour = 0
        file_list = self.list_file(subfolder_list)
        delete_file = {}
        for i in range(0, len(file_list)):
            path3 = file_list[i]
            if os.path.isdir(path3):
                continue
            file_modify_time = os.path.getmtime(path3)
            # type is float!!!
            # date = datetime.datetime.fromtimestamp(fileModifyTime)  # type is converted to datetime.datetime
            # print (filelist[i], ' last modify time is: ', date.strftime(timeformat))
            criteria_datetime = datetime.datetime.now() - datetime.timedelta(days=age_day, hours=age_hour)
            # type of end_t2 is datetime.datetime
            # instance
            p = Timeconvert()
            # update, similarly invoke "setter"
            p.time_convert_result = criteria_datetime
            # similarly invoke "getter" via @property
            # print (p.time_convert_result)
            # criteria = self.convert_datetime_to_float(criteria_datetime)
            if file_modify_time <= p.time_convert_result:
                os.remove(file_list[i])  # 删除文件夹或者文件
                delete_file[file_list[i]] = file_modify_time
        empty = 'y'
        delete_file_str = ''
        for k, v in delete_file.items():
            delete_file_str += '<tr><td>' + k + """</td>
            <td>""" + str(datetime.datetime.fromtimestamp(v)) + '</td></tr>'
            empty = 'n'
        if empty == 'y':
            delete_file_str = '''<tr><td>There is currently no backup file that need cleaning up. Cheers!</td>
            <td>N/A</td></tr>'''
        mail_content = '''<html><head></head><body>
        <p>An automatic job has run completely, which is to clean up old backup file(s) more than 2 days.<br/>
        Refer to below report.</p>
        <p><table width = "900" border ="1" cellspacing = "0" cellpadding = "2">
        <tr><td>Deleted file(s):</td><td>Backup file create date:</td></tr>''' + delete_file_str \
                       + "</table></p><p>Powered by LEOD.</p></body></html>"
        mail_sender(mail_subject="Old backup files have been handled", mail_content=mail_content)

    '''
    def convert_datetime_to_float(self, time_datetime):
        """

        :param dt:
        :return:
        """
        time_str = time_datetime.strftime(timeformat)   # type is converted to str
        time_float = time.mktime(time.strptime(time_str, timeformat))  # type is converted to float
        return time_float
    '''

''''
os.getcwd()：获得当前工作目录
os.curdir:返回当前目录（'.')
os.chdir(dirname):改变工作目录到dirname
os.path.isdir(name):判断name是不是一个目录，name不是目录就返回false
os.path.exists(name):判断是否存在文件或目录name
os.path.getsize(name):获得文件大小，如果name是目录返回0L
os.path.abspath(name):获得绝对路径
os.path.normpath(path):规范path字符串形式
os.path.split(name):分割文件名与目录（事实上，如果你完全使用目录，它也会将最后一个目录作为文件名而分离，同时它不会判断文件或目录是否存在）
os.path.splitext():分离文件名与扩展名
os.path.join(path,name):连接目录与文件名或目录
os.path.basename(path):返回文件名
os.path.dirname(path):返回文件路径
os.remove(dir) #dir为要删除的文件夹或者文件路径
os.rmdir(path) #path要删除的目录的路径。需要说明的是，使用os.rmdir删除的目录必须为空目录，否则函数出错。
os.stat(path).st_ctime #获取文件修改时间
os.path.getctime(name)#获取文件的创建时间
'''

# 比较l_time是否在时间区间[start_t, end_t]中
# def compare_time(l_time, end_t):
    # s_time = time.mktime(time.strptime(start_t, '%Y%m%d%H%M'))  # get the seconds for specify date
    # e_time = time.mktime(time.strptime(end_t, '%Y-%m-%d %H:%M:%S'))
    # log_time = time.mktime(time.strptime(l_time, '%Y-%m-%d %H:%M:%S'))
    # if float(log_time) <= float(e_time):  # True means file older than
    #     return True
    # return False

# 输入的时间格式必须跟自己的格式化串保持一致
# 如时间： "2011-11-10 14:56:58"  定义格式串时应该为: "%Y-%m-%d %H:%M:%S"
# 有试过 from datetime import datetime,time , 但是没有成功，暂时没有考虑去解决.