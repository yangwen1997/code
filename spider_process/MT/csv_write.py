import pymongo
DB= pymongo.MongoClient(host='172.16.75.28',port=27017)
# PC_DATA_info = DB["YANG"]["JSK_date"]
PC_DATA_info = DB["YANG"]["JZW555_date"]

# DB= pymongo.MongoClient(host='172.16.74.249',port=27017)
# PC_DATA_info = DB["BMD"]["Reserve_total_1"]
result = PC_DATA_info.find()
import csv



header= ["姓名","行业","电话","地区","发布时间"]

path = 'E:\code\spider\spider_process\MT\cd.csv'
with open(path,'a',newline='',encoding='utf-8') as fp:
    f_csv = csv.DictWriter(fp, header)
    row = []

    for _ in result:
        item = {}
        try:
            item["姓名"] = _["zj_Name"]
        except:
            item["姓名"] = ""
        try:
            item["行业"] = _["information_classification"]
        except :
            item["行业"] = ""
        try:
            item["电话"] = _["phone"]
        except :
            item["电话"] = ""
        try:
            item["地区"] = _["certificate_location"]
        except :
            item["地区"] = ""
        try:
            item["发布时间"] = _["updateTime"]
        except :
            item["发布时间"] = ""

        row.append(item)
    f_csv.writeheader()
    f_csv.writerows(row)