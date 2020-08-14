import pymongo

from random import choice

# 静态IP数据库
MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

# 美团数据库
SPIDERDB = pymongo.MongoClient(host='172.16.74.249',port=27017)
poiIdDB =  SPIDERDB["MTDB"]["PCPId"]
PC_DATA_info =  SPIDERDB["MTDB"]["PC_DATA_info"]



def ABY():
    """随机返回代理IP"""
    try:
        IP = STATIC_IP.find({}).limit(9).skip(10)
        # IP = STATIC_IP.find({"flag":"1"})

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