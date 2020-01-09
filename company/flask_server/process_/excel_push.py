"""
python操作excel主要用到xlrd和xlwt这两个库，即xlrd是读excel，xlwt是写excel的库。
可从这里下载https://pypi.python.org/pypi。下面分别记录python读和写excel.
"""
import xlrd, xlwt, hashlib
import re
import os
from datetime import date, datetime
import json
from flask_server.common import Spider_table,qcc_new,com_reserve
from flask import current_app

def read_excel(user_id,trade):
    """

    :param user_id: 工号
    :param trade: 液态
    :return:
    """

    from company.manage import app
    # 打开文件
    files = r'D:\bmd\bmd_server\src\company\flask_server\files\{}'.format(user_id)
    file_lt = os.listdir(files)

    # sheet的名称，行数，列数
    # print
    # sheet.name, sheet.nrows, sheet.ncols
    # 获取整行和整列的值（数组）
    m = 0
    n = 0
    s = 0
    lt = []
    for file in file_lt:
        if file == "TEL":
            pass
        else:
            file_path = files + r'\{}'.format(file)
            workbook = xlrd.open_workbook(file_path)
            mark = str(trade)
            # 获取所有sheet
            sheet_name = workbook.sheet_names()[0]
            # 根据sheet索引或者名称获取sheet内容
            sheet = workbook.sheet_by_index(0)  # sheet索引从0开始

            a = 1
            while True:
                try:
                    rows = sheet.row_values(a)
                    # print(rows)
                except Exception as e:
                    print(e)
                    break
                else:
                    if len(rows) == 0:
                        break
                    else:
                        companyName = rows[0]
                        businessState = rows[1]
                        legalMan = rows[2]
                        registerMoney = rows[3]
                        reg_time = rows[4]
                        if type(rows[4]) == str:
                            registerTime = rows[4]
                        else:
                            registerTime == str(datetime.datetime(*xlrd.xldate_as_tuple(rows[4], 0))).replace(' 00:00:00', '')
                        companyProvince = rows[5]
                        companyCity = rows[6]
                        companyTel = str(rows[7]).replace(".0","")
                        imTel = rows[8]
                        email = rows[9]
                        tynum = str(rows[10]).replace(".0","")
                        nsnum = str(rows[11]).replace(".0", "")
                        zch = str(rows[12]).replace(".0", "")
                        zznum = str(rows[13]).replace(".0", "")
                        cbrs = rows[14]
                        companyType = rows[15]
                        industry = rows[16]
                        web = rows[17]
                        registerAddress = rows[18]
                        businessScope = rows[19]

                        id = hashlib.md5(companyName.encode(encoding='utf-8')).hexdigest()

                        data = {
                            '_id': id,
                            'companyName': companyName,
                            'businessState': businessState,
                            'legalMan': legalMan,
                            'registerMoney': registerMoney,
                            'registerTime': registerTime,
                            'companyProvince': companyProvince,
                            'companyCity': companyCity,
                            'companyTel': companyTel,
                            'imTel': imTel,
                            'email': email,
                            'tynum': tynum,
                            'nsnum': nsnum,
                            'zch': zch,
                            'zznum': zznum,
                            'cbrs': cbrs,
                            'companyType': companyType,
                            'industry': industry,
                            'web': web,
                            'registerAddress': registerAddress,
                            'businessScope': businessScope,
                            'mark': mark
                        }
                        try:
                            # 存入成功的数据 data
                            Spider_table.insert(data)
                            m += 1
                            s += 1
                            a += 1
                            lt.append(data)
                        except :
                            # 失败的数据 data
                            s += 1
                            n += 1
                            a += 1

    for file in file_lt:
        if file != "TEL":
            file_path = files + r'\{}'.format(file)
            os.remove(file_path)

    # a: 总数， m：插入成功 n:失败
    current_app.logger.info(f'合计：上传数据总数{s}, 新上传数据m:{m}, 已有数据n:{n}')

    return s,m,n,lt


def tel_handler(data):
    """
    对公司的手机号去重存入数据库
    :return:
    """
    sucuess_count = 0
    # result = Spider_table.find({'flag':{"$exists":False}})
    result = data
    for i in result:
        old_id = i['_id']
        tel = []
        companyTel = i['companyTel']
        if companyTel.isdigit() and len(companyTel) == 11 and companyTel[0] == '1':
                tel.append(companyTel)
        imTel = i['imTel']
        if len(imTel):
            for j in imTel.split('；'):
                if j.isdigit() and len(j) == 11 and j[0] == '1':
                    tel.append(j)
        for k in tel:
            _id = hashlib.md5(k.encode(encoding='utf-8')).hexdigest()
            companyName = i['companyName']
            businessState = i['businessState']
            legalMan = i['legalMan']
            registerMoney = i['registerMoney']
            registerTime = i['registerTime']
            companyProvince = i['companyProvince']
            companyCity = i['companyCity']
            registerAddress = i['registerAddress']
            businessScope = i['businessScope']
            mark = i['mark']
            industry = i['industry']
            companyType = i['companyType']
            web = i['web']

            data = {
                "_id": _id,
                "companyName": companyName,
                "companyTel": k,
                "businessState": businessState,
                "legalMan": legalMan,
                "registerMoney": registerMoney,
                "registerTime": registerTime,
                "companyProvince": companyProvince,
                "registerAddress": registerAddress,
                "businessScope": businessScope,
                "companyCity": companyCity,
                "industry": industry,
                "companyType": companyType,
                "web": web,
                "mark": mark,
            }

            try:
                com_reserve.insert(data)
                sucuess_count += 1
                print(data)
            except Exception as e:

                print(e)


        Spider_table.find_one_and_update({"_id": old_id}, {"$set": {"flag": 1}})

    return sucuess_count

if __name__ == '__main__':
    read_excel(user_id="102888",trade="a")
