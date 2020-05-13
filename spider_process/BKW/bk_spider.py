import requests
import hashlib
import math
import redis

from BKW.common import ABY,STATIC_IP,BKID,get_log,BK_DATA_info
from lxml.etree import HTML

red_cli = redis.Redis(host="172.16.75.38",port=6379,db=15)
log = get_log()

class BK(object):
    """标库网爬虫程序"""

    def __init__(self):
        self.page = 1

        self.pageCount = None
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })
        self.proxy,self.ipItem = ABY()
        self.IPcount = 0

    @classmethod
    def item_clear(cls,item):
        """去除指定字符"""
        it = {}
        for k,v in item.items():
            if type(v) == list:
                pass
            elif k == "regist_time":
                it[k] = v.replace("\r", "").replace("\t", "").replace("\n", "").replace("\xa0", "").replace(" ","")\
                    .replace("我要买","").replace("我要卖","")
            else:
                it[k] = v.replace("\r","").replace("\t","").replace("\n","").replace("\xa0","").strip(" ")

        return it

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
                log.info("超过3次请求失败")
                return None

        except Exception as e:
            log.info(e)
            self.ipItem["flag"] = "0"
            STATIC_IP.save(self.ipItem)
            self.IPcount += 1
            self.proxy, self.ipItem = ABY()
            self.get_req(url, paramas)

    def trade_url_lt(self,tradeName):
        """获取列表页url"""
        url = f"https://www.tmkoo.com/search.php?pageNo={str(self.page)}&searchKey={tradeName}&st=4"

        resp = self.get_req(url)
        etre = HTML(resp.text)
        url_LT = etre.xpath('//div[@class="info"]//span[@class="tmname"]/ancestor::a/@href')
        regno_LT = etre.xpath('//div[@class="info"]//span[@class="regno"]/text()')
        for _ in range(len(url_LT)):
            item = {}
            item["url"] = "https://www.tmkoo.com" + url_LT[_]
            item["_id"] = hashlib.md5(item["url"].encode('utf-8')).hexdigest()
            item["flag"] = "0"
            BKID.save(item)
            log.info(f'数据{item["_id"]}存入mongo完成')
        if self.pageCount:
            if self.page <= self.pageCount:
                self.page += 1
                self.trade_url_lt(tradeName)
        else:
            data_count = "".join(etre.xpath('//div[@class="pager"][2]/span[1]/text()'))
            self.pageCount = math.ceil(int(data_count) / 30)
            if self.page < self.pageCount:
                self.page += 1
                self.trade_url_lt(tradeName)
            else:
                log.info("只有1页数据")

    def TO_Redis(self):
        """
        同步数据到redis进行缓存
        :return:
        """
        result = BKID.find({"flag":"0"})
        for _ in result:
            item = _
            red_cli.sadd("BKID", str(item))
            BKID.find_one_and_update({"_id": item["_id"]}, {"$set": {"flag": "1"}})
            print("数据存入redis sucess")

    def serach_trade(self,regNum="6297431",tmName="切迟杜威"):
        """指定商标搜索"""
        url = f"https://www.tmkoo.com/search.php?searchKey={tmName}&st=4"
        resp = self.get_req(url)
        etre = HTML(resp.text)

        url_LT = etre.xpath('//div[@class="info"]//span[@class="tmname"]/ancestor::a/@href')
        regno_LT = etre.xpath('//div[@class="info"]//span[@class="regno"]/text()')
        if url_LT and regno_LT:
            if len(regno_LT) == len(url_LT):
                for _ in range(len(url_LT)):
                    item = {}
                    if regno_LT[_].replace("注册号:","") == regNum:
                        item["url"] = "https://www.tmkoo.com" + url_LT[_]
                        item["_id"] = hashlib.md5(regNum.encode('utf-8')).hexdigest()
                        item["regNum"] = regNum
                        item["tmName"] = tmName
                        item["flag"] = "0"
                        BKID.save(item)
                        log.info(f'数据{item["_id"]}存入mongo完成')
                        break
                    else:pass
            else:
                log.info("规则匹配错误")
        else:
            log.info("页面数据获取为空")

    def trade_info(self):
        """
        抓取商标详细信息页面
        :return:
        """

        self.s.headers.update({
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        })
        data = red_cli.srandmember("BKID")
        url = eval(data)["url"]
        # url = 'https://www.tmkoo.com/detail/24ff6eaa997007f2967541ee3bb13223/11/'
        resp = self.get_req(url)
        etre = HTML(resp.text)

        regist_num = "".join(etre.xpath('//td[contains(text(),"注册号")]/following-sibling::td[1]/font/text()'))
        international_class = "".join(etre.xpath('//td[contains(text(),"注册号")]/following-sibling::td[2]/font/text()'))
        regist_time = "".join(etre.xpath('//td[contains(text(),"申请日期")]/following-sibling::td[1]//text()'))
        registrant_chinese_name = "".join(etre.xpath('//td[contains(text(),"申请人名称(中文)")]/following-sibling::td[1]/div/text()'))
        registrant_foreign_name = "".join(etre.xpath('//td[contains(text(),"申请人名称(英文)")]/following-sibling::td[1]//text()'))
        registrant_foreign_address = "".join(etre.xpath('//td[contains(text(),"申请人地址(英文)")]/following-sibling::td[1]//text()'))
        image_url = "".join(etre.xpath('//td[@align="center"]/img/@src'))
        preliminary_notice_num = "".join(etre.xpath('//td[contains(text(),"初审公告期号")]/following-sibling::td[1]//text()'))
        regist_notice_num = "".join(etre.xpath('//td[contains(text(),"注册公告期号")]/following-sibling::td[1]//text()'))
        preliminary_notice_time = "".join(etre.xpath('//td[contains(text(),"初审公告日期")]/following-sibling::td[1]//text()'))
        regist_notice_time = "".join(etre.xpath('//td[contains(text(),"注册公告日期")]/following-sibling::td[1]//text()'))
        special_period_effective_time = "".join(etre.xpath('//td[contains(text(),"专用权期限")]/following-sibling::td[1]//text()'))
        is_co_regist = "".join(etre.xpath('//td[contains(text(),"是否共有商标")]/following-sibling::td[1]//text()'))
        international_later_time = "".join(etre.xpath('//td[contains(text(),"后期指定日期")]/following-sibling::td[1]//text()'))
        international_regist_time = "".join(etre.xpath('//td[contains(text(),"国际注册日期")]/following-sibling::td[1]//text()'))
        priority_date = "".join(etre.xpath('//td[contains(text(),"优先权日期")]/following-sibling::td[1]//text()'))
        agent_name = "".join(etre.xpath('//td[contains(text(),"代理人名称")]/following-sibling::td[1]//text()'))
        color_indication = "".join(etre.xpath('//td[contains(text(),"指定颜色")]/following-sibling::td[1]//text()'))
        trademark_type = "".join(etre.xpath('//td[contains(text(),"商标类型")]/following-sibling::td[1]//text()'))
        form = "".join(etre.xpath('//td[contains(text(),"商标状态")]/following-sibling::td[1]//text()'))

        commodity_num = etre.xpath('//a[contains(text(),"具体核准商品/服务以商标公告为准，点击查看！")]/ancestor::td//table//tr/td[@align="right"]/text()')
        commodity_chinese_name = etre.xpath('//a[contains(text(),"具体核准商品/服务以商标公告为准，点击查看！")]/ancestor::td//table//tr/td[3]/text()')
        lt = []
        for _ in range(len(commodity_num)):
            i = {}
            i["commodity_num"] = commodity_num[_]
            i["commodity_chinese_name"] = commodity_chinese_name[_]
            lt.append(i)

        item = {
            "_id": eval(data)["_id"],
           "regist_num" : regist_num,
           "international_class" : international_class,
           "regist_time" : regist_time,
            "registrant_chinese_name":registrant_chinese_name ,
            "image_url":image_url ,
            "preliminary_notice_num":preliminary_notice_num ,
            "regist_notice_num":regist_notice_num ,
            "preliminary_notice_time":preliminary_notice_time ,
            "regist_notice_time":regist_notice_time ,
            "special_period_effective_time":special_period_effective_time ,
            "international_later_time":international_later_time ,
            "international_regist_time":international_regist_time ,
            "priority_date":priority_date ,
            "color_indication":color_indication ,
            "trademark_type":trademark_type ,
            "form":form ,
            "is_co_regist":is_co_regist,
            "agent_name":agent_name,
            "trademark_commodity_server_info":lt,
            "registrant_foreign_name":registrant_foreign_name ,
            "registrant_foreign_address":registrant_foreign_address ,
        }
        item = BK.item_clear(item=item)

        BK_DATA_info.save(item)
        log.info("数据存入成功。。。。。。。。。。")

test = BK()
test.trade_info()
# test.trade_url_lt(tradeName='蒙昊')

