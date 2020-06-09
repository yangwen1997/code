# -*- coding: utf-8 -*-
"""
@author: lywen
后台通过接口调用服务，获取OCR识别结果
"""
import base64
import requests
import json
import time
import hashlib
import pymongo

client = pymongo.MongoClient("mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017, 10.2.1.217:57017, 10.2.1.218:57017")
col = client['BMD']['LT_ocr']


def read_img_base64(p):
    with open(p, 'rb') as f:
        imgString = base64.b64encode(f.read())
    imgString = b'data:image/jpeg;base64,' + imgString
    return imgString.decode()


def post(p, billModel='通用OCR'):
    URL = 'http://127.0.0.1:8080/ocr'  # url地址
    imgString = read_img_base64(p)
    headers = {}
    param = {'billModel': billModel,  # 目前支持三种 通用OCR/ 火车票/ 身份证/
             'imgString': imgString,
             'textAngle': True
             }
    param = json.dumps(param)
    if 1:
        req = requests.post(URL, data=param, headers=None, timeout=50)
        data = req.content.decode('utf-8')
        data = json.loads(data)
    else:
        data = None
    # print(data)
    if data:
        for k in range(len(data['res'])):
            str_1 = data['res'][k]['text']
            tel = str(str_1[0:11])
            if tel.isdigit():
                name = str_1[12:]
                mimi = {
                    "_id": hashlib.md5(tel.encode(encoding='utf-8')).hexdigest(),
                    "tel": tel,
                    "name": name
                }
                col.save(mimi)
                print(mimi)


if __name__ == '__main__':
    # p = './test/idcard-demo.jpeg'
    # post(p,'身份证')
    start_time = time.time()
    # p = "./test/mingpian2.png"
    p = r"D:\图片\123.png"
    post(p, "通用OCR")
    print("花费时间：", time.time() - start_time)
