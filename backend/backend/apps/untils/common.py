import os
import logging
import time
import pymongo
from random import choice
MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]
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
    file_name = "{}_爬虫程序_{}.log".format(real_path,
                                             time.strftime("%Y-%m-%d",
                                                           time.localtime()))
    log = logger(file_name)
    return log


def ABY():
    try:
        IP = STATIC_IP.find()

        ip_lt = choice([_ for _ in IP])
        ip = ip_lt["ip_parmas"]
        _id = ip_lt["_id"]
        proxies = {
            "http": "http://" + ip,
            "https": "https://" + ip,
        }
        return proxies,_id

    except Exception as e:
        print(e)
        return None

