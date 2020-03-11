#encoding=utf-8
import redis
import pymongo


red_cli = redis.Redis(host='127.0.0.1',port=6379,db=15)
DB = pymongo.MongoClient(host="172.16.74.249",port=27017)

db = DB["BMD"]["Reserve_total"]

result = db.find().limit(10000).skip(0)

count = 0
for _ in result:
    item = {}
    item["_id"] = _["_id"]
    item["company"] = _["companyName"]
    red_cli.sadd("directories",str(item))
    count += 1
    print(f"第{count}条名录数据存入redis成功，等待抓取")
