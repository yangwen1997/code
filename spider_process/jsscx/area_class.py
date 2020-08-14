'''
@author yangwenlong
@time   2020/7/20
'''
import hashlib
from jsscx.common import areaCategory,REQ,ABY,get_log,area_category,areaTest
from lxml.etree import HTML
import requests
import cpca
import pymongo

db = pymongo.MongoClient(host='172.16.74.249',port=27017)
Reserve_total_1 = db["BMD"]["Reserve_total_1"]

class Category(REQ):

    def __init__(self):
        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseurl = 'https://shuidi.cn/pc-search?key='
        self.url = "https://www.qcc.com/search?key="


    def datesave(self):
        rest = area_category.find()
        count = 0
        for _ in rest:
            item = _
            id = hashlib.md5(str(count).encode('utf-8')).hexdigest()
            item["_id"] = id
            areaCategory.save(item)
            count += 1
            print(f"{id}更新成功。。。")


    def dateCategory(self):
        while 1:

            data = areaCategory.find_one({"flag":{"$exists":False}})
            if data:

                company = data["t1"]["customer_name"]
                url = self.baseurl + company
                resp = self.get_req(url)
                if resp:
                    etre = HTML(resp.text)
                    addr = "".join(etre.xpath('//div[@class="or_search_list"][1]//div[@class="or_search_row_content"]/div[4]/text()')).replace("\n","").replace("地址：","").strip(" ")

                    if addr:
                        # addr = list(addr)
                        lt = []
                        lt.append(addr)
                        df = cpca.transform(lt)
                        data["province"] = df["省"][0]
                        data["city"] = df["市"][0]
                        data["area"] = df["区"][0]
                        data["address"] = df["地址"][0]
                        data["pageAddress"] = addr
                        data["flag"] = "1"
                        areaCategory.save(data)
                        print(f"{data['_id']}更新完成。。。。。。。")
                    else:
                        if "Shuidi.CheckCodePc().init()" in resp.text:
                            self.get_proxy()
                            print("出现验证码")
                        else:
                            print("数据为搜索到")
                            data["flag"] = "2"
                            areaCategory.save(data)

                else:
                    print("IP失败")

            else:
                break

    def dbfind(self):
        data = areaCategory.find({"flag": {"$exists": False}})
        for _ in data:

            if _:
                company = _["t1"]["customer_name"]
                da = Reserve_total_1.find_one({"companyName":company})

                if da:
                    addr = da["registerAddress"]

                    lt = []
                    lt.append(addr)
                    df = cpca.transform(lt)
                    _["province"] = df["省"][0]
                    _["city"] = df["市"][0]
                    _["area"] = df["区"][0]
                    _["address"] = df["地址"][0]
                    _["pageAddress"] = addr
                    _["flag"] = "1"
                    areaCategory.save(_)
                    print(f"{_['_id']}更新完成。。。。。。。")
                else:
                    print("数据不存在")

    def update_order(self):
        """更新订单信息"""
        result = areaTest.find()

        for _ in result:
            new = _["是否成单"]
            id = _["_id"]
            areaCategory.find_one_and_update({"_id":id},{"$set":{"是否成单":new}})
            print("更新成功。。。。。")


st = Category()
# st.datesave()

import threading
for i in range(1):
    t = threading.Thread(target=st.update_order())
    t.start()
    print("please wait!")