

import requests
import hashlib
from rcspider.common import REQ,get_log,ABY,QH_RC
from lxml.etree import HTML


class QH(REQ):

    def __init__(self):
        """青海"""
        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Cookie": "UM_distinctid=1732868fb4344b-009cfeb9d14544-3a65420e-1fa400-1732868fb443ea; Hm_lvt_03b8714a30a2e110b8a13db120eb6774=1594110837,1594366937,1594602475; regionId=510000; token=3f200f0b24c74429b118d0621bbb28d3; acw_tc=2760825e15946082441805991e19acfd3194ae4680a04bfe334f8ce2aa98eb; CNZZDATA1275173796=34275469-1594106682-%7C1594607048; Hm_lpvt_03b8714a30a2e110b8a13db120eb6774=1594609014"
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseUrl = 'http://139.170.150.135/dataservice/query/staff/list'
        self.page = 9100
        # self.nextpage = 2
        self.pagecount = 16888


    def xpathpages(self,resp):
        """规则解析"""

        etre = HTML(resp)

        trlt = etre.xpath('//tbody//tr')

        try:
            for _ in trlt:
                item = {}
                id = "".join(_.xpath('.//td[1]//text()'))
                item["name"] = "".join(_.xpath('.//td[2]//text()')).strip(" ")
                item["userId"] = "".join(_.xpath('.//td[3]//text()')).strip(" ")
                item["sex"] = "".join(_.xpath('.//td[4]//text()')).strip(" ")
                item["nation"] = "".join(_.xpath('.//td[5]//text()')).strip(" ")
                item["highestEducation"] = "".join(_.xpath('.//td[6]//text()')).strip(" ")
                item["personnelCategory"] = "".join(_.xpath('.//td[7]//text()')).strip(" ")
                item["_id"] = hashlib.md5(id.encode('utf-8')).hexdigest()
                QH_RC.save(item)
                self.log.info(f"数据{item['_id']}存入mongo")
        except Exception as e:
            print(e)
    def spider(self):

        while self.page <= self.pagecount:
            data = {
                "$total": "253092",
                "$reload": "0",
                "$pg": str(self.page),
                "$pgsz": "15",
            }
            resp = self.post_req(self.baseUrl,data=data)
            if resp:
                resp = resp.text.replace("\r","").replace("\t","").replace("\n","")
                self.xpathpages(resp)
                self.log.info(f"第{str(self.page)}页数据抓取完成。。。。。。。。")

                self.page += 1
            else:
                print("IP无效")
st = QH()

st.spider()