#encoding=utf-8
import requests
import time
import random
import hashlib
import pymongo
import re
from lxml.etree import HTML
# 四川 arerid:25  中标类型：infoType

MOGO = pymongo.MongoClient(host="172.16.75.28",port=27017)
YFB_pageLT = MOGO["YANG"]["YFB_pageLT"]
YFB_dateHtml = MOGO["YANG"]["YFB_dateHtml"]
YFB_dateinfo_all = MOGO["YANG"]["YFB_dateinfo_all"]
YFB_dateinfo = MOGO["YANG"]["YFB_dateinfo"]

class yfb(object):

    def __init__(self):
        self.baseUrl = 'https://weixin.qianlima.com/qlmYFB/yfb_new/indexSeach.do'
        self.dateInfoUrl = "https://weixin.qianlima.com/qlmYFB/yfb/getZBDetail.do"
        self.currPage = 6
        self.data = {
            "openid": "oFNc6sx4Emv7QpqO_Jgmv5EluhMc",
            "isPayArea": "false",
            "currPage": str(self.currPage),
            "timeType": "1",
            "type": "3",
            "keywords": "",
            "areaId": "25",
            "isSem": "false",
            "logid": "",
            "infoType": "2",
            "filtermode	": "1",
            "startTime": "",
            "zbDyKeyword": "",
            "matchMode": "",
            "count": "",
            "needCount": "",
            "idsNotInclude": "",
            "isParticiple": "true",
            "isDefaultTimeType": "true",
            "chooseArea": "false",
            "noticeType": "",
            "isZhongBiao": "true",
            "showPeerWateched": "false",
            "startDate": "",
            "endDate": "",
        }
        self.infoData = {
            "openid": "oFNc6sx4Emv7QpqO_Jgmv5EluhMc",
            "mobanid": "",
            "dengji": "1",
            "contentid": "190171821",
            "type": "0",
            "isFromInformation": "false",
            "areaId": "2087",
        }
        self.s = requests.session()
        self.s.headers.update({
            "Cookie": "__jsluid_h=423877fbc9600a60a6b64e4cf1b6cbd0; __jsluid_s=d0e3441345deaf7dd3c86c33e2f02e6a",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat"
        })

    def dateLT_spider(self):
        """抓取数据列表
        :param 17459 :该网站的数据的总条数 每页10条,总共1746页
        """
        # count = 17459
        count = 20
        while self.currPage <= count:
            try:
                resp = self.s.post(url= self.baseUrl ,data=self.data)
                resp.encoding = resp.apparent_encoding
                datejson = resp.json()
                dateLT = datejson["resultList"]
                for i in dateLT:
                    item = i
                    item["_id"] = hashlib.md5(str(i["contentid"]).encode("utf-8")).hexdigest()
                    print(f"{item['contentid']}")
                    YFB_pageLT.save(item)

                self.currPage += 1
                self.data["currPage"] = str(self.currPage)
                time.sleep(random.randint(1,6))
                print(f"第{self.currPage}页数据抓取完成")
            except Exception as e:
                print(e)

    def dateinfo_spider(self):
        """抓取数据详情页面"""

        # result = YFB_pageLT.find({"flag":{"$exists":False}}).limit(500)
        result = YFB_pageLT.find({"flag":{"$exists":False}}).limit(100)

        for _ in result:
            try:
                self.infoData["contentid"] = _["contentid"]

                # self.infoData["contentid"] = "190262345"
                self.infoData["areaId"] = _["areaId"]
                # self.infoData["areaId"] = "2094"
                resp = self.s.post(url=self.dateInfoUrl, data=self.infoData)
                resp.encoding = 'utf-8'
                item = resp.json()
                item["_id"] = _["_id"]

                if item["contentid"]:
                    YFB_dateHtml.save(item)
                    YFB_pageLT.find_one_and_update({"_id": _["_id"]}, {"$set": {"flag": "1"}})
                    print(f"数据{item['_id']}详情入库完成。。。。。")
                    time.sleep(random.randint(1, 6))
                else:
                    print("error")


            except Exception as e:
                print(e)

    def page_xpath(self):
        """解析页面的数据"""
        # result = YFB_dateHtml.find({"flag":{"$exists":False}}).limit(500)
        result = YFB_dateHtml.find()

        try:
            count = 1
            for i in result:
                if i["content"]:
                    etree = HTML(i["content"])

                    zb_hxr_lt = etree.xpath('//th[contains(text(),"中标候选人及排序")]/ancestor::tr/ancestor::table/following-sibling::table[1]/following-sibling::table')
                    if zb_hxr_lt:
                        # 中标信息 ，项目负责人  技术负责人
                        zb_lt = []
                        for x in zb_hxr_lt:
                            item = {}
                            if "".join(x.xpath('.//tr[2]/th[1]//text()')) == "职务":
                                item["中标公司"] = "".join(x.xpath(".//tr[1]//text()"))
                                ProjectLeaderItems = {}
                                TechnicalDirectorItems = {}

                                # 项目负责人
                                ProjectLeaderItems["项目负责人"] = "".join(x.xpath(".//tr[4]//td[2]//text()"))
                                ProjectLeaderItems["证书名称"] = "".join(x.xpath(".//tr[4]//td[3]//text()"))
                                ProjectLeaderItems["证书编号"] = "".join(x.xpath(".//tr[4]//td[4]//text()"))
                                ProjectLeaderItems["职称专业"] = "".join(x.xpath(".//tr[4]//td[5]//text()"))
                                ProjectLeaderItems["级别"] = "".join(x.xpath(".//tr[4]//td[6]//text()"))

                                # 项目技术负责人
                                TechnicalDirectorItems["项目技术负责人"] = "".join(x.xpath(".//tr[4]//td[2]//text()"))
                                TechnicalDirectorItems["证书名称"] = "".join(x.xpath(".//tr[4]//td[3]//text()"))
                                TechnicalDirectorItems["证书编号"] = "".join(x.xpath(".//tr[4]//td[4]//text()"))
                                TechnicalDirectorItems["职称专业"] = "".join(x.xpath(".//tr[4]//td[5]//text()"))
                                TechnicalDirectorItems["级别"] = "".join(x.xpath(".//tr[4]//td[6]//text()"))

                                item["项目负责人信息"] = ProjectLeaderItems; item["项目技术负责人信息"] = TechnicalDirectorItems
                                zb_lt.append(item)
                            else:
                                pass
                        # 投标人名称
                        wzb_lt = etree.xpath('//th[contains(text(),"投标人名称")]/ancestor::tr/following-sibling::tr')
                        wzbDate_lt = []
                        for _ in wzb_lt:
                            items = {}
                            items["投标人名称"] = "".join(_.xpath("./th[1]/text()"))
                            items["失败原因"] = "".join(_.xpath("./th[3]/text()"))
                            if items["投标人名称"] and  items["失败原因"]:
                                wzbDate_lt.append(items)

                        if zb_lt or wzbDate_lt:
                            dateItem = {};dateItem["中标信息"] = zb_lt;dateItem["未中标信息"] = wzbDate_lt
                            dateItem["_id"] = i["_id"]
                            YFB_dateinfo_all.save(dateItem)

                        else:
                            if "中标候选人及排序" in i["content"]:
                                etre = HTML(i["content"])
                                table_lt = etre.xpath('//table');del table_lt[0];del table_lt[-1];del table_lt[-1]
                                companyLt = table_lt[0].xpath(".//tr"); del companyLt[0]

                                project = table_lt[1].xpath(".//td[contains(text(),'项目负责人')]/ancestor::tr")
                                major = table_lt[1].xpath(".//td[contains(text(),'项目技术负责人')]/ancestor::tr")

                                zb_lt = []
                                for _ in range(len(companyLt)):
                                    item ={}; ProjectLeaderItems ={};TechnicalDirectorItems = {}
                                    item["中标候选人名称"] = "".join(companyLt[_].xpath(".//td[1]/text()"))
                                    ProjectLeaderItems["项目负责人"] = "".join(project[_].xpath(".//td[2]/text()"))
                                    ProjectLeaderItems["证书名称"] = "".join(project[_].xpath(".//td[3]/text()"))
                                    ProjectLeaderItems["证书编号"] = "".join(project[_].xpath(".//td[4]/text()"))
                                    ProjectLeaderItems["职称专业"] = "".join(project[_].xpath(".//td[5]/text()"))
                                    ProjectLeaderItems["级别"] = "".join(project[_].xpath(".//td[6]/text()"))

                                    TechnicalDirectorItems["项目技术负责人"] = "".join(major[_].xpath(".//td[2]/text()"))
                                    TechnicalDirectorItems["证书名称"] = "".join(major[_].xpath(".//td[3]/text()"))
                                    TechnicalDirectorItems["证书编号"] = "".join(major[_].xpath(".//td[4]/text()"))
                                    TechnicalDirectorItems["职称专业"] = "".join(major[_].xpath(".//td[5]/text()"))
                                    TechnicalDirectorItems["级别"] = "".join(major[_].xpath(".//td[6]/text()"))

                                    item["项目负责人信息"] = ProjectLeaderItems; item["项目技术负责人信息"] = TechnicalDirectorItems
                                    zb_lt.append(item)

                                dateItem = {}
                                dateItem["中标信息"] = zb_lt
                                dateItem["_id"] = i["_id"]
                                YFB_dateinfo_all.save(dateItem)

                    else:
                        # dateItem:最后的结果 ；comLt : 公司的列表
                        dateItem = {}; dateItem["_id"] = i["_id"];comLt = []

                        if "采购人名称" in i["content"] or "供应商名称" in i["content"] or "采购项目名称" in i["content"]:
                            count += 1
                        else:
                            # 第二种情况
                            if "结果公示" in i["content"] and "成交候选人名称" in i["content"] and "附件" in i["content"]:
                                companyNameLT = re.findall(r"<p>第.候选人：(.*?)</p>",i["content"])

                                if companyNameLT:
                                    for _ in companyNameLT:
                                        item = {};item["公司名称"] = _
                                        comLt.append(item)
                                    dateItem["content"] = comLt
                                    YFB_dateinfo.save(dateItem)
                                else:
                                    count += 1


                            elif "中标候选单位" in i["content"] and "标包名称" in i["content"] and "中标单位名称" in i["content"] \
                                    and "中标候选人名次" in i["content"] and "发布时间" in i["content"]:
                                etre = HTML(i["content"]); tr_lt = etre.xpath('//tr')

                                if len(tr_lt) >= 4 :
                                    # 第三种
                                    for i in range(len(tr_lt)):
                                        if len(tr_lt) - i == len(tr_lt) or len(tr_lt) - i == 1 or len(tr_lt) - i == 2:
                                            continue
                                        else:
                                            item = {}
                                            item["公司名称"] = "".join(tr_lt[i].xpath('.//td[2]/text()'))
                                            comLt.append(item)
                                    dateItem["content"] = comLt
                                    YFB_dateinfo.save(dateItem)

                                else:
                                    # 第四种
                                    for i in range(len(tr_lt)):
                                        if len(tr_lt) - i == len(tr_lt) :
                                            continue
                                        else:
                                            item = {}
                                            item["公司名称"] = "".join(tr_lt[i].xpath('.//td[2]/text()'))
                                            comLt.append(item)

                                            dateItem["content"] = comLt
                                            YFB_dateinfo.save(dateItem)

                            elif "中选单位" in i["content"]:
                                # 第五种
                                companyNameLT = re.findall(r"<p>一、中选单位：(.*?)</p>",i["content"])
                                if companyNameLT:
                                    for _ in companyNameLT:
                                        item = {};item["公司名称"] = _
                                        comLt.append(item)
                                    dateItem["content"] = comLt
                                    YFB_dateinfo.save(dateItem)
                                else:
                                    count += 1

                            elif "中标单位" in i["content"] and "中标详情" in i["content"]:

                                # 第六种
                                etre = HTML(i["content"]); item = {}
                                item["公司名称"] =  "".join(etre.xpath('//div[contains(text(),"中标详情")]/following-sibling::div[1]/div[2]/div/div[2]/text()'))
                                comLt.append(item)
                                dateItem["content"] = comLt
                                YFB_dateinfo.save(dateItem)

                            elif "中介服务机构" in i["content"]:
                                # 第七种
                                companyNameLT = re.findall(r'target="_blank">(.*?)</a> \(下浮比例',i["content"])
                                if companyNameLT:
                                    for _ in companyNameLT:
                                        item = {}
                                        item["公司名称"] = _
                                        comLt.append(item)
                                    dateItem["content"] = comLt
                                    YFB_dateinfo.save(dateItem)
                                else:
                                    count += 1

                            else:
                                count += 1
                else:
                    count += 1


            print(f"共{count}条数据没有解析出来数据")
        except Exception as e:
            print(e)

    def delmogo(self):
        '''
        删除无效的数据
        :return:
        '''
        result = YFB_dateHtml.find()
        for _ in result:
            if _["contentid"]:
                print("sucess")
            else:
                YFB_dateHtml.delete_one(_)

    def companys(self):
        """提取公司名称"""
        result = YFB_dateinfo_all.find()

        result_lt = []
        for _ in result:
            for x in _["中标信息"]:
                item = {}
                try:
                    company = x["中标公司"].split("（")[1].strip("） ")
                except:
                    company = x["中标候选人名称"].strip(" ")

                if company != "无" and company:
                    item["company"] = company
                    result_lt.append(item)

            if "未中标信息" in _.keys():
                for q in _["未中标信息"]:
                    item = {}
                    company = q["投标人名称"].strip(" ")
                    if company != "无" and company:
                        item["company"] = company
                        result_lt.append(item)

        result = YFB_dateinfo.find()

        for _ in result:
            for x in _["content"]:
                item = {}
                item["company"] = x["公司名称"]
                result_lt.append(item)

        import csv

        header = ["公司名"]
        path = 'E:\code\spider\spider_process\MT\cd.csv'
        with open(path, 'a', newline='', encoding='utf-8') as fp:
            f_csv = csv.DictWriter(fp, header)

            roew = []
            for _ in result_lt:
                item = {}
                try:
                    item["公司名"] = _["company"]
                except:
                    item["公司名"] = ""

                roew.append(item)
            f_csv.writeheader()
            f_csv.writerows(roew)
        print(result_lt)



st = yfb()
st.dateinfo_spider()