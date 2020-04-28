import requests
import execjs
import uuid
import os
import json
import hashlib
import re
import redis
from lxml.etree import HTML

from common import ABY,STATIC_IP,poiIdDB,PC_DATA_info




red_cli = redis.Redis(host="172.16.75.38",port=6379,db=15)

class MTPC(object):

    def __init__(self,cateId=None,category=None,page=None):
        """初始化
        :param cateId   ：美食分类ID
        :param category ：数据库存入的类别
        :param page     ：页码
        """
        self.page = page
        self.data = {
            "cityName": "上海",
            "cateId": cateId,
            "areaId": "0",
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
            "_token":'eJx1T1tvmzAU/i9+BcUmFwN584AEnIQQBpRR7YHEpCaBUDAJLdX++1yte5k06Ujf7ejTOR+g8xhYagiZCKngUXRgCbQJmmCggl7IZGHopo6RMVvMTRWc/vEWWAXHLrHB8lkzp0id6ejnpxNK41lDhlR/Ag3NJZ/O5XwueDIHvO9fxRJCwSd1Ufb3/DY5NTWUXPASygP+swBkQx3JBonXL8y/sP+rd/IRWSHKl5tkBR2qy3W9Hy5kFxbQ8oRAh/DQxDz3Vow2jI8kpiz3nVu1twJfy8ghVEiTklWX1Tt4TmdQH+Jh6JxgrN6I8c30zp3Bf9xeoIsV3e796Lso3ZQGIkw4o8K0RJbZ+mU1z8ZtVLENfR2tzbhOU3/9hJz42lL3QUXi3L0xqXkrCrzehu97K81HP/CcoG5tGt3TGbeRvqHHnRMPD8VkyUapxHaquKeuJWetvJOIFVjAtE9ad3w3Fhjjt+OZEPGEGgZ+/QZj9pIz',
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
        return resp

    def get_poiid_list(self):
        """美团美食列表页码POIiD抓取程序"""
        self.data[0]["page"] = str(self.page)
        self.s.headers.update({
            "Accept": "application/json",
            "Referer": "https://sh.meituan.com/meishi/"
        })
        url = "https://sh.meituan.com/meishi/api/poi/getPoiList"
        resp = self.get_req(url=url,paramas=self.data[0])
        print(resp.text)

        try:
            res = json.loads(resp.text)["data"]["poiInfos"]
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
            print("结果获取异常，不是json数据,更换token")
            self.get_poiid_list()

    def to_redis(self):
        """抓取的破poiiD数据存入redis"""
        pass

    def get_shop_info(self):
        """美食获取店铺详情信息"""
        red_count = red_cli.scard("PCPId")

        while red_count:
            try:
                red_data = red_cli.srandmember("PCPId")
                poid_data = eval(red_data)
                url = f"https://www.meituan.com/meishi/{str(poid_data['poiId'])}/"
                self.s.headers.update({
                    "Accept": "*",
                })
                resp = self.get_req(url)
                # etre = HTML(resp.text)
                if resp:
                    resp_phne = "".join(re.findall(r',"phone":"(.*?)","openTime"',resp.text))

                    if resp_phne:
                        phonelt = resp_phne.split("/")
                        item = {}
                        item["title"] = poid_data["title"]
                        item["address"] = poid_data["address"]
                        item["avgScore"] = poid_data["avgScore"]
                        item["city"] = "上海"
                        item["category"] = "美食"
                        item["flag"] = "1"
                        for _ in phonelt:
                            item["_id"] = hashlib.md5(str(_).encode("utf-8")).hexdigest()
                            item["phone"] = str(_)
                            PC_DATA_info.save(item)
                            print(f"手机号为-{str(_)}的店铺数据存入数据库成功。。。")
                        red_count -= 1
                        red_cli.srem("PCPId",red_data)
                    else:
                        if "按省份选择" in resp.text:
                            red_cli.srem("PCPId", red_data)
                            red_count -= 1
                        elif "验证中心" in resp.text:
                            self.ipItem["flag"] = "0"
                            STATIC_IP.save(self.ipItem)
                            self.proxy, self.ipItem = ABY()

                        else:
                           lt = re.findall(r'"address":"(.*?)","phone":"(.*?)"',resp.text)
                           if lt[0]:

                                red_cli.srem("PCPId", red_data)
                                red_count -= 1
                                print("该数据没有号码")
            except Exception as e:
                pass





start = MTPC(cateId="0",category="美食",page=1)

start.get_shop_info()

# a = "伊洛斋"
# b = "184838581"
# c = b + a
# e = "2978614092d275a62efa025358219107"
# d= hashlib.md5(c.encode("utf-8")).hexdigest()
# if d == e:
#     print("sucess")