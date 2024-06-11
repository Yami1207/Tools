# -*- coding: UTF-8 -*-
#import sys
import os
import xlrd
import json
from DataSheet import DataSheet

from Utility import *
from ScriptTemplate import *

excelPath = "../excel"
dataPath = '../data'
tablePath = dataPath + '/Table'
csvPath = dataPath + '/CSV'

def main():
    InitConfig()

    # 加载脚本模板
    st = ScriptTemplate()
    if not st.IsValid():
        return

    # 遍历表文件
    fileList = os.listdir(excelPath)
    for i in range(0, len(fileList)):
        workbook = None
        try:
            workbook = xlrd.open_workbook(excelPath+ '/' + fileList[i])
        except:
            print('文件({0})不是excel'.format(fileList[i]))
        
        if workbook == None:
            continue

        # 遍历表格
        sheetnames = workbook.sheet_names()
        for key in sheetnames:
            sheet = workbook.sheet_by_name(key)
            dataSheet = DataSheet(sheet)
            if not dataSheet.IsValid():
                continue

            # 导出csv
            dataSheet.ExportCSV(csvPath, key, sheet)

            # 导出数据
            dataSheet.ExportData(tablePath, key, sheet)

            # 导出脚本
            st.GenerateScripts(tablePath, key, dataSheet)

def DefaultPath():
    global excelPath
    global dataPath
    global tablePath
    global csvPath

    excelPath = "../excel"
    dataPath = '../data'
    tablePath = dataPath + '/Table'
    csvPath = dataPath + '/CSV'

def InitConfig():
    global excelPath
    global dataPath
    global tablePath
    global csvPath

    jsonText = ''
    with open("autoexec.ini", 'r', encoding='utf-8') as file:
        jsonText = file.read()
    
    if len(jsonText) > 0:
        try:
            data = json.loads(jsonText)
            excelPath = data['excel']
            dataPath = data['data']
            tablePath = dataPath + '/Table'
            csvPath = dataPath + '/CSV'
        except:
            DefaultPath()

if __name__ == "__main__":
    main()
