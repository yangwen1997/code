

import requests
import hashlib
from rcspider.common import REQ,get_log,ABY,CQ_RC
from lxml.etree import HTML


class CQ(REQ):

    def __init__(self):
        """重庆"""
        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie": "UM_distinctid=1732868fb4344b-009cfeb9d14544-3a65420e-1fa400-1732868fb443ea; Hm_lvt_03b8714a30a2e110b8a13db120eb6774=1594110837,1594366937,1594602475; regionId=510000; token=3f200f0b24c74429b118d0621bbb28d3; acw_tc=2760825e15946082441805991e19acfd3194ae4680a04bfe334f8ce2aa98eb; CNZZDATA1275173796=34275469-1594106682-%7C1594607048; Hm_lpvt_03b8714a30a2e110b8a13db120eb6774=1594609014"
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseUrl = 'http://183.66.171.75:88/CQCollect/Ry_Query/zcjzs/Wright_List.aspx'
        self.page = 3
        # self.nextpage = 2
        self.pagecount = 1695


    def xpathpages(self,resp):
        """规则解析"""

        etre = HTML(resp)

        trlt = etre.xpath('//tr[@bgcolor="#00CCFF"]/following-sibling::tr')

        try:
            for _ in trlt:
                item = {}
                item["name"] = "".join(_.xpath('.//td[1]//text()')).strip(" ")
                item["sex"] = "".join(_.xpath('.//td[2]//text()')).strip(" ")
                item["qualifications"] = "".join(_.xpath('.//td[3]//text()')).strip(" ")
                item["leval"] = "".join(_.xpath('.//td[4]//text()')).strip(" ")
                item["company"] = "".join(_.xpath('.//td[6]//text()')).strip(" ")
                item["area"] = "".join(_.xpath('.//td[7]//text()')).strip(" ")
                item["_id"] = hashlib.md5((item["name"] + item["area"] + item["leval"] ).encode('utf-8')).hexdigest()
                CQ_RC.save(item)
                self.log.info(f"数据{item['_id']}存入mongo")
        except Exception as e:
            print(e)
    def spider(self):
        while 1:
            res = self.get_req(self.baseUrl)
            if res:
                ETRE = HTML(res.text)
                __VIEWSTATE = "".join(ETRE.xpath('//input[@name="__VIEWSTATE"]/@value'))
                data = {
                    "__EVENTTARGET":"",
                    "__EVENTARGUMENT": "",
                    "__VIEWSTATE":__VIEWSTATE,
                    "FName":"",
                    "FBaseinfoName":"",
                    "FManageDeptID": "-1",
                    "FLevel": "0",
                    "FQualiNumber":"",
                    "FNumber": "",
                    "FIsWright": "-1",
                    "Pager1:NewPage": str(self.page),
                    "Pager1:BT_Go.x": "8",
                    "Pager1:BT_Go.y": "9",
                }

                while self.page <= self.pagecount:

                    resp = self.post_req(self.baseUrl,data=data)
                    if resp:
                        resp = resp.text.replace("\r", "").replace("\t", "").replace("\n", "")
                        ETRE = HTML(resp)
                        self.xpathpages(resp)
                        self.log.info(f"第{str(self.page)}页数据抓取完成。。。。。。。。")

                        __VIEWSTATE = "".join(ETRE.xpath('//input[@name="__VIEWSTATE"]/@value'))
                        data["__VIEWSTATE"] = __VIEWSTATE
                        self.page += 1
                        data["Pager1:NewPage"] = str(self.page)
                    else:
                        print("IP无效")

                break


st = CQ()

st.spider()