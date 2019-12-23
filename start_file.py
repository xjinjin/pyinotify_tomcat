# !/usr/bin/env python3.7
# coding:utf-8

# import os
import subprocess
import requests
import time
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_MODIFY

class EventHandler(ProcessEvent):
    """事件处理"""

    def process_IN_CREATE(self, event):
        # print("Create file: %s " % os.path.join(event.path, event.name))
        print('process_IN_CREATE:{}'.format(event.pathname))

        # 判断生成的文件是否符合标准.    1.不符合什么也不做  2.符合从新定位position
        # /home/program/apache-tomcat-8.5.32/logs/localhost_access_log.2019-07-30.txt
        date = time.strftime("%Y-%m-%d", time.localtime())
        file = '/home/program/apache-tomcat-8.5.32/logs/localhost_access_log.{}.txt'.format(date)
        if event.pathname == file:
            create_file()

    # def process_IN_DELETE(self, event):
    #     print("Delete file: %s " % os.path.join(event.path, event.name))

    def process_IN_MODIFY(self, event):
        print('process_IN_MODIFY:{}'.format(event.pathname))
        date = time.strftime("%Y-%m-%d", time.localtime())
        file = '/home/program/apache-tomcat-8.5.32/logs/localhost_access_log.{}.txt'.format(date)
        if event.pathname == file:
            seek_access(event.pathname)
        # # print("Modify file: %s " % os.path.join(event.path, event.name))
        # # print("Modify file: %s " % event.pathname)
        # # print(dir(event))
        # # print(event.dir)    # False
        # # print(event.mask)   # 2
        # # print(event.maskname) # IN_MODIFY
        # # print(event.name)       # ''    localhost_access_log.2019-06-11.txt
        # # print(event.path)       # /home/xjj/pyinotify/  localhost_access_log.2019-06-11.txt
        # # print(event.pathname)   # /home/xjj/pyinotify/localhost_access_log.2019-06-11.txt
        # # print(event.wd)     # 1
        # # if event.pathname == '/home/xjj/pyinotify/localhost_access_log.2019-06-11.txt':
        # cmd = 'tail -1 /home/xjj/pyinotify/localhost_access_log.2019-06-11.txt'
        # res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        # result_str = res.stdout.read().decode(encoding='utf-8') # b'1\n'   b''     []
        # # print(result_str)
        # # print(type(result_str))
        # # 114.83.177.174 - - [11/Jun/2019:23:04:59 +0800] POST /account/loadWarningInfo.htm HTTP/1.1 200 300

pos = 0     # 记录每次调用后的指针位置 776628

def create_file():
    global pos
    pos = 0

def is_empty(path):
    #  没有日志tomcat就不会生成文件
    date = time.strftime("%Y-%m-%d", time.localtime())
    dir_filename = 'localhost_access_log.{}.txt'.format(date)
    cmd = 'find {} -name "{}"'.format(path,dir_filename)
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result_str = res.stdout.read().decode(encoding='utf-8').strip()
    return result_str

def initialization(filename):   # 每次启动脚本，预先知道要监测的文件，记录光标位置
    global pos
    with open(filename,'rb') as f:
        pos = len(f.read())

def seek_access(filename):
    global pos
    try:
        con = open(filename, 'rb')  # 无论哪种模式，都是以bytes为单位移动
        # if pos != 0:
        #     # print(pos)
        #     con.seek(pos, 0)  # 1行的末尾即2行的开头       # 移动指针位置   # 0代表从头开始，1代表当前位置，2代表文件最末尾
        # else:          # 启动监测，记录最初的文件指针
            # pos = len(con.read())  # b'1\r\n2\r\n3\r\n4\r\n5\r\n'   15
            # print(pos)
            # print()
            # con.close()
            # return pos
        # print(pos)
        con.seek(pos, 0)


        while True:
            line = con.readline()    # 读取一行内容,光标移动到第二行首部
            # print(line)
            # line = line.replace('\n','')
            if line:
                pos = pos + len(line)   # bytes
                result_str = line.decode(encoding='utf-8')
                # print(result_str)
                ip = result_str.split()[0]  # '114.83.177.174'
                path1 = result_str.split()[6]  # '/account/loadWarningInfo.htm' '/'
                path2 = path1.split('/')[1]  # 'account'
                path3 = '/' + path2  # '/account'

                if path3 in ['/ecms', '/tph', '/tyd', '/zjj', '/test', '/fj']:
                    # 合法则调用白名单接口
                    # http://192.168.1.240:8001/add_ip/?ip=192.168.1.240
                    res = requests.get('http://192.168.1.240:8001/add_ip/?ip={}'.format(ip))
                    # requests.post('http://192.168.1.240:8001/add_ip/?ip={}'.format(ip))
                    print(result_str,end='')
                    # print(res.status_code)
                    print(res.json()) # dict
                    print()
                    # print(res.text)   # str
                else:
                    print('{} Path mismatch'.format(path3))

            else:  # 新增内容读取处理完毕，指针后为空
                break
        con.close()
    except Exception as e:
        con.close()
        print(str(e))


def FSMonitor(path):

    result_str = is_empty(path)
    if result_str:
        initialization(result_str)
        # watch manager
        wm = WatchManager()
        mask = IN_CREATE | IN_MODIFY
        # mask = IN_MODIFY

        # event handler
        handler = EventHandler()

        # notifier
        notifier = Notifier(wm, handler)

        # wm.add_watch(path, mask, auto_add=True, rec=True)
        wm.add_watch(path, mask, rec=True)

        notifier.loop()
    else:
        # watch manager
        wm = WatchManager()
        mask = IN_CREATE | IN_MODIFY
        # mask = IN_MODIFY

        # event handler
        handler = EventHandler()

        # notifier
        notifier = Notifier(wm, handler)

        # wm.add_watch(path, mask, auto_add=True, rec=True)
        wm.add_watch(path, mask, rec=True)

        notifier.loop()


if __name__ == "__main__":
    # FSMonitor('/home/xjj/pyinotify/localhost_v6.txt')
    # /home/program/apache-tomcat-8.5.32/logs
    # localhost_access_log.2019-07-30.txt
    FSMonitor('/home/program/apache-tomcat-8.5.32/logs')