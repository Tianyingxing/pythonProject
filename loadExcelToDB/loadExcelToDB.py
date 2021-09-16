#!/usr/bin/env python
#coding:utf-8
"""
  Author:  chen_zj --<>
  Purpose: 
  Created: 09/15/21
"""

import unittest
import pymysql
import os
import pandas as pd
import xlrd
import csv
from sqlalchemy import create_engine




# 配置mysql 相关

host='127.0.0.1'
port=3306
user='root'
passwd='123456'
db = 'test'

mysqlURL = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'%(user,passwd,host,port,db)
print(mysqlURL)


def readExcel(path):
    # excel 文件阅读器
    wb = xlrd.open_workbook(path)
    sheet = wb.sheets()[0]
    nrows = sheet.nrows  # 行数
    ncols = sheet.ncols  # 列数
    
    # 获取标题字段，用于建表
    titlelist = [sheet.cell(0,i).value for i in range(ncols)]
    data = []
    # 第一行是跳过读取，从第二行开始读取数据
    for j in range(1,sheet.nrows):
        one = [sheet.cell(j,i).value for i in range(ncols)]
        data.append(one)
    return [titlelist,data]

def readCSV(path):
    # csv 文件阅读器
    # 尝试使用utf8和gbk进行读取
    try:
        f = open(path,'r',encoding='utf8')
        reader = csv.reader(f)
        titlelist = reader.__next__()
    except:
        f = open(path,'r',encoding='gbk')
        reader = csv.reader(f) 
        titlelist = reader.__next__()
        
    data = []
    for ar in reader:
        data.append(ar)        
        
    return [titlelist,data]



def loadDataToMysql(path):
    '''
    将数据导入到mysql
    params: path 传入文件路径,支持csv和xlsx两类文件
    
    '''
    if not os.path.exists(path):
        raise OSError('文件不存在:%s'%path)
    
    filename = os.path.split(path)[-1]
    tablename = filename.rsplit('.',1)[0]
    print(tablename)
    filetype = filename.rsplit('.',1)[-1]
    titlelist,data = [],[]
    if filetype in ('xlsx'):
        titlelist,data = readExcel(path)
        
    
    if filetype in ('csv'):
        titlelist,data = readCSV(path)
    
    
    if not data:
        print('not read data')
        return 
    
    df = pd.DataFrame(data,columns=titlelist)    
    engine = create_engine(mysqlURL,encoding='utf8')
    df.to_sql(tablename,con=engine,if_exists='replace',index=False)
    print('完成数据导入,数据行数:',len(data))

def main():
    
    #loadDataToMysql('./autohome_price_test1.csv')
    loadDataToMysql('./autohome_price_test2.xlsx')
    pass


if __name__ == '__main__':
    main()