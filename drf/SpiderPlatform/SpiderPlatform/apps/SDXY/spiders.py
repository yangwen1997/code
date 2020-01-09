#encoding=utf-8

import requests
from .Xpath import WaterCredit
from lxml.etree import HTML

class Spider(object):
    def __init__(self,key):

        self.url = "https://shuidi.cn/b-search?key={}"
        self.keys = key
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
        })
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
        :return
        """
        gsxx = self.sd_xpath.gdxx(HTML(resp))
        return gsxx

    def gsbg(self,resp):
        """
        解析工商变更信息
        :return:
        """
        gsbg = self.sd_xpath.gsbg(HTML(resp))
        return gsbg

    def base_first_page(self, items, resp):
        """
        解析首页信息
        :param items:
        :param resp:
        :return:
        """
        gsxx = self.gsxx(resp)
        items["公司名"] = self.keys
        items["工商信息"] = gsxx

        gdxx = self.gdxx(resp)
        items["股东信息"] = gdxx

        gsbg = self.gsbg(resp)
        items["工商变更"] = gsbg

    def rzxx(self,resp):
        """
        融资信息
        :return:
        """
        rzxx = self.sd_xpath.rzxx(HTML(resp))
        return rzxx

    def jpxx(self,resp):
        """
        融资信息
        :return:
        """
        jpxx = self.sd_xpath.jpxx(HTML(resp))
        return jpxx

    def qyyw(self,resp):
        """
        融资信息
        :return:
        """
        qyyw = self.sd_xpath.qyyw(HTML(resp))
        return qyyw

    def base_second_page(self,items,resp):
        """
        解析融资信息页面数据信息
        :param items:
        :param resp:
        :return:
        """
        rzxx = self.rzxx(resp)
        items["融资信息"] = rzxx

        jpxx = self.jpxx(resp)
        items["竞品信息"] = jpxx

        qyyw = self.qyyw(resp)
        items["企业业务"] = qyyw

    def xzxk(self,resp):
        """
        融资信息
        :return:
        """
        xzxk = self.sd_xpath.xzxk(HTML(resp))
        return xzxk

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
        xzxk = self.xzxk(resp)
        items["行政许可"] = xzxk

        zzzs = self.zzzs(resp)
        items["资质证书"] = zzzs

        cpxx = self.cpxx(resp)
        items["产品信息"] = cpxx

        wxgz = self.wxgz(resp)
        items["微信公众号"] = wxgz

        zbxx = self.zbxx(resp)
        items["投招标"] = zbxx

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
        sbxx = self.sbxx(resp)
        items["商标信息"] = sbxx

        zlxx = self.zlxx(resp)
        items["专利信息"] = zlxx

        rjzz = self.rjzz(resp)
        items["软件著作权"] = rjzz

        zpzz = self.zpzz(resp)
        items["作品著作权"] = zpzz

        wzba = self.wzba(resp)
        items["网站备案"] = wzba


    def sbxq(self,items, resp):
        """
        商标详情
        :return:
        """
        sbxq = self.sd_xpath.sbxq(HTML(resp))

        return sbxq

    def jbxx_spider(self):

        url = self.url.format(self.keys)
        resp = self.s.get(url)
        resp.encoding = "UTF-8"
        etre = HTML(resp.text)

        urls = etre.xpath('//a[@class="or_look"]/@href')
        names = etre.xpath('//div[@class="or_look_tit"]/span/a/@companyname')
        pageName = None

        index = 0
        for _ in names:
            if _ == self.keys:
                pageName = _
                break
            index += 1

        if pageName:
            url = "https://shuidi.cn" + urls[index]
            resp = self.s.get(url)
            resp.encoding = "UTF-8"
            gsxx = self.gsxx(resp.text)
            return gsxx
        else:
           return  False

    # def spider(self):
    #     try:
    #         url = self.url.format(self.keys)
    #         resp = self.s.get(url)
    #         resp.encoding = "UTF-8"
    #         etre = HTML(resp.text)
    #         urls = etre.xpath('//a[@class="or_look"]/@href')
    #         name = etre.xpath('//div[@class="or_look_tit"]/span/a/@companyname')
    #
    #         global base_url
    #         base_url = urls[0]
    #
    #         url = "https://shuidi.cn" + urls[0]
    #         resp = self.s.get(url)
    #         resp.encoding = "UTF-8"
    #
    #
    #
    #         items = {}
    #         self.base_first_page(items, resp.text)
    #         try:
    #             if items["工商信息"]["法定代表人"] and items["工商信息"]["法定代表人"] != "":
    #                 rz_resps = self.s.get("http://shuidi.cn/company/develop" + base_url.split("?")[0].split("company")[1])
    #                 self.base_second_page(items, rz_resps.text)
    #
    #                 xk_resps = self.s.get("http://shuidi.cn/company/manage" + base_url.split("?")[0].split("company")[1])
    #                 self.base_three_page(items, xk_resps.text)
    #                 print(items)
    #
    #                 sb_resps = self.s.get("http://shuidi.cn/company/property" + base_url.split("?")[0].split("company")[1])
    #                 self.base_four_page(items, sb_resps.text)
    #
    #                 sbxq_lt = items["商标信息"]
    #
    #                 sbxqLt = []
    #                 for sbxq in sbxq_lt:
    #                     sbxq_url = "http://shuidi.cn" + sbxq["详情页面URL"]
    #                     if sbxq_url:
    #                         sbqx_resp = self.s.get(sbxq_url)
    #                         sbxq = self.sbxq(items, sbqx_resp.text)
    #                         sbxqLt.append(sbxq)
    #
    #                 items["商标详情"] = sbxqLt
    #                 items["_id"] = hashlib.md5(str(items["公司名"]).encode("utf-8")).hexdigest()
    #                 print(items)
    #
    #         except Exception as e:
    #             log.info(e)
    #     except Exception as E:
    #         log.info(E)
