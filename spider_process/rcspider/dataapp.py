'''
author yang wen long
'''

import requests
import hashlib
from rcspider.common import REQ,get_log,ABY,gzszj
from lxml.etree import HTML


class DAtaAPP(REQ):

    def __init__(self):
        """贵州"""

        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie": "UM_distinctid=1732868fb4344b-009cfeb9d14544-3a65420e-1fa400-1732868fb443ea; Hm_lvt_03b8714a30a2e110b8a13db120eb6774=1594110837,1594366937,1594602475; regionId=510000; token=3f200f0b24c74429b118d0621bbb28d3; acw_tc=2760825e15946082441805991e19acfd3194ae4680a04bfe334f8ce2aa98eb; CNZZDATA1275173796=34275469-1594106682-%7C1594607048; Hm_lpvt_03b8714a30a2e110b8a13db120eb6774=1594609014"
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseUrl = 'http://220.197.219.123:88/Web/dataapp/per_dataResult.aspx'
        self.page = 1
        self.nextpage = 2
        self.pagecount = 2653

    def page_xpath(self,resp):
        """列表页面解析规则"""
        etre = HTML(resp)

        date_lt = etre.xpath('//tr[@class="resultTable_h"]//following-sibling::tr')
        for _ in date_lt:
            item = {}
            item["name"] = "".join(_.xpath(".//td[2]/text()"))
            item["company"] = "".join(_.xpath(".//td[3]/text()"))
            item["major"] = "".join(_.xpath(".//td[4]/text()"))
            item["reg_number"] = "".join(_.xpath(".//td[5]/text()"))
            item["time"] = "".join(_.xpath(".//td[6]/text()"))
            item["_id"] = hashlib.md5((item["name"] + item["reg_number"]).encode('utf-8')).hexdigest()
            gzszj.save(item)
            self.log.info(f"数据{item['_id']}存入mongo成功。。。。。。。。")

    def spider(self):
        resp = self.get_req(self.baseUrl)
        etre = HTML(resp.text.replace("\n","").replace("\r","").replace("\t",""))
        self.page_xpath(resp.text.replace("\n","").replace("\r","").replace("\t",""))
        __VIEWSTATE = "".join(etre.xpath('//input[@name="__VIEWSTATE"]/@value'))

        date = {
            "__VIEWSTATE" : __VIEWSTATE,
            "__VIEWSTATEGENERATOR": "836E111D",
            "__EVENTTARGET" : "Pager1",
            "__EVENTARGUMENT": str(self.nextpage),
            "ent_n" : "",
            "per_n" : "",
            "per_Code" : "",
            "per_Style" :"0",
            "Pager1_input" : str(self.page),

        }
        while self.pagecount > self.nextpage:
            resp = self.post_req(self.baseUrl,data=date)

            etre = HTML(resp.text.replace("\n", "").replace("\r", "").replace("\t", ""))
            self.page_xpath(resp.text.replace("\n", "").replace("\r", "").replace("\t", ""))
            __VIEWSTATE = "".join(etre.xpath('//input[@name="__VIEWSTATE"]/@value'))
            date["__VIEWSTATE"] = __VIEWSTATE
            self.log.info(f"第{self.page}页数据抓取完成")
            self.page += 1; self.nextpage +=1
            date["Pager1_input"] = str(self.page)
            date["__EVENTARGUMENT"] = str(self.nextpage)

st = DAtaAPP()

st.spider()