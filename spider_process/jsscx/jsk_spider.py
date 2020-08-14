'''
author yangwenlong
time 2020/7/13
'''

import pymongo
import redis
import hashlib
import requests
from random import choice
from lxml.etree import HTML
from jsscx.common import ABY,get_log

MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
DB = pymongo.MongoClient(host='172.16.75.28',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

JSK_url = DB["YANG"]["JSK_url"]
JSK_date = DB["YANG"]["JSK_date"]

red_cli = redis.Redis(host="172.16.75.38",port=6379,db=14)




class JS_spider(object):

    def __init__(self):

        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()

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

    def xpath_ltpage(self,resp):
        etre = HTML(resp)
        div_lt = etre.xpath('//div[@class="jsz_list clearfix"]')

        for _ in div_lt:
            item = {}
            item["name"] = "".join(_.xpath('.//h3/a/text()'))
            item["date_info_url"] = "".join(_.xpath('.//h3/a/@href'))
            item["_id"] = hashlib.md5(( item["date_info_url"]).encode('utf-8')).hexdigest()
            item["userID"] = "".join(_.xpath('.//span[contains(text(),"身份证号码")]/following-sibling::span//text()'))
            item["reg_category"] = "".join(_.xpath('.//span[contains(text(),"注册类别")]/following-sibling::span//text()'))
            item["reg_major"] =  "".join(_.xpath('.//span[contains(text(),"注册专业")]/following-sibling::span//text()'))
            item["practice_seal"] =  "".join(_.xpath('.//span[contains(text(),"执业印章号")]/following-sibling::span//text()'))
            item["validity_time"] =  "".join(_.xpath('.//span[contains(text(),"有效期")]/following-sibling::span//text()'))
            JSK_url.save(item)
            self.log.info(f'数据{ item["_id"]}存入完成。。。。')

    def spider(self,page):

        try:
            self.page = page
            self.baseurl = f'https://www.jiansheku.com/jianzaoshi_{str(page)}.html'
            resp = self.get_req(url=self.baseurl)
            self.xpath_ltpage((resp.text.replace("\r","").replace("\n","").replace("\t","")))
            self.log.info(f'第{self.page}页数据抓取完毕')
        except Exception as e:
            pass

    def to_redis(self):

        resp = JSK_url.find()
        for _ in resp:
            red_cli.sadd("jsk",str(_))
            self.log.info("存入redis成功")

    def date_xpath(self,resp,id):

        items = {}
        etre = HTML(resp)
        items["_id"] = id
        items["name"] = "".join(etre.xpath('//div[@class="zbxq_name"]/text()'))
        items["company"] = "".join(etre.xpath('//div[@class="zbxq_time"]/a[1]/text()'))
        items["userID"] = "".join(etre.xpath('//div[@class="zbxq_time"]/span//label/text()'))

        cont = etre.xpath('//div[@class="see"]/table')
        if len(cont) > 1:

            # 证书名称 执业印章号 注册专业 注册编号 有效期

            trlt = etre.xpath('//div[@class="see"]/table[1]//tr')
            first = []
            k = 0
            v = 3
            for x in range(len(trlt) + 1):
                if v == x:
                    y = trlt[k:v]
                    first.append(y)
                    k += 3
                    v += 3

            for _ in range(len(first)):
                items[f"certificate_name_{str(_)}"] = "".join(first[_][0].xpath('.//td[2]//text()'))
                items[f"practice_seal_{str(_)}"] = "".join(first[_][0].xpath('.//td[4]//text()'))
                items[f"reg_major_{str(_)}"] = "".join(first[_][1].xpath('.//td[2]//text()'))
                items[f"reg_number_{str(_)}"] = "".join(first[_][1].xpath('.//td[4]//text()'))
                items[f"validity_time_{str(_)}"] = "".join(first[_][2].xpath('.//td[2]/span/span[2]/text()'))


            tr_2_lt = etre.xpath('//div[@class="see"]/table[2]//tr')
            second = []
            k = 0
            v = 2

            for x in range(len(tr_2_lt) + 1):
                if v == x:
                    y = tr_2_lt[k:v]
                    second.append(y)
                    k += 2
                    v += 2
            for _ in range(len(second)):
                items[f"certificate_category_{str(_)}"] = "".join(second[_][0].xpath('.//td[2]//text()'))
                items[f"certificate_num_{str(_)}"] = "".join(second[_][1].xpath('.//td[2]//text()'))
                items[f"cer_validity_time_{str(_)}"] = "".join(second[_][1].xpath('.//td[4]/span/span[2]/text()'))
        # 证书类型 证书编号 证书名称 执业印章号 注册专业 注册编号 有效期
        else:
            trlt = etre.xpath('//div[@class="see"]/table[1]//tr')
            first = []
            k = 0
            v = 3
            for x in range(len(trlt) + 1):
                if v == x:
                    y = trlt[k:v]
                    first.append(y)
                    k += 3
                    v += 3

            for _ in range(len(first)):
                items[f"certificate_name_{str(_)}"] = "".join(first[_][0].xpath('.//td[2]//text()'))
                items[f"practice_seal_{str(_)}"] = "".join(first[_][0].xpath('.//td[4]//text()'))
                items[f"reg_major_{str(_)}"] = "".join(first[_][1].xpath('.//td[2]//text()'))
                items[f"reg_number_{str(_)}"] = "".join(first[_][1].xpath('.//td[4]//text()'))
                items[f"validity_time_{str(_)}"] = "".join(first[_][2].xpath('.//td[2]/span/span[2]/text()'))

        JSK_date.save(items)
        self.log.info(f"数据{id}存入成功")


    def date_info(self):
        count = red_cli.scard("jsk")
        while count:
            try:
                data = red_cli.srandmember("jsk")
                item = eval(data)
                url = item["date_info_url"]
                # url = "https://www.jiansheku.com/qy_7307359/rynew_0a5859125ade4b6dac692780c4005b59.html"
                resp = self.get_req(url)
                try:
                    self.date_xpath((resp.text.replace("\r", "").replace("\n", "").replace("\t", "")),item["_id"])
                    red_cli.srem("jsk",data)
                    count -= 1
                except:
                    print("解析错误")
            except:
                pass

start = JS_spider()
# for _ in range(99,101):
#     start.spider(_)
#     time.sleep(5)
# start.to_redis()

import threading
for i in range(10):
    t = threading.Thread(target=start.date_info())
    t.start()
    print("please wait!")