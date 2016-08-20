# -*- coding: utf-8 -*-
# old file clean up

from datetime import datetime, timedelta
import os
from ConfigurationReader import ConfigurationReader
from mail_sender import mail_sender
from TimeConversion import TimeConversion

c = ConfigurationReader()
SETTING_base_dir, SETTING_subfolder = \
    (x for x in c.read_configuration('path', 'base_dir', 'subfolder'))
subfolder_list = SETTING_subfolder.split(', ')

class OldFileCleaner(object):
    def __init__(self):
        self.age_day = 2
        self.age_hour = 0
        self.subfolder_list = subfolder_list
        self.delete_file = {}
        self.delete_file_str = ''

    def check_file_age(self):
        """
        list all file names with the full paths
        """
        list_path = (os.path.join(SETTING_base_dir, eachsubfolder) for eachsubfolder
                     in subfolder_list if os.path.isdir(os.path.join(SETTING_base_dir, eachsubfolder)))
                     # os.path.isdir(x) 判断x是(不是)一个目录
                     # list_path: a generator of elements (E:\IPT Backups\test1), only full path without filename

        def list_file():
            for path_list in list_path:
                list1 = os.listdir(path_list)  # os.listdir(path_list) 列出path_list下的目录和文件, type is list
                # list1: ['New Text Document.txt', 'notes.txt', 'testfile.test'] (only filename without path)

                # path2 = (os.path.join(path_list, eachfilename)
                #          for eachfilename in list1
                #          if os.path.isfile(os.path.join(path_list, eachfilename)))

                for eachfilename in list1:
                    path2 = os.path.join(path_list, eachfilename)
                    if os.path.isfile(path2):  # os.path.isfile(path)判断path是不是一个文件，不存在path也返回false
                        yield path2

        p = TimeConversion()
        t = TimeConversion()
        p.time_conversion_dt_float = datetime.now() - timedelta(days=self.age_day, hours=self.age_hour)

        file_list = list_file()
        # file_list: a generator of elements (E:\IPT Backups\test1\New Text Document.txt)

        self.delete_file = {y: int(os.path.getmtime(y)) for y in file_list if
                            ((not os.path.isdir(y)) and (os.path.getmtime(y) <= p.time_conversion_dt_float))}
                            # type of os.path.getmtime() is float
                            # omitted decimal part of second
                            # delete_file: dict with one key:value pair:
                            # E:\IPT Backups\test2\testfile.test : 2016-07-21 20:19:16
        for k, v in self.delete_file.items():
            os.remove(k)  # delete folder or file
            t.time_conversion_float_str = v
            self.delete_file_str += """<tr>
            <td>""" + k + """</td>
            <td>""" + t.time_conversion_float_str + """</td>
            </tr>"""
        if '' == self.delete_file_str:
            self.delete_file_str = '''<tr><td>There is currently no backup file that need cleaning up. Cheers!</td>
            <td>N/A</td></tr>'''
        mail_sender(mail_subject="Old backup files have been handled", mail_content=self.delete_file_str)

''''
os.getcwd()：获得当前工作目录
os.curdir:返回当前目录（'.')
os.chdir(dirname):改变工作目录到dirname
os.path.isdir(name):判断name是不是一个目录，name不是目录就返回false
os.path.exists(name):判断是否存在文件或目录name
os.path.getsize(name):获得文件大小，如果name是目录返回0L
os.path.abspath(name):获得绝对路径

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