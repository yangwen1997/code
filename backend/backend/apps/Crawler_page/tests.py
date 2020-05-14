from django.test import TestCase

# Create your tests here.

import requests
import json
#
# s = requests.session()
#
# s.headers.update({
#     'User-Agent' :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
# })
# url = 'http://172.16.75.38:8001/crawler/bdxy_basic/'
# # url = 'http://127.0.0.1:8000/crawler/bdxy_basic/'
# # url = 'http://172.16.74.78:5678/add/Baiducompany/'
# # url = 'http://172.16.74.78:1234/add/Tyccompany/'
# data = {
#     # "company_name" : "aaa",
#     "ApiType":"基本信息查询",
#     'company_name': "华为技术有限公司",
# }
# resp = s.post(url,data=data)
# resp.encoding = 'utf-8'
# print(resp.text)
# # {"err_msg":"未找到符合条件的查询结果，请更改关键词重新查询"}
import pymysql
import json
conn = pymysql.Connect(host='172.16.75.38',port=3306,user='yang',password='dgg102888',database='db_manage')
cursor  = conn.cursor()






data = {
    "info":[
        {"field":"company_name","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"公司名"},
        {"field":"case_num","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"案号"},
        {"field":"case_judge","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"承办法官"},
        {"field":"case_helper","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"法官助理"},
        {"field":"case_time","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"立案时间"},
        {"field":"case_open","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"开庭时间"},
        {"field":"case_end_time","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"结束时间"},
        {"field":"case_status","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"案件状态"},
        {"field":"case_plaintiff","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"原告"},
        {"field":"case_defendant","dataType":"varchar(255)","fieldType":"varchar","length":"255","notes":"原告"},
        {"field":"update_time","dataType":"datetime","fieldType":"datetime","length":"","notes":"写入mysql时间"},

    ]
}

titles = "企业基本信息表"
tit = "立案信息表"
tables = "company_case_info"

sql = 'INSERT INTO db_info(title, ch_table, en_table, dates) VALUES("{}","{}","{}","{}")'.format(titles,tit,tables,str(data))
# sql = 'select * from db_info'
cursor.execute(sql)
# results = cursor.fetchall()
# a = json.dumps(results[0][3])
# print(a)
# print(type(a))

conn.commit()
conn.close()
