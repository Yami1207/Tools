# -*- coding: UTF-8 -*-
import os

VERSION = '1.00'

# 数据类型
DATA_PROPERTY_TYPE_UNKNOWN = 0
DATA_PROPERTY_TYPE_BYTE = 1
DATA_PROPERTY_TYPE_SHORT = 2
DATA_PROPERTY_TYPE_INT = 3
DATA_PROPERTY_TYPE_FLOAT = 4
DATA_PROPERTY_TYPE_BOOL = 5
DATA_PROPERTY_TYPE_STRING = 6
DATA_PROPERTY_TYPE_ULONG = 7

# 创建目录
def MakeDir(dir):
    if dir == '.' or dir == '..':
        return
    
    pos = dir.rfind('/')
    if pos != -1:
        MakeDir(dir[0 : pos])

    if not os.path.exists(dir):
        os.mkdir(dir)

# 打开文件
def OpenFile(filename, mode, encode = 'UTF-8'):
    pos = filename.rfind('/')
    if pos != -1:
        MakeDir(filename[0 : pos])

    if encode == '':
        return open(filename, mode)
    return open(filename, mode, encoding = encode)
