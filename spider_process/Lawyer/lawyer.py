#encoding=utf-8

import requests
import hashlib
import pymongo
from lxml.etree import HTML

from concurrent.futures import ThreadPoolExecutor
from BKW.common import ABY,STATIC_IP,get_log

MONGO_DB = pymongo.MongoClient(host='172.16.74.249',port=27017)

LAWYER_URI = MONGO_DB["YANG"]["LAWYER_URI"]
LAWYER_INFO = MONGO_DB["YANG"]["LAWYER_INFO"]

import redis
red_cli = redis.Redis(host="172.16.75.38",port=6379,db=15)

log = get_log()
class lawyey(object):

    def __init__(self):
        # 成都，深圳，广州，杭州，武汉，北京，长沙，石家庄，东莞，宜昌，重庆  各50个
        self.urllt = [
            # {"url":"https://www.66law.cn/chengdu/lawyer/page_1.aspx","city":"成都"},
            # {"url":"https://www.66law.cn/shenzhen/lawyer/page_1.aspx","city":"深圳"},
            # {"url":"https://www.66law.cn/guangzhou/lawyer/page_1.aspx","city":"广州"},
            # {"url":"https://www.66law.cn/hangzhou/lawyer/page_1.aspx","city":"杭州"},
            # {"url":"https://www.66law.cn/wuhan/lawyer/page_1.aspx","city":"武汉"},
            # {"url":"https://www.66law.cn/beijing/lawyer/page_1.aspx","city":"北京"},
            # {"url":"https://www.66law.cn/changsha/lawyer/page_1.aspx","city":"长沙"},
            # {"url":"https://www.66law.cn/shijiazhuang/lawyer/page_1.aspx","city":"石家庄"},
            # {"url":"https://www.66law.cn/dongzuo/lawyer/page_1.aspx","city":"东莞"},
            {"url":"https://www.66law.cn/yichang/lawyer/page_1.aspx","city":"宜昌"},
            # {"url":"https://www.66law.cn/chongqing/lawyer/page_1.aspx","city":"重庆"},
        ]
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            # "upgrade-insecure-requests": "1",
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        })
        self.page = 1
        self.pagecount = 100
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
                elif resp.status_code == 404:
                    return "404"
                else:
                    self.ipItem["flag"] = "0"
                    STATIC_IP.save(self.ipItem)
                    self.IPcount += 1
                    self.proxy, self.ipItem = ABY()
                    self.get_req(url,paramas)
            else:
                self.IPcount = 0
                log.info("超过3次请求失败")
                return None

        except Exception as e:
            log.info(e)
            self.ipItem["flag"] = "0"
            STATIC_IP.save(self.ipItem)
            self.IPcount += 1
            self.proxy, self.ipItem = ABY()
            self.get_req(url, paramas)

    def get_data(self,url,city):
        """抓取数据"""
        resp = self.get_req(url)
        if resp:

            etre = HTML(resp.text)
            namelt = etre.xpath('//div[@class="name"]/a/text()')
            dataurl_lt = etre.xpath('//div[@class="name"]/a/@href')

            for _ in range(len(namelt)):
                item = {}

                item["_id"] = hashlib.md5(namelt[_].encode('utf-8')).hexdigest()
                item["name"] = namelt[_]
                item["url"] =f"https:{dataurl_lt[_]}lawyer_message.aspx"
                item["phone_url"] =f"https:{dataurl_lt[_]}lawyer_contact.aspx"
                item["city"] = city
                LAWYER_URI.save(item)
                log.info("数据存储成功。。。。。。。")

            if self.page == 2:
                self.pagecount = int(etre.xpath('//a[contains(text(),">")]/preceding-sibling::a[1]/text()')[0])

            k = f"page_{str(self.page)}"
            self.page += 1
            p = f"page_{str(self.page)}"

            if int(self.page) <= self.pagecount:
                url = url.replace(k,p)
                self.get_data(url,city)
            else:
                self.page = 1
                log.info(f"{city}地区数据列表抓取完毕")
        else:
            self.get_data(url, city)

    def TO_redis(self):
        result = LAWYER_URI.find()
        for _ in result:
            red_cli.sadd("lawyer",str(_))
            log.info("数据存入缓存成功")

    def get_data_info(self):
        """
        获取详情信息
        :return:
        """
        count = red_cli.scard("lawyer")
        while count:
            data = red_cli.srandmember("lawyer")
            url= eval(data)["url"]

            resp = self.get_req(url)
            if resp:
                if resp == "404":
                    log.info("页面错误删除")
                    red_cli.srem("lawyer",data)
                else:
                    etre = HTML(resp.text)

                    item = {}
                    #姓名 城市 介绍 擅长领域
                    item["_id"] = eval(data)["_id"]
                    item["name"] = eval(data)["name"]
                    item["city"] =  eval(data)["city"]
                    item["weburl"] =  eval(data)["url"]
                    item["introduce"] = "".join(etre.xpath('//div[@id="intro"]//text()|//div[@class="un-nr"]//text()')).replace("\xa0","").replace("\r","").replace("\n","").replace(" ","")

                    item["field"] = ",".join(etre.xpath('//span[contains(text(),"擅长领域")]/ancestor::li/text()|'
                                                        '//ul[@class="sc-tag mt25"]//text()|//p[contains(text(),"主攻方向")]/text()'))\
                        .replace("\r","").replace("\n","").replace(" ","").replace("主攻方向：","")

                    item["LicenseNo"] = "".join(etre.xpath('//span[contains(text(),"执业证号")]/ancestor::li/text()|//label[contains(text(),'
                                                           '"执业证号")]/following-sibling::p/text()')).replace("\r","").replace("\n","").replace(" ","")

                    item["img_url"] = "https:" + "".join(etre.xpath('//div[@class="lawyer"]//img/@src|//div[@class="img-block"]/img/@src|//div[@class="lr-infor"]//img/@src'))
                    item["Company"] = "".join(etre.xpath('//span[contains(text(),"执业单位")]/ancestor::li/text()|//ul[@class="info"]/li[3]/text()|//label[contains(text(),"律所名称")]/following-sibling::p/text()|//span[contains(text(),"执业机构")]/following-sibling::text()')).replace("\r","").replace("\n","").replace(" ","")
                    item["tel"] = "".join(etre.xpath('//span[contains(text(),"机：")]/following-sibling::span/text()|//div[@class="tel"]/b/text()'))

                    if len(item["tel"]) > 2:
                        LAWYER_INFO.save(item)
                        log.info("数据存入mongo完成")
                        red_cli.srem("lawyer", data)
                    else:
                        url = eval(data)["phone_url"]
                        rp = self.get_req(url)
                        if rp:
                            etre = HTML(rp.text)
                            item["tel"] = "".join(etre.xpath('//label[contains(text(),"手机号")]/following-sibling::p/text()'))
                            LAWYER_INFO.save(item)
                            log.info("数据存入mongo完成")
                            red_cli.srem("lawyer", data)
                        else:
                            log.info("手机号获取失败")
            else:
                self.ipItem["flag"] = "0"
                STATIC_IP.save(self.ipItem)
                self.IPcount += 1
                self.proxy, self.ipItem = ABY()
                log.info("未获取到页面数据")


    def run(self):
        """抓取列表页数据"""

        for items in self.urllt:
            url = items["url"]
            city = items["city"]
            self.get_data(url,city)

    def img_to_redis(self):
        result = LAWYER_INFO.find()
        for _ in result:
            red_cli.sadd("lawyerimg",str(_))
            log.info("数据存入缓存成功")

    def downloadimg(self):
        """下载图片"""
        count = red_cli.scard("lawyerimg")
        while count:
            data = red_cli.srandmember("lawyerimg")
            url= eval(data)["img_url"].replace("https:https:","https:")
            # url = "https://imgt.66law.cn/upload/t/201910/8/1601019140.jpg"
            _id = eval(data)["_id"]
            try:
                resp = self.s.get(url)
                path = r'E:\code\spider\spider_process\Lawyer\img\{}.png'.format(_id)
                with open(path,'wb')as fp:
                    fp.write(resp.content)
                    log.info(f"数据{_id}的图片存储成功")
                red_cli.srem("lawyerimg",data)
                count -= 1
            except Exception as e:
                print(e)
                if url == 'https:':
                    red_cli.srem("lawyerimg", data)
def main():
    st = lawyey()
    st.downloadimg()


# 多线程
executor = ThreadPoolExecutor(max_workers=5)
for i in range(1):
    executor.submit(main)



