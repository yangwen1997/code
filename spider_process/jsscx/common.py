
import pymongo
import requests
from random import choice

MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
DB = pymongo.MongoClient(host='172.16.75.28',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

# 建设库的数据库地址
JSK_url = DB["YANG"]["JSK_url"]
JSK_date = DB["YANG"]["JSK_date"]

# 555建筑网的数据库地址
JZW555_category = DB["YANG"]["JZW555_category"]
JZW555_url = DB["YANG"]["JZW555_url"]
JZW555_date = DB["YANG"]["JZW555_date"]

#数据地区补充更新库
area_category = DB["YANG"]["areaCategory"]
areaCategory = DB["YANG"]["area_category"]
areaTest = DB["YANG"]["test"]

def ABY():
    """随机返回代理IP"""
    try:
        # IP = STATIC_IP.find({"flag":"1"})
        # IP = STATIC_IP.find().limit(9).skip(10)
        IP = STATIC_IP.find().limit(19)

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


class REQ(object):

    def __init__(self):
        pass

    def get_proxy(self):
        """
        请求代理IP
        :return:
        """
        self.ipItem["flag"] = "0"
        STATIC_IP.save(self.ipItem)
        self.proxy, self.ipItem = ABY()

    def get_req(self,url):
        """
        get请求封装，超过3次停止请求，自动更新替换IP
        :param url:
        :return:
        """
        try:
            if self.IPcount < 3:
                resp = self.s.get(url=url,proxies=self.proxy,timeout=30)
                # resp = self.s.get(url=url,timeout=30)

                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    return resp
                else:
                    self.get_proxy()
                    self.IPcount += 1
                    self.log.info("页面状态码错误，更换IP")
            else:
                self.log.info("请求超过3次出错停止请求")
                self.get_proxy()
                self.IPcount = 0
                return None
        except Exception as e:
            self.get_proxy()
            self.IPcount += 1
            self.log.info("超时出错")