# http://110.16.70.26/nmjgpublisher/UserInfo/CertifiedEngineersObtain.aspx







import requests
import hashlib
import time
import json
from rcspider.common import REQ,get_log,ABY,NMG_RC
from lxml.etree import HTML


class CQ(REQ):

    def __init__(self):
        """内蒙古"""
        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseUrl = 'http://110.16.70.26/nmjgpublisher/handle/ProjectsInfoHandler.ashx'
        self.page = 1
        # self.nextpage = 2
        self.pagecount = 273


    def xpathpages(self,resp):
        """规则解析"""

        # etre = HTML(resp)

        # trlt = etre.xpath('//tbody[@id="acBody"]/tr')

        try:
            for _ in resp:
                item = {}
                item["number"] = _["number"]
                item["IDCards"] = _["IDCards"]
                item["PersonName"] = _["PersonName"]
                item["IDCard"] = _["IDCard"]
                item["RowGuid"] = _["RowGuid"]
                item["CorpName"] = _["CorpName"]
                item["SPECIALTYPENAME"] = _["SPECIALTYPENAME"]
                item["_id"] = hashlib.md5(str(item["number"]).encode('utf-8')).hexdigest()
                NMG_RC.save(item)
                self.log.info(f"数据{item['_id']}存入mongo")
        except Exception as e:
            print(e)
    def spider(self):

        ti = int(time.time() * 1000)
        data = f"?type=UserInfo&lblPageCount=273&lblPageIndex={self.page}&lblRowsCount=5445&lblPageSize=20&PersonName=&Specialty=&IDCard=&CorpName=&_={ti}"
        while self.page <= self.pagecount:

            url = self.baseUrl + data
            resp = self.get_req(url)
            if resp:
                res = json.loads(resp.text, strict=False)["datainfo"]
                self.xpathpages(res)
                self.log.info(f"第{str(self.page)}页数据抓取完成。。。。。。。。")
                self.page += 1
                ti = int(time.time() * 1000)
                data = f"?type=UserInfo&lblPageCount=273&lblPageIndex={self.page}&lblRowsCount=5445&lblPageSize=20&PersonName=&Specialty=&IDCard=&CorpName=&_={ti}"

            else:
                print("IP无效")

st = CQ()

st.spider()