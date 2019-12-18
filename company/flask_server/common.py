import os
import time
import logging
import pymysql
import pymongo
import redis


#个人数据库

#公共表 推送状态查询表 号码状态查询表
# Online_total = DB['BMD']["Online_total"]
# Tel_total = DB['BMD']["Tel_total"]

# redis 缓存库 未检测表数据
# RED_CLI = redis.Redis(host="127.0.0.1",port=6379,db=6)

#log日志
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
    file_name = "{}_白名单推送系统_{}.log".format(real_path,
                                             time.strftime("%Y-%m-%d",
                                                           time.localtime()))
    log = logger(file_name)
    return log



# 本地测试库地址
DBB = pymongo.MongoClient(host="127.0.0.1",port=27017)
# 企业数据库 公司唯一标识表  号码唯一标识表 数据总表
# com_company_md = DB['BMD']["qcc_table"]
# com_phone_md =  DB['BMD']["qcc_new"]
com_reserve = DBB['BMD']["Reserve_total"]


#公共表 推送状态查询表 号码状态查询表 未检测号码表
Online_total = DBB['BMD']["Online_total"]
Tel_total = DBB['BMD']["Tel_total"]

DATA_result = DBB['BMD']["result"]
Spider_table = DBB['BMD']['spider_table']
qcc_new = DBB['BMD']['qcc_new']

# redis 缓存库 未检测表数据
RED_CLI = redis.Redis(host="127.0.0.1",port=6379,db=6)
