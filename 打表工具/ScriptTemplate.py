# -*- coding: UTF-8 -*-
import re
import sys
import os

from Utility import *
from string import Template
from DataSheet import DataSheet

class ScriptTemplate(object):
    def __init__(self):
        self.isValid = False

        filename = "./Res/template"

        self.templates = {}
        self.templates['cs'] = self.LoadTemplateCS(filename)
        self.isValid = True

    def IsValid(self):
        return self.isValid

    def LoadTemplateCS(self, filename):
        filename = filename + ".cs"

        # 判断模板文件是否存在
        if not os.path.exists(filename):
            print("模板文件({0})不存在".format(filename))
            return None
        
        # 读取模板
        fileStream = open(filename, encoding='utf-8')
        strngBuffer = fileStream.read()
        fileStream.close()

        classDefine = {}
        classDefine['script'] = self.ReadField('[Script]', strngBuffer)
        classDefine['baseProperty'] = self.ReadField('[BaseProperty]', strngBuffer)
        classDefine['readBaseProperty'] = self.ReadField('[ReadBaseProperty]', strngBuffer)
        return classDefine
    
    def GenerateScripts(self, path, filename, dataSheet):
        self.GenerateCS(path, filename, dataSheet)

    def GenerateCS(self, path, filename, dataSheet):
        classDefine = self.templates['cs']
        if classDefine == None:
            return

        script = classDefine['script']
        if script == None:
            return
        
        def _GetKeyType(propertyList, index):
            result, type = 'int', propertyList[index].type
            if type == DATA_PROPERTY_TYPE_STRING:
                result = 'string'
            return result

        def _GetDefineField(propertyList):
            result = ''
            bpt = Template(classDefine['baseProperty'])
            for dataProperty in dataSheet.propertyList:
                result += '\n'

                fieldTemplate, type = None, ''
                if dataProperty.type == DATA_PROPERTY_TYPE_INT:
                    fieldTemplate, type = bpt, 'int'
                elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
                    fieldTemplate, type = bpt, 'string'
                elif dataProperty.type == DATA_PROPERTY_TYPE_BOOL:
                    fieldTemplate, type = bpt, 'bool'
                
                if fieldTemplate != None:
                    result += fieldTemplate.substitute(destribe=dataProperty.info, attrtype=type, attrname=dataProperty.name)

            return result
        
        def _GetReadField(propertyList):
            result = ''
            rbpt = Template(classDefine['readBaseProperty'])

            for dataProperty in dataSheet.propertyList:
                fieldTemplate, type = None, ''
                if dataProperty.type == DATA_PROPERTY_TYPE_INT:
                    fieldTemplate, type = rbpt, 'ToInt32'
                elif dataProperty.type == DATA_PROPERTY_TYPE_STRING:
                    fieldTemplate, type = rbpt, 'String'
                elif dataProperty.type == DATA_PROPERTY_TYPE_BOOL:
                    fieldTemplate, type = rbpt, 'ToBoolean'

                if fieldTemplate != None:
                    result = result + fieldTemplate.substitute(attrtype=type, attrname=dataProperty.name)

            return result
        
        keyType = _GetKeyType(dataSheet.propertyList, dataSheet.keyIndex)

        cn = 'CSV{0}'.format(filename)
        file = OpenFile('{0}_cs/{1}.cs'.format(path, cn), 'w')
        defineField = _GetDefineField(dataSheet.propertyList)
        readField = _GetReadField(dataSheet.propertyList)

        scriptTemplate = Template(script)
        script = scriptTemplate.substitute(fileName=filename, className=cn, keyType=keyType, defineField=defineField, readField=readField)

        file.write(script)
        file.close()
    
    # 读取字段
    def ReadField(self, label, buffer):
        # 获取字段头位置
        start = buffer.find(label)
        if start == -1:
            return None
        
        # 获取字段尾位置
        start += len(label)
        end = buffer.find(label, start)
        if end == -1:
            return None
        
        # 返回字段
        linePos = buffer.find('\n', start) + 1
        if linePos < end:
            return buffer[linePos:end]
        return buffer[start:end].rstrip()
