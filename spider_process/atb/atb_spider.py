import requests
import pymongo
import hashlib
import time
import redis
import gc
from common import ABY,STATIC_IP,get_log
from lxml.etree import HTML

from concurrent.futures import ThreadPoolExecutor
log = get_log()
SPIDERDB = pymongo.MongoClient(host='172.16.75.28',port=27017)
ATB = SPIDERDB["BMD"]["ATB_URL"]
ATB_DATA_URL = SPIDERDB["BMD"]["ATB_data_URL"]
ATB_Data_Info = SPIDERDB["BMD"]["ATB_Data_Info"]
red_cli = redis.Redis(host="172.16.75.38",port=6379,db=14)

class atb_url(object):
    """阿土伯交易网站爬虫程序"""
    def __init__(self):
        self.url = 'http://www.atobo.com/Companys/s-p8-s137/'
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })
        self.proxy, self.ipItem = ABY()
        self.IPcount = 0
        self.page = 0

    def get_proxy(self):
        """重新获取IP代理"""
        self.ipItem["flag"] = "0"
        STATIC_IP.save(self.ipItem)
        self.IPcount += 1
        self.proxy, self.ipItem = ABY()

    def get_req(self,url,paramas=None):
        """get请求封装"""
        try:
            if self.IPcount < 3:
                resp = self.s.get(url=url,params=paramas,proxies=self.proxy,timeout=60)
                # resp = self.s.get(url=url,params=paramas)
                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    self.IPcount = 0
                    return resp
                # elif resp.status_code == 403:
                #     return "403"
                else:
                    if "可能是您要找的信息已经删除" in resp.text:
                        return "可能是您要找的信息已经删除"
                    self.get_proxy()
                    self.get_req(url,paramas)
            else:
                log.info(url)
                self.IPcount = 0
                log.info("超过3次请求失败")
                self.get_proxy()
                return None

        except Exception as e:
            log.info(e)
            self.get_proxy()
            self.get_req(url, paramas)

    def run(self):
        """程序入口，按照地区加分类条件进行搜素存储URL

        """

        try:
            resp = self.get_req(self.url)

            etre = HTML(resp.text)
            class_name_lt = etre.xpath('//div[@id="filterCate"]/ul/li/a/text()')
            class_url_lt = etre.xpath('//div[@id="filterCate"]/ul/li/a/@href')

            area_name_lt = etre.xpath('//div[@id="filterArea"]/ul/li/a/text()')
            area_url_lt = etre.xpath('//div[@id="filterArea"]/ul/li/a/@href')

            city = "".join(etre.xpath('//a[contains(text(),"城市：")]/text()')).replace("城市：","").replace(" ","")
            province = "".join(etre.xpath('//a[contains(text(),"省/直辖市：")]/text()')).replace("省/直辖市：","").replace(" ","")
            for x in range(len(area_name_lt)):
                item = {}
                item["area"] = area_name_lt[x]
                item["city"] = city
                item["province"] = province
                area_url = area_url_lt[x]
                base_url = "http://www.atobo.com" + area_url
                for _ in range(len(class_name_lt)):
                    class_url = class_url_lt[_].split('-')[-1]
                    url = base_url + f'-{class_url}'
                    item["class_name"] = class_name_lt[_]
                    item["url"] = url
                    item["_id"] = hashlib.md5(url.encode('utf-8')).hexdigest()
                    ATB.save(item)
                    log.info(f'{item["_id"]}存入mongo成功。。。')

        except Exception as e:
            log.info("主程序错误")

    def redis_page(self):
        """
        :param 从mongo中读取地区加分类存储好的URL数据存入redis
        :return:
        """
        result = ATB.find({"city":"佛山"})

        for _ in result:
            red_cli.sadd("wh_atb_page_url",str(_))
            log.info("存入redis成功")

    def xpath_page(self,etre,type):
        """
        解析页面信息
        :param
        :return:
        """

        if type == "page":
            try:
                company_name_lt = etre.xpath('//a[@class="CompanyName"]/text()')
                company_name_url = etre.xpath('//a[@class="CompanyName"]/@href')
                company_product_xpath = etre.xpath('//li[@class="pp_product"]')
                company_addr_xpath = etre.xpath('//li[@class="pp_address"]')
                company_cname_lt = etre.xpath('//li[@class="c_name"]/text()')
                company_city_lt = etre.xpath('//li[@class="localsearch"]')
                for _ in range(len(company_name_lt)):
                    item = {}
                    item["company_name"] = company_name_lt[_]
                    item["_id"] = hashlib.md5(company_name_lt[_].encode('utf-8')).hexdigest()
                    item["company_url"] = "http://www.atobo.com" + company_name_url[_]
                    item["company_product"] = "".join(company_product_xpath[_].xpath(".//text()")).replace("主营：","")
                    item["company_addr"] = "".join(company_addr_xpath[_].xpath("./text()")).replace("地址：","")
                    item["company_cname"] = company_cname_lt[_]
                    localsearch = "".join(company_city_lt[_].xpath(".//text()"))
                    item["area"] = localsearch.split('-')[-1].replace(" ","")
                    item["city"] = localsearch.split('-')[1].replace(" ","")
                    item["province"] = localsearch.split('-')[0].replace(" ","")
                    ATB_DATA_URL.save(item)
                    log.info(f'数据{item["_id"]}存入mongo完成')
            except Exception as e:
                pass
        elif type == "phone":
            pass

    def spider_page_url(self):
        """
        根据分类好的URL进行每页的数据抓取，后续补充手机号
        :return:
        """
        count = red_cli.scard("wh_atb_page_url")
        while count:
            try:
                data = red_cli.srandmember("wh_atb_page_url")
                url = eval(data)["url"]
                resp = self.get_req(url)

                if resp and resp != '403':
                    etre = HTML(resp.text)
                    self.page = int("".join(etre.xpath('//li[@class="spagelist"]/strong[2]/text()'))) - 1
                    self.xpath_page(etre=etre,type="page")
                    page = 2
                    while self.page:
                        url = url[0:-1] + f'-y{str(page)}/'
                        resp = self.get_req(url)
                        if resp:
                            etre = HTML(resp.text)
                            self.xpath_page(etre=etre, type="page")
                            log.info(f"第{page}页数据抓取完毕")
                            page += 1
                            self.page -= 1
                        else:
                            print("从新抓取")

                    red_cli.srem("wh_atb_page_url",data)
                    log.info(f'{eval(data)["_id"]}数据全部抓取完成从redis删除成功')
                    count -= 1
                elif resp == '403':
                    log.info('无效URL')
                    red_cli.srem("wh_atb_page_url", data)
                    count -= 1

            except Exception as e:
                log.info(e)


    def to_redis(self):
        """把需要补充手机号的数据存入redis"""
        result = ATB_DATA_URL.find({"flag":{"$exists":False}})
        for _ in result:
            _["flag"] = "1"
            ATB_DATA_URL.save(_)
            red_cli.sadd("atb_data_phone",str(_))
            log.info(f"数据{_['_id']}存入redis完成。。。。。。。")

    def data_info(self):
        """
        :param
        :return
        """
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36",
        })
        count = red_cli.scard("atb_data_phone")

        while count:
            try:
                data = red_cli.srandmember("atb_data_phone")
                url = eval(data)["company_url"].replace("www","m")
                item = eval(data)

                if "Companys" not in url:
                    red_cli.srem("atb_data_phone", data)
                    count -= 1
                else:
                    resp = self.get_req(url)

                    if resp == "可能是您要找的信息已经删除":
                        red_cli.srem("atb_data_phone", data)
                        log.info("页面数据不存在删除")
                        count -= 1

                    if resp:
                        etre = HTML(resp.text)
                        item["phone"] = "".join(etre.xpath('//td[contains(text(),"机")]/following-sibling::td[1]//text()'))
                        item["tel"] = "".join(etre.xpath('//td[contains(text(),"话")]/following-sibling::td//text()'))
                        item["city"] = eval(data)["city"].replace(" ","")
                        ATB_Data_Info.save(item)
                        red_cli.srem("atb_data_phone",data)
                        log.info(f"数据{item['_id']}存入mongo完成")
                        count -= 1
                        time.sleep(0.5)

                    else:
                        log.info("页面为空，IP被检测。。。。")
                        self.get_proxy()
                    gc.collect()
            except Exception as e:
                log.info(e)

def main():
    start = atb_url()

    # start.run()
    # start.redis_page()
    # start.spider_page_url()
    # start.to_redis()
    start.data_info()


if __name__ == '__main__':

    # 多线程
    # seed = ["1"]
    with ThreadPoolExecutor(5) as executor:

        for _ in range(0,2):
            executor.map(main())