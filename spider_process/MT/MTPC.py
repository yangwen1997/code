import requests
import execjs
import uuid
import os
import json
import hashlib
import re
import redis
import gc
from lxml.etree import HTML

# 多进程 多线程
from multiprocessing.pool import Pool
from concurrent.futures import ThreadPoolExecutor

from common import ABY,STATIC_IP,poiIdDB,PC_DATA_info

red_cli = redis.Redis(host="172.16.75.38",port=6379,db=15)

class MTPC(object):

    def __init__(self,cateId=None,areaId=None,category=None,page=None,cityName=None):
        """初始化
        :param cateId   ：美食分类ID
        :param category ：数据库存入的类别
        :param page     ：页码
        """

        self.page = page
        self.data = {
            "cityName": cityName,
            "cateId": cateId,
            "areaId": areaId,
            "sort": "",
            "dinnerCountAttrId": "",
            "page": str(self.page),
            "userId": "",
            "uuid": uuid.uuid1(),
            "platform": "1",
            "partner": "126",
            "originUrl": "https://sh.meituan.com/meishi/",
            "riskLevel": "1",
            "optimusCode": "10",
            "_token":'',
        },
        self.category = category
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })
        self.proxy,self.ipItem = ABY()
        self.IPcount = 0

    def get_req(self,url,paramas=None):
        """get请求封装"""
        try:
            if self.IPcount < 3:
                resp = self.s.get(url=url,params=paramas,proxies=self.proxy)
                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    self.IPcount = 0
                    return resp
                else:
                    self.ipItem["flag"] = "0"
                    STATIC_IP.save(self.ipItem)
                    self.IPcount += 1
                    self.proxy, self.ipItem = ABY()
                    self.get_req(url,paramas)
            else:
                self.IPcount = 0
                print("超过3次请求失败")
                return None

        except Exception as e:
            print(e)
            self.ipItem["flag"] = "0"
            STATIC_IP.save(self.ipItem)
            self.IPcount += 1
            self.proxy, self.ipItem = ABY()
            self.get_req(url, paramas)

    def get_token(self):
        """获取token"""
        r = r'E:\code\spider\spider_process\MT\rohr.main.js'
        with open(r, "r", encoding="utf-8")as fp:
            js = fp.read()
        etx = execjs.compile(js)
        print(execjs.get().name)
        resp = etx.call("get_token")
        with open(r'token.txt','w',encoding='utf-8') as fp:
            fp.write(resp)
        return resp

    def get_poiid_list(self):
        """美团美食列表页码POIiD抓取程序"""

        while self.page < 68:
            self.data[0]["page"] = str(self.page)
            self.s.headers.update({
                "Accept": "application/json",
                "Referer": f"https://cd.meituan.com/meishi/{self.data[0]['cateId']}"
                # "Referer": f"https://cd.meituan.com/meishi"
            })
            url = "https://cd.meituan.com/meishi/api/poi/getPoiList"
            resp = self.get_req(url=url,paramas=self.data[0])
            if resp:
                # print(resp.text)
                try:
                    res = json.loads(resp.text)["data"]["poiInfos"]
                    print (res)
                    if res == []:
                        break
                    else:
                        for _ in res:
                            item = {}
                            item["_id"] = hashlib.md5((str(_["poiId"]) +_["title"]).encode("utf-8")).hexdigest()
                            item["poiId"] = _["poiId"]
                            item["title"] = _["title"]
                            item["address"] = _["address"]
                            item["avgScore"] = _["avgScore"]
                            item["city"] = self.data[0]["cityName"]
                            item["category"] = self.category
                            item["flag"] = "0"
                            poiIdDB.save(item)
                        print(f"第{self.page}页的列表数据存入mongo成功。。。")
                        self.page += 1
                except:
                    token = self.get_token()
                    print(token)
                    self.data[0]["_token"] = token
                    self.ipItem["flag"] = "0"
                    STATIC_IP.save(self.ipItem)
                    self.IPcount += 1
                    self.proxy, self.ipItem = ABY()
                    print("结果获取异常，不是json数据,更换token")
                    self.get_poiid_list()
                    gc.collect()
            else :
                print("获取页面失败")
                self.ipItem["flag"] = "0"
                STATIC_IP.save(self.ipItem)
                self.IPcount += 1
                self.proxy, self.ipItem = ABY()

    def to_redis(self):
        """抓取的破poiiD数据存入redis"""
        result = poiIdDB.find({"flag":"0","city":"长沙"})
        for _ in result:
            item = _
            red_cli.sadd("PCPId",str(item))
            poiIdDB.find_one_and_update({"_id":item["_id"]},{"$set":{"flag":"1"}})
            print("数据存入redis sucess")

    def get_shop_info(self):
        """美食获取店铺详情信息"""
        red_count = red_cli.scard("PCPId")

        while red_count:
            try:
                red_data = red_cli.srandmember("PCPId")
                poid_data = eval(red_data)
                self.data[0]["cityName"] = eval(red_data)["city"]
                url = f"https://www.meituan.com/meishi/{str(poid_data['poiId'])}/"
                # url = f"https://www.meituan.com/meishi/2449761/"
                self.s.headers.update({
                    "Accept": "*",
                })
                resp = self.get_req(url)
                # etre = HTML(resp.text)
                if resp:
                    resp_phne = "".join(re.findall(r',"phone":"(.*?)","openTime"',resp.text))

                    if resp_phne:
                        phonelt = resp_phne.split("/")
                        item = poid_data
                        item["flag"] = "1"
                        for _ in phonelt:
                            if len(str(_)) > 18:
                                print(str(_))
                                print(f"手机号码过长，删除该数据。。。")
                            else:

                                phone = str(_).replace("\u002F","")
                                item["_id"] = hashlib.md5(phone.encode("utf-8")).hexdigest()
                                item["phone"] = phone
                                PC_DATA_info.save(item)
                                print(f"手机号为-{str(_)}的店铺数据存入数据库成功。。。")
                        red_count -= 1
                        red_cli.srem("PCPId",red_data)
                    else:
                        if "按省份选择" in resp.text:
                            red_cli.srem("PCPId", red_data)
                            red_count -= 1

                        elif "验证中心" in resp.text or "美团导航" in resp.text:
                            self.ipItem["flag"] = "0"
                            STATIC_IP.save(self.ipItem)
                            self.proxy, self.ipItem = ABY()
                        else:
                           lt = re.findall(r'"address":"(.*?)","phone":"(.*?)"',resp.text)
                           if lt == [] or lt[0]:
                               red_cli.srem("PCPId", red_data)
                               red_count -= 1
                               print("该数据没有号码")

            except Exception as e:
                pass

        if red_count > 0:
            self.get_shop_info()



def main():
    areaIdLT = ["9634","13722","13735","13893","14832","16087","16088","16682","16683","16684","27097"]

    for _ in areaIdLT:
        start = MTPC(cateId="0",areaId=_,category="美食",page=1,cityName="成都")
        start.get_poiid_list()
        print(f"第{_}类抓取完毕")

    # start = MTPC(cateId="0", areaId="0", category="美食", page=1,cityName="德阳")
    # start.get_shop_info()

if __name__ == '__main__':

    # 多线程
    executor = ThreadPoolExecutor(max_workers=5)
    for i in range(1):
        executor.submit(main)