import sys
import re
import hashlib
import pymongo
sys.path.insert(0,r"D:\bmd\bmd_server")
sys.path.insert(0,r"D:\bmd\bmd_server\spider_manage\backend\backend\apps\Crawler_page\sdxy")
# from spiders.common import get_log,ABY
from untils.common import get_log,ABY
import requests
from lxml.etree import HTML
from .XPATH import WaterCredit
from datetime import datetime
log = get_log()


MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

class basc_Spider(object):
    def __init__(self,key,ApiType=None):

        self.url = "https://shuidi.cn/b-search?key={}"
        self.keys = key
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        })
        self.proxy,self.ip_id = ABY()
        self.sd_xpath = WaterCredit()
        self.ApiType = ApiType

    def get_req(self,url):

        count = 1
        while count:

            # if proxy:
            try:

                resp = self.s.get(url=url,proxies=self.proxy)
                # resp = self.s.get(url=url,timeout=10)
                resp.encoding = resp.apparent_encoding
                if resp.status_code == 200:
                    if "请输入你的验证码" in resp.text:

                        self.proxy,self.ip_id = ABY()
                        STATIC_IP.update_one({"_id":self.ip_id},{"flag":"1"})
                    else:
                        return resp

            except Exception as e:

                count += 1
                self.proxy,self.ip_id = ABY()
                if self.proxy or count > 3:
                    return "IP无效"
            # else:
            #     return "IP无效"

    def gsxx(self,resp):
        """
        解析工商信息
        :return:
        """
        gsxx = self.sd_xpath.gsxx(HTML(resp))
        return gsxx

    def gdxx(self,resp):
        """
        解析股东信息
        :return:
        """
        gsxx = self.sd_xpath.gdxx(HTML(resp))
        return gsxx

    def base_first_page(self, items, resp,url):
        """
        解析首页信息
        :param items:
        :param resp:
        :return:
        """

        etre = HTML(resp)
        lawDangerous = {}
        # _id 公司名称 联系电话 联系人 公司地址 公司所在城市 网站信息更新时间 经营状态 信息抓取入库时间 来源网址 来源网站
        items["_id"] = hashlib.md5(str(self.keys).encode('utf-8')).hexdigest()
        items["companyName"] = self.keys
        items.update({"companyTel":"-"})
        items.update({"outName":"-"})
        items["companyAddr"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"企业地址")]/following-sibling::td[1]/text()'))
        items.update({"companyCity": "-"})
        items["companyProvince"] = "".join(etre.xpath('//table[@class="table1"]//tr[6]/td[2]/text()'))
        items["updateTime"] = "".join(etre.xpath('//div[@class="pull_left update_time"]/text()')).replace("\n","").replace(" ","")
        items["businessState"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"登记状态")]/following-sibling::td[1]/text()'))
        items["collectTime"] = str(datetime.now())
        items["companyUrl"] = url
        items["webSource"] = "https://shuidi.cn/"

        base = {}
        #基本工商信息
        gsxx = self.gsxx(resp)
        base["baseInfo"] = gsxx
        items["base"] = base

    def start(self):
        try:
            url = self.url.format(self.keys)
            resp = self.get_req(url)
            if resp != 'IP无效':
                resp.encoding = "UTF-8"
                etre = HTML(resp.text)
                urls = etre.xpath('//a[@class="or_look"]/@href')
                name = etre.xpath('//div[@class="or_look_tit"]/span/a/@companyname')
                if urls and name:
                    #指定抓取
                    if name[0] == self.keys:
                        items = {}
                        if self.ApiType == "基本信息查询" or self.ApiType == '股东信息查询':
                            url = "https://shuidi.cn" + urls[0]
                            resp = self.get_req(url)
                            resp.encoding = "UTF-8"
                            if  self.ApiType == "基本信息查询":
                                self.base_first_page(items, resp.text, url)
                            elif self.ApiType == '股东信息查询':
                                gdxx = self.gdxx(resp.text)
                                items["holderInfo"] = gdxx
                        return items
                    else:
                        log.info("公司名不匹配")
                        result = "公司名不匹配"
                        return result
                else:
                    if urls == []:
                        log.info("页面为空")
                        return "页面为空"

                    if re.search('点我验证身份',resp.text):
                        log.info("IP无效")
                        return "IP无效"
                    else:
                        log.info("未搜索到公司")
                        result = "未搜索到公司"
                        return result
            else:
                return "IP无效"
        except Exception as E:
            log.info(E)

def basc_start(key,ApiType=None):
    """
    程序入口
    :return:
    """
    RUN = basc_Spider(key,ApiType)
    results = RUN.start()

    if results == "未搜索到公司":
        return "未搜索到公司"

    elif results == "公司名不匹配":
        return "公司名不匹配"

    elif results == "IP无效":
        return "IP无效"

    elif results == "页面为空":
        return "页面为空"
    else:
        print(results)
        return results


# run(key="华为技术有限公司")
