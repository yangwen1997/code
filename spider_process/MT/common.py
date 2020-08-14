import pymongo

from random import choice

# 静态IP数据库
MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

# 美团数据库
# SPIDERDB = pymongo.MongoClient(host='172.16.74.249',port=27017)
SPIDERDB = pymongo.MongoClient(host='172.16.75.28',port=27017)
poiIdDB =  SPIDERDB["MTDB"]["PCPId"]
PC_DATA_info =  SPIDERDB["MTDB"]["PC_DATA_info"]



def ABY():
    """随机返回代理IP"""
    try:
        # IP = STATIC_IP.find({"flag":"1"})
        IP = STATIC_IP.find().limit(9).skip(10)
        # IP = STATIC_IP.find().limit(19)

        ip = choice([_ for _ in IP])

        proxies = {
            "http": "http://" + ip["ip_parmas"],
            "https": "https://" + ip["ip_parmas"],
        }
        return proxies,ip
    except Exception as e:
        print(e)
        return None


import os
import logging
import time
def logger(FILE_NAME):
    """
    日志配置
    :param FILE_NAME: 日志文件名(全路径 )
    :return:日志记录生成器
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y %H:%M:%S',
        filename=FILE_NAME,
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging

def get_log():
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + "/log/"
    file_name = "{}_爬虫程序_{}.log".format(real_path,time.strftime("%Y-%m-%d",time.localtime()))
    log = logger(file_name)
    return log

import requests
import execjs
class mt_spider_base(object):

    def __init__(self):
        self.s = requests.session()
        self.s.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://hotel.meituan.com/shanghai/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        })
        self.IPcount = 0
        self.proxy, self.ipItem = ABY()

    def get_req(self, url, paramas=None):
        """
        get请求封装
        :param url:
        :param paramas:
        :return:
        """

        try:
            if self.IPcount < 3:
                # self.proxy = {'http': 'http://122.6.226.248:2404', 'https': 'https://122.6.226.248:2404'}
                # resp = self.s.get(url=url, params=paramas, proxies=self.proxy,timeout=30)
                resp = self.s.get(url=url)
                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    self.IPcount = 0
                    return resp
                else:
                    self.ipItem["flag"] = "0"
                    STATIC_IP.save(self.ipItem)
                    self.IPcount += 1
                    self.proxy, self.ipItem = ABY()
                    self.get_req(url, paramas)
            else:
                self.IPcount = 0
                print("超过3次请求失败")
                return None
        except requests.exceptions.InvalidSchema as e:
            return "InvalidSchema"
        except Exception as e:
            print(e)

    def post_req(self, url, data):
        """
        get请求封装
        :param url:
        :param paramas:
        :return:
        """
        try:
            if self.IPcount < 3:
                resp = self.s.get(url=url, data=data, proxies=self.proxy)
                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    self.IPcount = 0
                    return resp
                else:
                    self.ipItem["flag"] = "0"
                    STATIC_IP.save(self.ipItem)
                    self.IPcount += 1
                    self.proxy, self.ipItem = ABY()
                    self.get_req(url, data)
            else:
                self.IPcount = 0
                print("超过3次请求失败")
                return None
        except Exception as e:
            print(e)

    def get_token(self):
        """获取token"""
        r = r'E:\code\spider\spider_process\MT\rohr.main.js'
        with open(r, "r", encoding="utf-8")as fp:
            js = fp.read()
        etx = execjs.compile(js)
        print(execjs.get().name)
        resp = etx.call("get_token")
        with open(r'token.txt', 'w', encoding='utf-8') as fp:
            fp.write(resp)
        return resp