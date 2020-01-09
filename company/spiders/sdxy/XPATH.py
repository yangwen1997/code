'''
@author : yangwenlong
@intro : xpath解析规则
'''

class WaterCredit(object):
    """
    水滴信用规则解析类
    """
    def __init__(self):
        pass

    @staticmethod
    def filiters(item:dict):
        """
        item 数据过滤器
        :return:
        """
        filter_item = {}
        for k,v in item.items():
            if v:
                filter_item[k] = v.replace("\r","").replace("\n","").replace("\t","").replace("\xa0","").replace("\u0000","").strip(" ")
            else:
                filter_item[k] = v
        return filter_item

    def gsxx(self,etree):
        """
        工商信息
        :return:
        """
        etre = etree
        item = {}
        item["法定代表人"] = "".join(etre.xpath('//table[@class="table1"]//a[@class="color444 name-hover"]/text()'))
        item["注册资本"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"注册资本")]/following-sibling::td[1]/text()'))
        item["经营状态"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"登记状态")]/following-sibling::td[1]/text()'))
        item["实缴资本"] = None
        item["成立日期"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"成立时间")]/following-sibling::td[1]/text()'))
        item["统一社会信用代码"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"企业信用代码")]/following-sibling::td[1]/text()'))
        item["纳税人识别号"] = None
        item["注册号"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"工商注册号")]/following-sibling::td[1]/text()'))
        item["组织机构代码"] = None
        item["企业类型"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"企业类型")]/following-sibling::td[1]/text()'))
        item["所属行业"] = None
        item["核准日期"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"核准日期")]/following-sibling::td[1]/text()'))
        item["登记机关"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"登记机关")]/following-sibling::td[1]/text()'))
        item["英文名"] = None
        item["曾用名"] = None
        item["参保人数"] = None
        item["人员规模"] = None
        item["营业期限"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"营业期限")]/following-sibling::td[1]/text()'))
        item["企业地址"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"企业地址")]/following-sibling::td[1]/text()'))
        item["经营范围"] = "".join(etre.xpath('//table[@class="table1"]//div[@class="overflow"]/text()'))
        filter_item = self.filiters(item)

        return filter_item

    def gdxx(self,etree):
        """
        股东信息
        :return:
        """
        etre = etree
        gd = []
        gd_lt = etre.xpath('//div[@class="partner-info"]//ul[@class="clearfix"]/li')
        count = 0
        for _ in gd_lt:
            item = {}
            item["股东"] = "".join(_.xpath('.//p[@class="left t4-p1"]//text()')).replace("查关联企业","").replace("关联企业","").replace(" ","")
            item["持股比例"] = "".join((_.xpath('.//p[@class="left t4-p4"]/text()')))
            item["认缴出资额(万)"] = "".join(_.xpath('.//p[@class="left t4-p2"]/text()'))
            filter_item = self.filiters(item)
            gd.append(filter_item)

        return gd

    def gsbg(self,etree):
        """
        工商变更
        :param etree:
        :return:
        """
        etre = etree

        gsbg = []
        gdbg_lt =  etre.xpath('//div[@id="m119"]//ul/li')

        for _ in gdbg_lt:
            item = {}
            item["变更日期"] = "".join(_.xpath('.//div[2]/p[@class="up-el"]/text()')).replace("变更日期：","")
            item["变更事项"] = "".join((_.xpath('.//div[1]/p[@class="up-el"]/text()'))).replace("变更项目：","")
            item["变更前"] = "".join(_.xpath('.//div[1]/p[2]/text()')).replace("变更前：","")
            item["变更后"] = "".join(_.xpath('.//div[2]/p[2]/text()')).replace("变更后：","")
            filter_item = self.filiters(item)
            gsbg.append(filter_item)

        return gsbg

    def rzxx(self,etree):
        """
        解析融资信息
        :param etree:
        :return:
        """

        etre = etree

        rzxx = []
        rzxx_lt = etre.xpath('//div[@id="m122"]//tr[1]/following-sibling::tr')

        count = 0
        for _ in rzxx_lt:
            count += 1
            item = {}
            item["融资时间"] = "".join(_.xpath('.//td[2]/text()'))
            item["融资轮次"] = "".join((_.xpath('.//td[5]/text()')))
            item["融资金额"] = "".join(_.xpath('.//td[4]/text()'))
            item["投资方"] = "".join(_.xpath('.//td[8]/text()'))
            filter_item = self.filiters(item)
            rzxx.append(filter_item)

        return rzxx

    def jpxx(self,etree):
        """
        解析竞品信息
        :param etree:
        :return:
        """
        etre = etree

        jpxx = []
        jpxx_lt = etre.xpath('//div[@id="m165"]//tr[1]/following-sibling::tr')

        for _ in jpxx_lt:
            item = {}
            item["产品名称"] = "".join(_.xpath('.//td[2]/text()'))
            item["当前融资轮次"] = "".join((_.xpath('.//td[4]/text()')))
            item["估值"] = None
            item["成立日期"] = "".join(_.xpath('.//td[7]/text()'))
            item["产品标签"] = "".join(_.xpath('.//td[5]/text()'))
            item["所属地"] = "".join(_.xpath('.//td[3]/text()'))
            item["简介"] = "".join(_.xpath('.//td[6]/text()'))
            filter_item = self.filiters(item)
            jpxx.append(filter_item)

        return jpxx

    def qyyw(self,etree):
        """
        解析企业业务信息
        :param etree:
        :return:
        """
        etre = etree

        qyyw = []
        qyyw_lt = etre.xpath('//div[@id="n161"]//tr[1]/following-sibling::tr')

        for _ in qyyw_lt:
            item = {}
            item["产品名称"] = "".join(_.xpath('.//td[2]/text()'))
            item["成立日期"] = None
            item["当前融资轮次"] = None
            item["产品标签"] = "".join(_.xpath('.//td[3]/text()'))
            item["所属地"] = None
            item["产品介绍"] = "".join(_.xpath('.//td[4]/text()'))
            filter_item = self.filiters(item)
            qyyw.append(filter_item)

        return qyyw

    def xzxk(self,etree):
        """
        解析行政许可信息
        :param etree:
        :return:
        """
        etre = etree

        xzxk = []
        xzxk_lt = etre.xpath('//div[@id="m151"]//tr[1]/following-sibling::tr')

        for _ in xzxk_lt:
            item = {}
            item["许可文书编号"] = "".join(_.xpath('.//td[2]/text()'))
            item["许可文件"] = "".join(_.xpath('.//td[3]/text()'))
            item["有效期自"] = "".join(_.xpath('.//td[4]/text()'))
            item["有效期至"] = "".join(_.xpath('.//td[5]/text()'))
            item["许可机关"] = "".join(_.xpath('.//td[6]/text()'))
            item["许可内容"] = "".join(_.xpath('.//td[7]/text()'))
            filter_item = self.filiters(item)
            xzxk.append(filter_item)

        return xzxk

    def zzzs(self,etree):
        """
        解析行资质证书信息
        :param etree:
        :return:
        """
        etre = etree

        zzzs = []
        zzzs_lt = etre.xpath('//div[@id="n159"]//tr[1]/following-sibling::tr')

        for _ in zzzs_lt:
            item = {}
            item["发证日期"] = "".join(_.xpath('.//td[4]/text()'))
            item["证书类型"] = "".join(_.xpath('.//td[2]/text()'))
            item["截至日期"] = "".join(_.xpath('.//td[5]/text()'))
            item["操作"] = None
            filter_item = self.filiters(item)
            zzzs.append(filter_item)

        return zzzs

    def cpxx(self,etree):
        """
        解析行产品信息信息
        :param etree:
        :return:
        """
        etre = etree

        cpxx = []
        cpxx_lt = etre.xpath('///div[@id="n1511"]//tr[1]/following-sibling::tr')

        for _ in cpxx_lt:
            item = {}
            item["产品名称"] = "".join(_.xpath('.//td[2]/text()'))
            item["产品简介"] = "".join(_.xpath('.//td[3]/text()'))
            item["产品分类"] = "".join(_.xpath('.//td[4]/text()'))
            item["领域"] = "".join(_.xpath('.//td[5]/text()'))
            item["操作"] = "".join(_.xpath('.//td[6]/text()'))
            filter_item = self.filiters(item)
            cpxx.append(filter_item)

        return cpxx

    def wxgz(self,etree):
        """
        解析行微信公众号信息
        :param etree:
        :return:
        """
        etre = etree

        wxgz = []
        wxgz_lt = etre.xpath('//div[@id="n1512"]//tr[1]/following-sibling::tr')

        for _ in wxgz_lt:
            item = {}
            item["微信公众号"] = "".join(_.xpath('.//td[2]/text()'))
            item["微信号"] = "".join(_.xpath('.//td[3]/text()'))
            item["二维码"] = "http:" + "".join(_.xpath('.//td[4]//img/@src'))
            item["简介"] = "".join(_.xpath('.//td[5]/text()'))

            filter_item = self.filiters(item)
            wxgz.append(filter_item)

        return wxgz

    def zbxx(self,etree):
        """
        解析行招标信息
        :param etree:
        :return:
        """
        etre = etree

        zbxx = []
        zbxx_lt = etre.xpath('//div[@id="m126"]//tr[1]/following-sibling::tr')

        for _ in zbxx_lt:
            item = {}
            item["发布日期"] = "".join(_.xpath('.//td[2]/text()'))
            item["标题"] = "".join(_.xpath('.//td[3]/text()'))
            item["采购人"] = "".join(_.xpath('.//td[4]/text()'))
            filter_item = self.filiters(item)
            zbxx.append(filter_item)

        return zbxx

    def sbxx(self,etree):
        """
        解析商标信息
        :param etree:
        :return:
        """
        etre = etree

        sbxx = []
        sbxx_lt = etre.xpath('//div[@id="m141"]//tr[1]/following-sibling::tr')

        for _ in sbxx_lt:
            item = {}
            item["申请日期"] = "".join(_.xpath('.//td[2]/text()'))
            item["商标"] = "".join(_.xpath('.//td[3]//img/@src'))
            item["商标名称"] = "".join(_.xpath('.//td[4]/text()'))
            item["注册号"] = "".join(_.xpath('.//td[5]/text()'))
            item["国际分类"] = "".join(_.xpath('.//td[6]/text()'))
            item["商标状态"] = "".join(_.xpath('.//td[7]/text()'))
            item["详情页面URL"] = "".join(_.xpath('.//td[8]/a/@href'))
            filter_item = self.filiters(item)
            sbxx.append(filter_item)

        return sbxx

    def zlxx(self,etree):
        """
        解析专利信息
        :param etree:
        :return:
        """
        etre = etree

        zlxx = []
        zlxx_lt = etre.xpath('//div[@id="m142"]//tr[1]/following-sibling::tr')

        for _ in zlxx_lt:
            item = {}
            item["申请公布日"] = "".join(_.xpath('.//td[2]/text()'))
            item["专利名称"] = "".join(_.xpath('.//td[3]//text()'))
            item["专利类型"] = "".join(_.xpath('.//td[6]/text()'))

            filter_item = self.filiters(item)
            zlxx.append(filter_item)

        return zlxx

    def rjzz(self,etree):
        """
        解析软件著作权信息
        :param etree:
        :return:
        """
        etre = etree

        rjzz = []
        rjzz_lt = etre.xpath('//div[@id="m144"]//tr[1]/following-sibling::tr')

        for _ in rjzz_lt:
            item = {}
            item["登记批准日期"] = "".join(_.xpath('.//td[2]/text()'))
            item["软件全称"] = "".join(_.xpath('.//td[3]//text()'))
            item["软件简称"] = "".join(_.xpath('.//td[4]/text()'))
            item["分类号"] = "".join(_.xpath('.//td[6]/text()'))

            filter_item = self.filiters(item)
            rjzz.append(filter_item)

        return rjzz

    def zpzz(self,etree):
        """
        解析作品著作权信息
        :param etree:
        :return:
        """
        etre = etree

        rjzz = []
        rjzz_lt = etre.xpath('//div[@id="m143"]//tr[1]/following-sibling::tr')

        for _ in rjzz_lt:
            item = {}
            item["作品名称"] = "".join(_.xpath('.//td[2]/text()'))
            item["作品类别"] = "".join(_.xpath('.//td[4]//text()'))
            item["创作完成日期"] = "".join(_.xpath('.//td[5]/text()'))
            item["登记日期"] = "".join(_.xpath('.//td[6]/text()'))
            item["首次发表日期"] = "".join(_.xpath('.//td[7]/text()'))

            filter_item = self.filiters(item)
            rjzz.append(filter_item)

        return rjzz

    def wzba(self,etree):
        """
        解析网站备案信息
        :param etree:
        :return:
        """
        etre = etree

        rjzz = []
        rjzz_lt = etre.xpath('//div[@id="n141"]//tr[1]/following-sibling::tr')

        for _ in rjzz_lt:
            item = {}
            item["审核日期"] = "".join(_.xpath('.//td[2]/text()'))
            item["网站名称"] = "".join(_.xpath('.//td[3]//text()'))
            item["网站首页"] = "".join(_.xpath('.//td[4]/text()'))

            filter_item = self.filiters(item)
            rjzz.append(filter_item)

        return rjzz

    def sbxq(self,etree):
        """
        解析商标详情页面信息
        :param etree:
        :return:
        """
        etre = etree
        item = {}

        item["商标名称"] = "".join(etre.xpath('//td[contains(text(),"商标名称")]/following-sibling::td[1]//text()'))
        item["申请日期"] = "".join(etre.xpath('//td[contains(text(),"申请日期")]/following-sibling::td[1]/text()'))
        item["申请/注册号"] = "".join(etre.xpath('//td[contains(text(),"申请/注册号")]/following-sibling::td[1]/text()'))
        item["国际分类"] = "".join(etre.xpath('//td[contains(text(),"国际分类")]/following-sibling::td[1]/text()'))
        item["申请人名称(中文)"] = "".join(etre.xpath('//td[contains(text(),"申请人名称（中文）")]/following-sibling::td[1]//text()'))
        item["申请人名称(英文)"] = "".join(etre.xpath('//td[contains(text(),"申请人名称（英文）")]/following-sibling::td[1]//text()'))
        item["申请人地址(中文)"] = "".join(etre.xpath('//td[contains(text(),"申请人地址（中文）")]/following-sibling::td[1]//text()'))
        item["申请人地址(英文)"] = "".join(etre.xpath('//td[contains(text(),"申请人名称（英文）")]/following-sibling::td[1]//text()'))
        item["初审公告期号"] = "".join(etre.xpath('//td[contains(text(),"初审公告期号")]/following-sibling::td[1]//text()'))
        item["初审公告日期"] = "".join(etre.xpath('//td[contains(text(),"初审公告日期")]/following-sibling::td[1]//text()'))
        item["注册公告期号"] = "".join(etre.xpath('//td[contains(text(),"注册公告期号")]/following-sibling::td[1]//text()'))
        item["注册公告日期"] = "".join(etre.xpath('//td[contains(text(),"注册公告日期")]/following-sibling::td[1]//text()'))
        item["是否共有商标"] = "".join(etre.xpath('//td[contains(text(),"是否共有商标")]/following-sibling::td[1]//text()'))
        item["商标类型"] = "".join(etre.xpath('//td[contains(text(),"商标类型")]/following-sibling::td[1]//text()'))
        item["专用权期限"] = "".join(etre.xpath('//td[contains(text(),"专用权期限")]/following-sibling::td[1]//text()'))
        item["商标形式"] = "".join(etre.xpath('//td[contains(text(),"商标形式")]/following-sibling::td[1]//text()'))
        item["国际注册日期"] = "".join(etre.xpath('//td[contains(text(),"国际注册日期")]/following-sibling::td[1]//text()'))
        item["后期指定日期"] = "".join(etre.xpath('//td[contains(text(),"后期指定日期")]/following-sibling::td[1]//text()'))
        item["优先权日期"] = "".join(etre.xpath('//td[contains(text(),"优先权日期")]/following-sibling::td[1]//text()'))
        item["代理/办理机构"] = "".join(etre.xpath('//td[contains(text(),"代理/办理机构")]/following-sibling::td[1]//text()'))
        item["商品服务"] = ",".join(etre.xpath('//td[contains(text(),"商品/服务")]/following-sibling::td[1]//text()')).replace(" ","")
        item["商标流程状态"] = "-".join(etre.xpath('//td[contains(text(),"商标流程")]/following-sibling::td[1]//text()')).replace(" ","")
        filter_item = self.filiters(item)
        # rjzz.append(filter_item)

        return filter_item
