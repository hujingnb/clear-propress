"""
Created on 2018年4月11日
实现清理后台程序
@author: hujing
"""
import easygui
from ctypes.wintypes import *
from ctypes import *
import collections
import os
from src.config import Config

kernel32 = windll.kernel32


class tagPROCESSENTRY32(Structure):
    _fields_ = [('dwSize', DWORD),
                ('cntUsage', DWORD),
                ('th32ProcessID', DWORD),
                ('th32DefaultHeapID', POINTER(ULONG)),
                ('th32ModuleID', DWORD),
                ('cntThreads', DWORD),
                ('th32ParentProcessID', DWORD),
                ('pcPriClassBase', LONG),
                ('dwFlags', DWORD),
                ('szExeFile', c_char * 260)]


# 获取系统当前进程
def enumProcess():
    hSnapshot = kernel32.CreateToolhelp32Snapshot(15, 0)
    fProcessEntry32 = tagPROCESSENTRY32()
    processClass = collections.namedtuple("processInfo", "processName processID")
    processSet = []
    if hSnapshot:
        fProcessEntry32.dwSize = sizeof(fProcessEntry32)
        listLoop = kernel32.Process32First(hSnapshot, byref(fProcessEntry32))
        while listLoop:
            processName = fProcessEntry32.szExeFile
            processID = fProcessEntry32.th32ProcessID
            processSet.append(processClass(processName, processID))
            listLoop = kernel32.Process32Next(hSnapshot, byref(fProcessEntry32))
    return processSet


if __name__ == '__main__':
    config = Config()
    choices = []
    preselect = []
    count = 0
    # 将列表倒序
    li = enumProcess()
    li.reverse()
    # 遍历进程列表
    for i in li:
        #     print(i.processName,i.processID)
        name = i.processName.decode()
        # 进程简介
        referral = config.getReferral(name)
        # 想列表中添加进程
        choices.append('%s(%d)[%s]' % (name, i.processID, referral if referral != '' else '暂无介绍'))
        if config.ifDefault(name):
            preselect.append(count)
        count += 1
    # 显示选择列表
    result = easygui.multchoicebox(msg='选择要结束的进程,本次选中的进程,下次会默认选中', title='靖哥清除进程', choices=choices, preselect=preselect)
    # 结果中的进程名字集合
    names = []

    try:
        # 遍历选择列表
        for each in result:
            # 取pid
            pid = int(each[each.find('(') + 1: each.find(')')])
            # 取名字
            name = each[:each.find('(')]
            names.append(name)
            # 结束进程
            os.system('tskill %d' % pid)
    # 什么都没选
    except TypeError:
        pass
    # 更新配置文件
    config.updateDefault(names)
