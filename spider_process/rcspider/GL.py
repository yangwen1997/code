

import requests
import hashlib
from rcspider.common import REQ,get_log,ABY,GL_RC
from lxml.etree import HTML


class CQ(REQ):

    def __init__(self):
        """吉林"""
        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseUrl = 'http://cx.jlsjsxxw.com/UserInfo/CertifiedEngineers.aspx'
        self.page = 1
        # self.nextpage = 2
        self.pagecount = 25862


    def xpathpages(self,resp):
        """规则解析"""

        etre = HTML(resp)

        trlt = etre.xpath('//table[@class="employee_list table_list"]/tbody/tr')

        try:
            for _ in trlt:
                item = {}
                id = "".join(_.xpath('.//td[1]//text()')).strip(" ")
                item["name"] = "".join(_.xpath('.//td[2]//text()')).strip(" ")
                item["IdentificationNumber"] = "".join(_.xpath('.//td[3]//text()')).strip(" ")
                item["PersonnelType"] = "".join(_.xpath('.//td[4]//text()')).strip(" ")
                item["company"] = "".join(_.xpath('.//td[5]//text()')).strip(" ")
                item["_id"] = hashlib.md5((id).encode('utf-8')).hexdigest()
                GL_RC.save(item)
                self.log.info(f"数据{item['_id']}存入mongo")
        except Exception as e:
            print(e)
    def spider(self):
        while 1:
            res = self.get_req(self.baseUrl)
            if res:
                ETRE = HTML(res.text)
                __VIEWSTATE = "".join(ETRE.xpath('//input[@name="__VIEWSTATE"]/@value'))
                __EVENTVALIDATION = "".join(ETRE.xpath('//input[@name="__EVENTVALIDATION"]/@value'))
                action = "".join(ETRE.xpath('//form[@id="form1"]/@action'))
                self.baseUrl = "http://cx.jlsjsxxw.com/UserInfo/"  + action
                cok = res.headers["Set-Cookie"]
                self.s.headers.update({
                    "Cookie":cok,
                    "Referer":self.baseUrl,
                })
                data = {
                    "__EVENTTARGET": "Linkbutton5",
                    "__EVENTARGUMENT": "",
                    "__VIEWSTATE":__VIEWSTATE,
                    "__EVENTVALIDATION":__EVENTVALIDATION,
                    "txtPersonName":"",
                    "ddlSpecialty":"",
                    "txtIDCard":"",
                    "txtCorpName":"",
                    "newpage":str(self.page),

                }

                while self.page <= self.pagecount:

                    resp = self.post_req(self.baseUrl,data=data)
                    if resp:
                        resp = resp.text.replace("\r", "").replace("\t", "").replace("\n", "")
                        ETRE = HTML(resp)
                        self.xpathpages(resp)
                        self.log.info(f"第{str(self.page)}页数据抓取完成。。。。。。。。")

                        __VIEWSTATE = "".join(ETRE.xpath('//input[@name="__VIEWSTATE"]/@value'))
                        __EVENTVALIDATION = "".join(ETRE.xpath('//input[@name="__EVENTVALIDATION"]/@value'))

                        data["__EVENTVALIDATION"] = __EVENTVALIDATION
                        self.page += 1
                        data["newpage"] = str(self.page)
                    else:
                        print("IP无效")

                break


st = CQ()

st.spider()