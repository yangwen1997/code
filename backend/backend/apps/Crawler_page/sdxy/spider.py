'''
@author yangwenlong
@type   spiders
@time   2019/2/10
@file   水滴信用爬虫程序
'''
import sys
import re
import hashlib
sys.path.insert(0,r"D:\bmd\bmd_server")
# from spiders.common import get_log,ABY
from untils.common import get_log,ABY
import requests
from lxml.etree import HTML
from .XPATH import WaterCredit
from datetime import datetime
log = get_log()

import pymongo

MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]


# DB = pymongo.MongoClient(host="127.0.0.1",port=27017)
# dbb = DB["Spider"]["SDXY"]
# red_cli = redis.Redis(host='127.0.0.1',port=6379, db=15)
class Spider(object):
    def __init__(self,key):

        self.url = "https://shuidi.cn/b-search?key={}"
        self.keys = key
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        })
        self.proxy = ABY()
        self.sd_xpath = WaterCredit()

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

    def employeeInfo(self,resp):
        """
        解析主要成员信息
        :param resp:
        :return:
        """
        employeeInfo = self.sd_xpath.employeeInfo(HTML(resp))
        return employeeInfo

    def gsbg(self,resp):
        """
        解析工商变更信息
        :return:
        """
        gsbg = self.sd_xpath.gsbg(HTML(resp))
        return gsbg

    def branchInfo(self,resp):
        """分支机构"""
        branchInfo = self.sd_xpath.branchInfo(HTML(resp))
        return branchInfo

    def annualReports(self,resp):
        """企业年报"""
        annualReports = self.sd_xpath.annualReports(HTML(resp))
        return annualReports

    def investmentInfo(self,resp):
        """对外投资"""
        investmentInfo = self.sd_xpath.investmentInfo(HTML(resp))
        return investmentInfo

    def gxzp(self,resp):
        """关系族谱"""
        relationChartInfo = self.sd_xpath.relationChartInfo(HTML(resp))
        return relationChartInfo

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

        #关系族谱
        # relationChart = self.gxzp(resp)
        # base["relationChart"] = relationChart

        #股东信息计数 股东信息
        holderInfoCount = "".join(etre.xpath('//span[contains(text(),"股东信息")]/following-sibling::span[1]/text()'))
        base["holderInfoCount"] =  '0' if holderInfoCount == '' else holderInfoCount
        gdxx = self.gdxx(resp)
        base["holderInfo"] = gdxx

        # 主要人员计数 主要人员
        employeeInfoCount = "".join(etre.xpath('//span[contains(text(),"主要成员")]/following-sibling::span[1]/text()'))
        base["employeeInfoCount"] = '0' if employeeInfoCount == '' else employeeInfoCount
        employeeInfo = self.employeeInfo(resp)
        base["employeeInfo"] = employeeInfo

        # 工商变更计数  工商变更
        changeInfoCount = "".join(etre.xpath('//span[contains(text(),"变更记录")]/following-sibling::span[1]/text()'))
        base["changeInfoCount"] = '0' if changeInfoCount == '' else changeInfoCount
        gsbg = self.gsbg(resp)
        base["changeInfo"] = gsbg

        #分支机构计数  分支机构
        branchInfoCount = "".join(etre.xpath('//span[contains(text(),"分支机构")]/following-sibling::span[1]/text()'))
        base["branchInfoCount"] = '0' if branchInfoCount == '' else branchInfoCount
        branchInfo = self.branchInfo(resp)
        base["branchInfo"] = branchInfo

        # 企业年报计数 企业年报
        annualReportsCount = "".join(etre.xpath('//span[contains(text(),"企业年报")]/following-sibling::span[1]/text()'))
        lawDangerous["annualReportsCount"] = '0' if annualReportsCount == '' else annualReportsCount
        annualReports = self.annualReports(resp)
        lawDangerous["annualReports"] = annualReports


        items["base"] = base

        # 对外投资计数  对外投资

        correlation = {}
        investmentInfoCount = "".join(etre.xpath('//span[contains(text(),"企业对外投资")]/following-sibling::span[1]/text()'))
        correlation["investmentInfoCount"] = 0 if investmentInfoCount == '' else investmentInfoCount
        investmentInfo = self.investmentInfo(resp)

        correlation["investmentInfo"] = investmentInfo
        lawDangerous["correlation"] = correlation
        items["lawDangerous"] = lawDangerous

    def lawSuitsInfo(self,resp):
        """裁判文书"""
        lawSuitsInfo = self.sd_xpath.lawSuitsInfo(HTML(resp))
        return lawSuitsInfo

    def executedPersonInfo(self,resp):
        """被执行人"""
        executedPersonInfo = self.sd_xpath.executedPersonInfo(HTML(resp))
        return executedPersonInfo

    def courtNoticeInfo(self,resp):
        """开庭公告"""
        courtNoticeInfo = self.sd_xpath.courtNoticeInfo(HTML(resp))
        return courtNoticeInfo

    def noticesInfo(self,resp):
        """法院公告"""
        noticesInfo = self.sd_xpath.noticesInfo(HTML(resp))
        return noticesInfo

    def executionInfo(self,resp):
        """失信信息"""
        executionInfo = self.sd_xpath.executionInfo(HTML(resp))
        return executionInfo

    def abnormalInfo(self,resp):
        """经营异常"""
        abnormalInfo = self.sd_xpath.abnormalInfo(HTML(resp))
        return abnormalInfo

    def equityInfo(self,resp):
        """股权出质"""
        equityInfo = self.sd_xpath.equityInfo(HTML(resp))
        return equityInfo

    def caseInfo(self,resp):
        """立案信息"""
        caseInfo = self.sd_xpath.caseInfo(HTML(resp))
        return caseInfo

    def equityFreezeInfo(self,resp):
        """股权冻结"""
        equityFreezeInfo = self.sd_xpath.equityFreezeInfo(HTML(resp))
        return equityFreezeInfo

    def tddyInfo(self,resp):
        """土地抵押"""
        tddyInfo = self.sd_xpath.tddyInfo(HTML(resp))

        return tddyInfo

    def first_second_page(self,items, resp):
        """风险异常"""
        etre = HTML(resp)

        # 裁判文书计数 裁判文书
        lawSuitsInfoCount = "".join(etre.xpath('//span[contains(text(),"法律诉讼")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["lawSuitsInfoCount"] = '0' if lawSuitsInfoCount == ' ' else lawSuitsInfoCount
        lawSuitsInfo = self.lawSuitsInfo(resp)
        items["lawDangerous"]["lawSuitsInfo"] = lawSuitsInfo

        #被执行人计数 被执行人
        executedPersonInfoCount = "".join(etre.xpath('//span[contains(text(),"被执行人")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["executedPersonInfoCount"] = '0' if executedPersonInfoCount == ' ' else executedPersonInfoCount
        executedPersonInfo = self.executedPersonInfo(resp)
        items["lawDangerous"]["executedPersonInfo"] = executedPersonInfo

        #开庭公告计数 开庭公告
        courtNoticeInfoCount = "".join(etre.xpath('//span[contains(text(),"开庭公告")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["courtNoticeInfoCount"] = '0' if courtNoticeInfoCount == ' ' else courtNoticeInfoCount
        courtNoticeInfo = self.courtNoticeInfo(resp)
        items["lawDangerous"]["courtNoticeInfo"] = courtNoticeInfo

        #法院公告计数 法院公告
        noticesInfoCount = "".join(etre.xpath('//span[contains(text(),"法院公告")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["noticesInfoCount"] = '0' if noticesInfoCount == ' ' else noticesInfoCount
        noticesInfo = self.noticesInfo(resp)
        items["lawDangerous"]["noticesInfo"] = noticesInfo

        #失信信息计数 失信信息
        executionInfoCount = "".join(etre.xpath('//span[contains(text(),"失信被执行")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["executionInfoCount"] = '0' if executionInfoCount == ' ' else executionInfoCount
        executionInfo = self.executionInfo(resp)
        items["lawDangerous"]["executionInfo"] = executionInfo


    def oper_page(self,items, resp):
        """经营异常"""
        etre = HTML(resp)

        # 经营异常计数 经营异常
        abnormalInfoCount = "".join(etre.xpath('//span[contains(text(),"经营异常")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["abnormalInfoCount"] = '0' if abnormalInfoCount == '' else abnormalInfoCount
        abnormalInfo = self.abnormalInfo(resp)
        items["lawDangerous"]["abnormalInfo"] = abnormalInfo

        #股权出质计数 股权出质
        equityInfoCount = "".join(etre.xpath('//span[contains(text(),"股权出质")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["equityInfoCount"] = '0' if equityInfoCount == '' else equityInfoCount
        equityInfo = self.equityInfo(resp)
        items["lawDangerous"]["equityInfo"] = equityInfo

        # 立案信息计数 立案信息
        items["lawDangerous"]["caseInfoCount"] = '0'
        caseInfo = self.caseInfo(resp)
        items["lawDangerous"]["caseInfo"] = caseInfo

        # 股权冻结计数 股权冻结
        items["lawDangerous"]["equityFreezeInfoCount"] = '0'
        equityFreezeInfo = self.equityFreezeInfo(resp)
        items["lawDangerous"]["equityFreezeInfo"] = equityFreezeInfo

        # 土地抵押计数 土地抵押
        items["lawDangerous"]["tddyInfoCount"] = '0'
        tddyInfo = self.tddyInfo(resp)
        items["lawDangerous"]["tddyInfo"] = tddyInfo

    def rzxx(self,resp):
        """
        融资信息
        :return:
        """
        rzxx = self.sd_xpath.rzxx(HTML(resp))
        return rzxx

    def jpxx(self,resp):
        """
        竞品信息
        :return:
        """
        jpxx = self.sd_xpath.jpxx(HTML(resp))
        return jpxx

    def qyyw(self,resp):
        """
        企业业务
        :return:
        """
        qyyw = self.sd_xpath.qyyw(HTML(resp))
        return qyyw
    def coreteam(self,resp):
        """核心团队"""
        coreteam = self.sd_xpath.coreteam(HTML(resp))
        return coreteam
    def base_second_page(self,items,resp):
        """
        解析融资信息页面数据信息
        :param items:
        :param resp:
        :return:
        """
        etre = HTML(resp)

        #  风险信息大类


        # 融资信息计数 融资信息
        development = {}
        financeDataInfoCount = "".join(etre.xpath('//span[contains(text(),"融资历史")]/following-sibling::span[1]/text()'))
        development["financeDataInfoCount"] = '0' if financeDataInfoCount == '' else financeDataInfoCount
        items["lawDangerous"]["development"] = development
        rzxx = self.rzxx(resp)
        items["lawDangerous"]["development"]["financeDataInfo"] = rzxx

        jpxx = self.jpxx(resp)
        items["jpxx"] = jpxx

        qyyw = self.qyyw(resp)
        items["qyyw"] = qyyw

        #核心团队计数
        coreteamCount = "".join(etre.xpath('//span[contains(text(),"核心团队")]/following-sibling::span[1]/text()'))
        coreteamCount = '0' if coreteamCount == '' else coreteamCount
        items["lawDangerous"]["development"]["coreteamCount"] = coreteamCount
        coreteam = self.coreteam(resp)
        items["lawDangerous"]["development"]["coreteamInfo"] = coreteam

    def xzxk(self,resp):
        """
        行政许可 工商局
        :return:
        """
        xzxk = self.sd_xpath.xzxk(HTML(resp))
        return xzxk
    def xzxkxyzg(self,resp):
        """
        行政许可 信用中国
        :param resp:
        :return:
        """
        xzxkxyzg = self.sd_xpath.xzxkxyzg(HTML(resp))
        return xzxkxyzg

    def zpxxinfo(self,resp):
        """招聘信息"""
        zpxxinfo = self.sd_xpath.zpxxinfo(HTML(resp))
        return zpxxinfo

    def taxRating(self,resp):
        """税务评级"""
        taxRating = self.sd_xpath.taxRating(HTML(resp))
        return taxRating
    def wxnum(self,resp):
        """微信公众号"""
        wxnum = self.sd_xpath.wxnum(HTML(resp))
        return wxnum

    def BondInformation(self,resp):
        """债券信息"""
        BondInformation = self.sd_xpath.BondInformation(HTML(resp))
        return BondInformation

    def zzzs(self,resp):
        """
        融资信息
        :return:
        """
        zzzs = self.sd_xpath.zzzs(HTML(resp))
        return zzzs

    def cpxx(self,resp):
        """
        融资信息
        :return:
        """
        cpxx = self.sd_xpath.cpxx(HTML(resp))
        return cpxx

    def wxgz(self,resp):
        """
        融资信息
        :return:
        """
        wxgz = self.sd_xpath.wxgz(HTML(resp))
        return wxgz

    def zbxx(self,resp):
        """
        融资信息
        :return:
        """
        zbxx = self.sd_xpath.zbxx(HTML(resp))
        return zbxx

    def base_three_page(self,items,resp):
        """
        行政许可信息页面数据解析
        :param items:
        :param resp:
        :return:
        """
        etre = HTML(resp)

        # 行政许可计数 行政许可 工商局
        admLicenseInfoCount = "".join(etre.xpath('//span[contains(text(),"行政许可【工商局】")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["admLicenseInfoCount"] = '0' if admLicenseInfoCount == '' else admLicenseInfoCount
        xzxk = self.xzxk(resp)
        items["lawDangerous"]["development"]["admLicenseInfo"] = xzxk

        # 行政许可计数 行政许可 信用中国
        xzxkxyzgCount = "".join(etre.xpath('//span[contains(text(),"行政许可【信用中国】")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["xzxkxyzgCount"] = '0' if xzxkxyzgCount == '' else xzxkxyzgCount
        xzxkxyzg = self.xzxkxyzg(resp)
        items["lawDangerous"]["development"]["xzxkxyzgInfo"] = xzxkxyzg

        # 招聘信息
        zpxxinfoCount = "".join(etre.xpath('//span[contains(text(),"招聘信息")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["zpxxCount"] = '0' if zpxxinfoCount == '' else zpxxinfoCount
        zpxxinfo = self.zpxxinfo(resp)
        items["lawDangerous"]["development"]["zpxxInfo"] = zpxxinfo

        # 税务评级
        taxRatingCount = "".join(etre.xpath('//span[contains(text(),"税务评级")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["taxRatingCount"] = '0' if taxRatingCount == '' else taxRatingCount
        taxRating = self.taxRating(resp)
        items["lawDangerous"]["development"]["taxRatinginfo"] = taxRating

        # 微信公众号
        wxnumCount = "".join(etre.xpath('//span[contains(text(),"税务评级")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["wxnumCount"] = '0' if wxnumCount == '' else wxnumCount
        wxnum = self.wxnum(resp)
        items["lawDangerous"]["development"]["wxnumInfo"] = wxnum

        # 债券信息
        BondInformationCount = "".join(etre.xpath('//span[contains(text(),"债券信息")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["BondInformationCount"] = '0' if BondInformationCount == '' else BondInformationCount
        BondInformation = self.BondInformation(resp)
        items["lawDangerous"]["development"]["BondInformationinfo"] = BondInformation

        # 资质认证计数 资质认证（证书）
        knowledgeProperty = {}
        certificateInfoCount = "".join(etre.xpath('//span[contains(text(),"资质证书")]/following-sibling::span[1]/text()'))
        knowledgeProperty["certificateInfoCount"] = '0' if certificateInfoCount == '' else certificateInfoCount
        items["lawDangerous"]["knowledgeProperty"] = knowledgeProperty
        zzzs = self.zzzs(resp)
        items["lawDangerous"]["knowledgeProperty"]["certificateInfo"] = zzzs

        # 产品信息计数 产品信息
        productInfoCount = "".join(etre.xpath('//span[contains(text(),"产品信息")]/following-sibling::span[1]/text()'))
        items["base"]["productInfoCount"] = '0' if productInfoCount == '' else productInfoCount
        cpxx = self.cpxx(resp)
        items["base"]["productInfo"] = cpxx

        # 招投标计数 招投标
        biddingInfoCount = "".join(etre.xpath('//span[contains(text(),"招投标")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["development"]["biddingInfoCount"] = '0' if biddingInfoCount == '' else biddingInfoCount

        zbxx = self.zbxx(resp)
        items["lawDangerous"]["development"]["biddingInfo"]= zbxx

    def sbxx(self, resp):
        """
        商标信息
        :return:
        """
        sbxx = self.sd_xpath.sbxx(HTML(resp))
        return sbxx

    def zlxx(self, resp):
        """
        专利信息
        :return:
        """
        zlxx = self.sd_xpath.zlxx(HTML(resp))
        return zlxx

    def rjzz(self, resp):
        """
        专利信息
        :return:
        """
        rjzz = self.sd_xpath.rjzz(HTML(resp))
        return rjzz

    def zpzz(self, resp):
        """
        专利信息
        :return:
        """
        zpzz = self.sd_xpath.zpzz(HTML(resp))
        return zpzz

    def pawneeInfo(self,resp):
        """
        质权人
        :param resp:
        :return:
        """
        pawneeInfo = self.sd_xpath.pawneeInfo(HTML(resp))
        return pawneeInfo

    def tdgsInfo(self,resp):
        """地块公示"""
        tdgsInfo = self.sd_xpath.tdgsInfo(HTML(resp))
        return tdgsInfo

    def wzba(self, resp):
        """
        网站备案
        :return:
        """
        wzba = self.sd_xpath.wzba(HTML(resp))
        return wzba

    def base_four_page(self,items, resp):
        """
        解析商标信息页面数据信息
        :param resp:
        :return:
        """
        etre  = HTML(resp)
        # 商标计数 商标
        trademarkInfoCount = "".join(etre.xpath('//span[contains(text(),"商标信息")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["knowledgeProperty"]["trademarkInfoCount"] = '0' if trademarkInfoCount == '' else trademarkInfoCount
        sbxx = self.sbxx(resp)
        items["lawDangerous"]["knowledgeProperty"]["trademarkInfo"] = sbxx

        # 专利信息计数 专利信息
        patentInfoCount = "".join(etre.xpath('//span[contains(text(),"专利信息")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["knowledgeProperty"]["patentInfoCount"] = '0' if patentInfoCount == '' else patentInfoCount
        zlxx = self.zlxx(resp)
        items["lawDangerous"]["knowledgeProperty"]["patentInfo"] = zlxx

        # 软件著作权计数 软件著作权
        copyrightSoftInfoCount = "".join(etre.xpath('//span[contains(text(),"软件著作权")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["knowledgeProperty"]["copyrightSoftInfoCount"] = '0' if copyrightSoftInfoCount == '' else copyrightSoftInfoCount
        rjzz = self.rjzz(resp)
        items["lawDangerous"]["knowledgeProperty"]["copyrightSoftInfo"] = rjzz

        # 作品著作权计数 作品著作权
        copyrightInfoCount = "".join(etre.xpath('//span[contains(text(),"作品著作权")]/following-sibling::span[1]/text()'))
        items["lawDangerous"]["knowledgeProperty"]["copyrightInfoCount"] = '0' if copyrightInfoCount == '' else copyrightInfoCount
        zpzz = self.zpzz(resp)
        items["lawDangerous"]["knowledgeProperty"]["copyrightInfo"] = zpzz

        #质权人计数 质权人
        items["lawDangerous"]["development"]["pawneeInfoCount"] = '0'
        pawneeInfo = self.pawneeInfo(resp)
        items["lawDangerous"]["development"]["pawneeInfo"] = pawneeInfo

        #地块公示计数 地块公示
        items["lawDangerous"]["development"]["tdgsInfoCount"] = '0'
        tdgsInfo = self.tdgsInfo(resp)
        items["lawDangerous"]["development"]["tdgsInfo"] = tdgsInfo

    def sbxq(self,items, resp):
        """
        商标详情
        :return:
        """
        sbxq = self.sd_xpath.sbxq(HTML(resp))

        return sbxq

    def get_req(self,url):

        count = 1
        while count:

            # if proxy:
            try:

                resp = self.s.get(url=url,proxies=self.proxy)
                # resp = self.s.get(url=url,timeout=10)
                resp.encoding = resp.apparent_encoding
                if resp.status_code == 200:
                    return resp

            except Exception as e:

                count += 1
                self.proxy = ABY()
                if self.proxy or count > 3:
                    return "IP无效"
            # else:
            #     return "IP无效"

    def spider(self):
        try:
            url = self.url.format(self.keys)
            resp = self.get_req(url)
            if resp != 'IP无效':
                resp.encoding = "UTF-8"
                etre = HTML(resp.text)
                urls = etre.xpath('//a[@class="or_look"]/@href')
                name = etre.xpath('//div[@class="or_look_tit"]/span/a/@companyname')
                if urls and name:
                    global base_url
                    base_url = urls[0]

                    #指定抓取
                    if name[0] == self.keys:
                            # 全量信息
                        url = "https://shuidi.cn" + urls[0]
                        resp = self.get_req(url)
                        resp.encoding = "UTF-8"
                        items = {}
                        self.base_first_page(items, resp.text,url)
                        try:

                            yc_resps = self.get_req("http://shuidi.cn/company/risk" + base_url.split("?")[0].split("company")[1])
                            self.first_second_page(items, yc_resps.text)

                            oper_resp =  self.get_req("http://shuidi.cn/company/operate" + base_url.split("?")[0].split("company")[1])
                            self.oper_page(items, oper_resp.text)

                            rz_resps = self.get_req("http://shuidi.cn/company/develop" + base_url.split("?")[0].split("company")[1])
                            self.base_second_page(items, rz_resps.text)

                            xk_resps = self.get_req("http://shuidi.cn/company/manage" + base_url.split("?")[0].split("company")[1])
                            self.base_three_page(items, xk_resps.text)

                            sb_resps = self.get_req("http://shuidi.cn/company/property" + base_url.split("?")[0].split("company")[1])
                            self.base_four_page(items, sb_resps.text)
                        # print(items)
                        # log.info("数据存入mongo成功")
                            return items
                        except Exception as e:
                            log.info(e)
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

def start(key):
    """入口程序"""
    # count = 100
    # while count:
    # key = '国家电网有限公司'
    RUN = Spider(key)

    results = RUN.spider()
    if results == "未搜索到公司":
        # item = {}
        # item["company"] = key
        return "未搜索到公司"
    elif results == "公司名不匹配":
        # item = {}
        # item["company"] = key
        return "公司名不匹配"
    elif results == "IP无效":
        # item = {}
        return "IP无效"
    elif results == "页面为空":
        return "页面为空"
    else:
        print(results)
        return results



def main():
    key = "长沙诺美商业策划有限公司"
    # for i in range(1):
    #     t =threading.Thread(target=start,args=(i,))
    #     t.start()
    start()
if __name__ == '__main__':
    main()


