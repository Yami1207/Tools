# -*- coding: UTF-8 -*-
import os
import struct
import ctypes
import xlrd
from Utility import *

class DataProperty(object):
    def __init__(self):
        self.name = ''
        self.info = ''
        self.index = -1
        self.isKey = False
        self.isDel = False
        self.type = DATA_PROPERTY_TYPE_UNKNOWN

class DataSheet(object):
    def __init__(self, sheet):
        self.isValid = False
        self.keyIndex = -1
        self.propertyList = []

        # 少于5行或2列可退出
        if sheet.nrows < 5 or sheet.ncols < 2:
            return
        if sheet.row_values(0)[0].lower() != 'define' or sheet.row_values(1)[0].lower() != 'info':
            return
        if sheet.row_values(2)[0].lower() != 'type' or sheet.row_values(3)[0].lower() != 'name':
            return
        
        for i in range(1, sheet.ncols):
            dataProperty = DataProperty()

            defineField = sheet.row_values(0)[i].lower()
            if defineField == 'key' and self.keyIndex == -1:
                self.keyIndex = len(self.propertyList)
                dataProperty.isKey = True
            if defineField == 'del':
                dataProperty.isDel = True
            
            # 类型
            typeField = sheet.row_values(2)[i].lower()
            if typeField == 'int':
                dataProperty.type = DATA_PROPERTY_TYPE_INT
            elif typeField == 'string':
                dataProperty.type = DATA_PROPERTY_TYPE_STRING
            elif typeField == 'float':
                dataProperty.type = DATA_PROPERTY_TYPE_FLOAT
            elif typeField == 'bool':
                dataProperty.type = DATA_PROPERTY_TYPE_BOOL
            
            dataProperty.name = sheet.row_values(3)[i]
            dataProperty.info = sheet.row_values(1)[i]
            dataProperty.index = i

            self.propertyList.append(dataProperty)
        
        if self.keyIndex != -1:
            self.isValid = True
    
    def IsValid(self):
        return self.isValid
    
    def ExportCSV(self, path, filename, sheet):
        file = OpenFile('{0}/{1}.csv'.format(path, filename), 'w')
        
        for i in range(4, sheet.nrows):
            line = ''
            for dataProperty in self.propertyList:
                if dataProperty.isDel or dataProperty.type == DATA_PROPERTY_TYPE_UNKNOWN:
                    continue

                if line != '':
                    line = line + ','
                
                # 获取类型与数值
                ctype = sheet.cell(i , dataProperty.index).ctype
                value = sheet.cell_value(i, dataProperty.index)
                if ctype == 2 and value % 1 == 0:
                    value = int(value)

                # 写入数据
                if dataProperty.type == DATA_PROPERTY_TYPE_INT or dataProperty.type == DATA_PROPERTY_TYPE_FLOAT or dataProperty.type == DATA_PROPERTY_TYPE_BOOL:
                    line = line + '{0}'.format(str(value))
                elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
                    line = line + '"{0}"'.format(value)
            
            # 换行
            line = line + '\n'
            file.write(line)
        
        # 关闭文件
        file.close()
    
    def ExportData(self, path, filename, sheet):
        file = OpenFile('{0}/{1}.bytes'.format(path, filename), 'wb', '')

        # 写入行列数
        rowsCount = sheet.nrows - 4
        file.write(struct.pack('i', rowsCount))
        columnsCount = len(self.propertyList)
        file.write(struct.pack('i', columnsCount))

        # 写入每行字段属性
        for i in range(columnsCount):
            prop = self.propertyList[i]

            # 类型
            propType = prop.type
            if prop.isDel:
                propType = DATA_PROPERTY_TYPE_UNKNOWN
            file.write(struct.pack('b', propType))

        for i in range(4, sheet.nrows):
            # 写入key值
            self._WriteKeyData(file, self.propertyList[self.keyIndex], sheet, i)

            # 统计需要分配内存大小
            bytesSize = 0
            for dataProperty in self.propertyList:
                if dataProperty.isDel or dataProperty.type == DATA_PROPERTY_TYPE_UNKNOWN:
                    continue
                
                if dataProperty.type == DATA_PROPERTY_TYPE_BOOL:
                    bytesSize += 1
                elif dataProperty.type == DATA_PROPERTY_TYPE_INT or dataProperty.type == DATA_PROPERTY_TYPE_FLOAT:
                    bytesSize += 4
                elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
                    value = sheet.cell_value(i, dataProperty.index)
                    value = '{0}'.format(value)
                    bytesSize += 4 + len(value)
            
            dataBytes = ctypes.create_string_buffer(bytesSize)
            index = 0
            for dataProperty in self.propertyList:
                if dataProperty.isDel or dataProperty.type == DATA_PROPERTY_TYPE_UNKNOWN:
                    continue
                
                value = sheet.cell_value(i, dataProperty.index)
                if dataProperty.type == DATA_PROPERTY_TYPE_BOOL:
                    struct.pack_into('b', dataBytes, index, bool(value))
                    index += 1
                elif dataProperty.type == DATA_PROPERTY_TYPE_INT:
                    struct.pack_into('i', dataBytes, index, self._GetIntValue(value))
                    index += 4
                elif dataProperty.type == DATA_PROPERTY_TYPE_FLOAT:
                    struct.pack_into('i', dataBytes, index, float(value))
                    index += 4
                elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
                    value = '{0}'.format(value)
                    size = len(value)
                    struct.pack_into('i{0}s'.format(size), dataBytes, index, size, value.encode('UTF-8'))
                    index += 4 + size
            
            file.write(struct.pack('i', bytesSize)) 
            file.write(dataBytes)
        
        # 关闭文件
        file.close()
    
    def _WriteKeyData(self, file, dataProperty, sheet, index):
        bytesSize = 0
        if dataProperty.type == DATA_PROPERTY_TYPE_INT or dataProperty.type == DATA_PROPERTY_TYPE_FLOAT:
            bytesSize = 4
        elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
            value = '{0}'.format(value)
            value = sheet.cell_value(index, dataProperty.index)
            bytesSize = len(value)
        
        dataBytes = ctypes.create_string_buffer(bytesSize + 4)
        key = sheet.cell_value(index, dataProperty.index)
        if dataProperty.type == DATA_PROPERTY_TYPE_BOOL:
            struct.pack_into('ib', dataBytes, 0, 1, bool(key))
        elif dataProperty.type == DATA_PROPERTY_TYPE_INT:
            struct.pack_into('ii', dataBytes, 0, 4, self._GetIntValue(key))
        elif dataProperty.type == DATA_PROPERTY_TYPE_FLOAT:
            struct.pack_into('if', dataBytes, 0, 4, float(key))
        elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
            key = '{0}'.format(key)
            size = len(key)
            struct.pack_into('i{0}s'.format(size), dataBytes, 0, 4, size, key.encode('UTF-8'))
        
        file.write(dataBytes)
    
    def _GetIntValue(self, value):
        if len('{0}'.format(value)) == 0:
            return 0
        return int(value)
