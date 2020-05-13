import pymongo
import csv

mg = pymongo.MongoClient(host="172.16.74.249",port=27017)

STATIC_IP = mg["MTDB"]["PC_DATA_info"]
result = STATIC_IP.find({"city" : "德阳"})
with open(r"E:\code\spider\spider_process\MT\dy.csv", "a", encoding="utf-8")as fp:

    filednames = ['_id', 'title','address','city','phone']
    books = []
    writer = csv.DictWriter(fp, fieldnames=filednames)
    writer.writeheader()
    for _ in result:
        items = {
            "_id" :_["_id"],
            "title" :_["title"],
            "address" :_["address"],
            "city" :_["city"],
            "phone" :_["phone"]
        }
        writer.writerow(items)
