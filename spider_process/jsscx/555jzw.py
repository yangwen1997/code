'''
author yangwenlong
time 2020/7/14
'''
import redis
import hashlib
import requests
from jsscx.common import REQ, JZW555_category, JZW555_url, JZW555_date,ABY,get_log

from lxml.etree import HTML

red_cli = redis.Redis(host="172.16.75.38",port=6379,db=14)
class jzw_spider(REQ):

    def __init__(self):
        super(REQ, self).__init__()  # 继承父类的__init__方法并拥有自己的初始化方法
        self.baseurl = 'http://www.555gk.com/resume/r0t5c0.html'
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })
        self.proxy, self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()

    def information_classification(self):
        """信息分类"""
        try:
            resp = self.get_req(self.baseurl)
            if resp:
                res = resp.text.replace("\r", "").replace("\t", "").replace("\n", "")
                etre = HTML(res)
                namelt = etre.xpath(
                    '//div[contains(text(),"信息分类")]/following-sibling::div[1]/a[1]/following-sibling::a/text()')
                href_lt = etre.xpath(
                    '//div[contains(text(),"信息分类")]/following-sibling::div[1]/a[1]/following-sibling::a/@href')
                for _ in range(len(namelt)):
                    item = {}
                    item["name"] = namelt[_]
                    item["url"] = "http://www.555gk.com" + href_lt[_]
                    item["_id"] = hashlib.md5(item["url"].encode("utf-8")).hexdigest()
                    JZW555_category.save(item)
                    self.log.info(f"数据{item['_id']}存入mongo")
            else:
                print("页面请求失败")

        except Exception as e:
            print(e)

    def TO_redis(self,name,DB,condition=None):
        """数据存入redis"""
        if condition:
            result = DB.find(condition)
        else:
            result = DB.find()

        for _ in result:
            red_cli.sadd(name,str(_))
            self.log.info("数据存入redis。。。。。。。")

    def xpath_page(self,resp,category):
        """
        列表页规则解析
        :return:
        """
        etre = HTML(resp)
        tr_lt = etre.xpath('//thead//following-sibling::tbody/tr')

        for _ in tr_lt:
            item = {}
            item["category"] = category
            item["url"] = "http://www.555gk.com" + "".join(_.xpath('.//td[1]/a/@href')).strip(" ")
            item["name"] = "".join(_.xpath('.//td[1]/a/text()')).strip(" ")
            item["state"] = "".join(_.xpath('.//td[2]/text()')).strip(" ")
            item["price"] = "".join(_.xpath('.//td[3]/text()')).strip(" ")
            item["Registration"] = "".join(_.xpath('.//td[4]/text()')).strip(" ")
            item["major"] = "".join(_.xpath('.//td[5]/text()')).strip(" ")
            item["region"] = "".join(_.xpath('.//td[6]/text()')).strip(" ")
            item["updateTime"] = "".join(_.xpath('.//td[7]/text()')).strip(" ")
            item["_id"] = hashlib.md5(item["url"].encode('utf-8')).hexdigest()
            JZW555_url.save(item)
            self.log.info(f"数据{item['_id'] }存入成功")


    def page_list(self):
        """列表分页"""
        count = red_cli.scard("information_classification")
        while count:
            data = red_cli.srandmember("information_classification")

            url = eval(data)["url"]
            category =  eval(data)["name"]
            try:
                resp = self.get_req(url)
                print(url)
                res = resp.text.replace("\r","").replace("\n","").replace("\t","")
                self.xpath_page(res,category)

                etre = HTML(res)
                pagelt = etre.xpath('//a[@class="next layui-laypage-next"]/preceding-sibling::span/following-sibling::a/@href')

                self.log.info("第1页数据抓取完毕")
                if len(pagelt) == 1:
                    self.log.info("当前类别只有一页")
                else:
                    pagelt = pagelt[0:-1]
                    page_count = 2
                    for _ in pagelt:
                        urls = "http://www.555gk.com" + _
                        resp = self.get_req(urls)
                        res = resp.text.replace("\r","").replace("\n","").replace("\t","")
                        self.xpath_page(res, category)
                        self.log.info(f"第{str(page_count)}页数据抓取完毕")
                        page_count += 1
                red_cli.srem("information_classification",data)
                count -= 1
            except:
                pass

    def date_spider(self):
        '''抓取详情页面数据，手机号后续登录后单独抓取'''

        count = red_cli.scard("date_jzw")

        while count:
            data = red_cli.srandmember('date_jzw')
            items = eval(data)
            url = items["url"]

            try:
                resp = self.get_req(url)
                res = resp.text.replace("\r","").replace("\n","").replace("\t","")
                etre = HTML(res)
                item = {}
                item["_id"] = items["_id"]
                item["zj_Name"] = "".join(etre.xpath('//h1/text()'))
                item["information_classification"] = "".join(etre.xpath('//ul[@class="list a3"][3]/li[1]/a/text()')).replace("证书类型：","")
                item["certificate_location"] = "".join(etre.xpath('//ul[@class="list a3"][3]/li[2]/a/text()')).replace("证书所在地：","")
                item["social_security_location"] = "".join(etre.xpath('//ul[@class="list a3"][3]/li[3]//text()')).replace("社保所在地：","")
                item["registration"] = "".join(etre.xpath('//ul[@class="list a3"][3]/li[4]//text()')).replace("注册情况：","")
                item["certificate_status"] = "".join(etre.xpath('//ul[@class="list a3"][4]/li[1]//text()')).replace("证书状态：","")
                item["certificate_usage"] = "".join(etre.xpath('//ul[@class="list a3"][4]/li[2]//text()')).replace("证书用途：","")
                item["certificate_applicable"] = "".join(etre.xpath('//ul[@class="list a3"][4]/li[3]//text()')).replace("证书适用：","")
                item["price"] = "".join(etre.xpath('//ul[@class="list a3"][4]/li[4]//text()')).replace("价格：","")
                item["category"] = items["category"]
                item["updateTime"] = items["updateTime"]
                item["url"] = f"http://www.555gk.com/resume/check_resume?id={items['url'].split('/')[-1].split('.')[0]}"
                item["flag"] = "1"
                JZW555_date.save(item)
                self.log.info("数据存入mongo")
                red_cli.srem("date_jzw",data)
                count -= 1
            except Exception as e:
                print(e)


    def phone_save(self):
        while 1:
            resp = JZW555_date.find_one({"flag":"1"})
            if resp:
                url = resp["url"]
                self.s = requests.session()
                self.s.headers.update({
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
                    "Cookie": "QYK=16nb6km77fftuc2jpc67k4hub0; Hm_lvt_5596a3543de444306c876a4b981c5c6b=1594706260; remember=think%3A%5B%221%22%2C%221D1K1F1K1E1G1K1L1C1C1K%22%2C%222G29293C392Q2P321G1I1D1K%22%5D; motto=%E5%8A%AA%E5%8A%9B%E7%9A%84%E6%97%B6%E5%85%89%E6%98%AF%E6%9C%AC%E4%B9%A6%EF%BC%8C%E7%BF%BB%E4%B8%80%E9%A1%B5%E6%98%AF%E4%B8%80%E9%A1%B5; Hm_lpvt_5596a3543de444306c876a4b981c5c6b=1594709841"
                })

                resps = self.s.get(url)
                etre = HTML(resps.text)
                resp["phone"] = "".join(etre.xpath('//label[contains(text(),"手机号码")]/following-sibling::div//text()'))
                resp["QQ"] = "".join(etre.xpath('//label[contains(text(),"QQ号码")]/following-sibling::div//text()'))
                resp["Email"] = "".join(etre.xpath('//label[contains(text(),"电子邮箱")]/following-sibling::div//text()'))
                resp["flag"] = "2"
                JZW555_date.save(resp)
                self.log.info(f"数据{resp['_id']}手机号码补充完成")
            else:
                break

spider = jzw_spider()
# spider.TO_redis(name="date_jzw",DB=JZW555_url)
# spider.page_list()

from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=20)
for i in range(15):
    executor.submit(spider.phone_save())
