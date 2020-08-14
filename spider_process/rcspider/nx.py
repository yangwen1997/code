

import requests
import hashlib
import json
from rcspider.common import REQ,get_log,ABY,NC_RC
from lxml.etree import HTML


class CQ(REQ):

    def __init__(self):
        """宁夏"""
        super(REQ).__init__()
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        })

        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.baseUrl = 'http://218.95.173.11:8092/portal.php?'
        self.page = 2740
        # self.nextpage = 2
        self.pagecount = 2961


    def spider(self):
        import re
        data = {
            "page": str(self.page),
            "resid": "web_company.quaryPerson",
            "pi_qual_code": "YFTE5BF",
            "rows": "15"
        }
        while self.page <= self.pagecount:
            try:
                resp = self.post_req(self.baseUrl,data=data)

                res = json.loads(resp.text, strict=False)
                for _ in res["data"]:
                    item = {}
                    item["id"] = _["id"]
                    item["fk_corp_id"] = _["fk_corp_id"]
                    try:
                        item["pi_name"] = _["pi_name"]
                    except:
                        item["pi_name"] =""
                    item["pi_corp"] = _["pi_corp"]
                    item["pi_qual_code"] = _["pi_qual_code"]
                    item["pi_qual"] = _["pi_qual"]
                    item["pi_spec"] = _["pi_spec"]

                    _["_id"] = hashlib.md5(_["id"].encode('utf-8')).hexdigest()
                    NC_RC.save(_)
                    self.log.info(f'数据{_["_id"]}存入mongo')

                self.log.info(f'第{self.page}页数据抓取完成')
                self.page += 1
                data["page"] = self.page
            except Exception as e:
                print(e)




st = CQ()

st.spider()