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
        IP = STATIC_IP.find()

        ip = choice([_ for _ in IP])

        proxies = {
            "http": "http://" + ip["ip_parmas"],
            "https": "https://" + ip["ip_parmas"],
        }
        return proxies,ip
    except Exception as e:
        print(e)
        return None
