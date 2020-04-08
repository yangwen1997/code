'''
@author : yangwenlong
@intro : xpath解析规则
'''



def decorter(lt):
    """使用装饰器为指定的结果进行装饰，节省大量重复编码"""
    def _decorter(fn):
        def wrapper(*args,**kwargs):
            result = fn(*args,**kwargs)
            if result == []:
                item = {}
                for _ in lt:
                    item[_] = "-"
                return item
            else:
                return result
        return wrapper
    return _decorter


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
                filter_item[k] = "-"
        return filter_item

    def gsxx(self,etree):
        """
        工商信息
        :return:
        """
        etre = etree
        item = {}


        # 统一社会信用代码 组织机构代码 注册号 经营状态 所属行业 成立日期 公司类型 营业期限
        item["creditCode"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"企业信用代码")]/following-sibling::td[1]/text()'))
        item.update({"OrganizationCode":"-"})
        item["registerNum"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"工商注册号")]/following-sibling::td[1]/text()'))
        item["businessState"] = "".join(etre.xpath('//table[@class="table1"]//td[contains(text(),"登记状态")]/following-sibling::td[1]/text()'))
        item.update({"industry":"-"})
        item["registerTime"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"成立时间")]/following-sibling::td[1]/text()'))
        item["companyType"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"企业类型")]/following-sibling::td[1]/text()'))
        item["businessTimeout"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"营业期限")]/following-sibling::td[1]/text()'))

        # 法定代表人 发照日期 注册资本 登记机关 企业地址 经营范围
        item["legalMan"] = "".join(etre.xpath('//table[@class="table1"]//a[@class="color444 name-hover"]/text()'))
        item["confirmTime"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"核准日期")]/following-sibling::td[1]/text()'))
        item["registerMoney"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"注册资本")]/following-sibling::td[1]/text()'))
        item["registOrgan"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"登记机关")]/following-sibling::td[1]/text()'))
        item["registerAddress"] = "".join(etre.xpath('//table[@class="table1"][1]//td[contains(text(),"企业地址")]/following-sibling::td[1]/text()'))
        item["businessScope"] = "".join(etre.xpath('//table[@class="table1"][1]//div[@class="overflow"]/text()'))

        filter_item = self.filiters(item)

        return filter_item

    @decorter(["hiType","hiName","hiContribu","hiRealPay"])
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
            #股东类型  股东  认缴出资（金额/时间）  实缴出资（金额/时间）
            item.update({"hiType":"-"})
            item["hiName"] = "".join(_.xpath('.//p[@class="left t4-p1"]//text()|'
                                             './/p[@class="t4-p2"]/span[2]/@title')).replace("查关联企业","").replace("关联企业","").replace(" ","")
            item["hiContribu"] = "".join((_.xpath('.//p[@class="left t4-p2"]/text()|'
                                                  './/p[@class="t4-p4"]//text()')))
            # item["hiRealPay"] = "".join(_.xpath('.//p[@class="left t4-p3"]/text()'))
            item["hiRealPay"] = "".join(_.xpath('.//p[@class="t4-p5"]//text()'))
            filter_item = self.filiters(item)
            gd.append(filter_item)

        return gd

    @decorter(["scPosition","scName"])
    def employeeInfo(self,etree):
        """主要成员"""
        etre = etree
        employeelt = []
        employeeInfo_lt = etre.xpath('//div[@class="member-info"]//ul[@class="clearfix"]/li')
        for _ in employeeInfo_lt:
            item = {}
            # 主要人员职位 主要人员姓名
            item["scPosition"] = "".join(_.xpath('.//p[@class="t3-p3"]//text()'))
            item["scName"] = "".join(_.xpath('.//p[@class="t3-p2"]/span[1]/@title'))
            if item["scPosition"] or item["scName"]:
                filter_item = self.filiters(item)
                employeelt.append(filter_item)
        return employeelt

    @decorter(["changeTime","changeItem","changeBefore","changeAfter"])
    def gsbg(self,etree):
        """
        工商变更
        :param etree:
        :return:
        """
        etre = etree

        gsbg = []
        gdbg_lt =  etre.xpath('//div[@id="m119"]//ul[@class="clearfix"]/li')

        for _ in gdbg_lt:
            item = {}
            # 变更日期 变更事项 变更前 变更后
            item["changeTime"] = "".join(_.xpath('.//p[@class="tm119-p2"]//text()')).replace("变更日期：","")
            item["changeItem"] = "".join((_.xpath('.//p[@class="tm119-p3"]//text()'))).replace("变更项目：","")
            item["changeBefore"] = "".join(_.xpath('.//p[@class="tm119-p4"]//text()')).replace("变更前：","")
            item["changeAfter"] = "".join(_.xpath('.//p[@class="tm119-p5"]//text()')).replace("变更后：","")
            filter_item = self.filiters(item)
            gsbg.append(filter_item)

        return gsbg

    def branchInfo(self,etree):
        """分支机构信息"""
        etre = etree

        branchInfolt = []
        # branchInfo_lt = etre.xpath('//ul[@class="add-bd2 clearfix"]/li')

        # for _ in branchInfo_lt:
        item = {}
        # 分支公司名称 负责人姓名
        item.update({"bCompanyName":"-"})
        item.update({"bName":"-"})
        branchInfolt.append(item)
        return  branchInfolt

    @decorter(["submitAnnual","fillTime"])
    def annualReports(self,etre):
        """企业年报信息"""
        annualReportslt = []
        annualReports_lt = etre.xpath('//div[@class="annual-reports-info"]/div[2]/ul/li')

        for _ in annualReports_lt:
            item = {}

            #报送年度 填报时间
            item["submitAnnual"] = "".join(_.xpath('./div[1]//text()'))
            item["fillTime"] = "".join(_.xpath('./div[2]//text()'))
            filter_item = self.filiters(item)
            annualReportslt.append(item)

        return annualReportslt

    @decorter(["iiCompany","iiName","iiCapital","iiBuild"])
    def investmentInfo(self,etree):
        """对外投资"""
        etre = etree
        investmentInfolt = []
        investmentInfo_lt = etre.xpath('//div[@class="invest-abroad-info"]//li')

        for _ in investmentInfo_lt:
            item = {}
            # 投资公司名 法人 注册资本 成立时间
            item["iiCompany"] = "".join(_.xpath('.//p[1]//text()'))
            item["iiName"] = "".join(_.xpath('.//p[2]/a/text()'))
            item["iiCapital"] = "".join(_.xpath('.//p[3]//text()')).replace("关联企业","").replace(" ","")
            item["iiBuild"] = "".join(_.xpath('.//p[4]//text()'))
            filter_item = self.filiters(item)
            investmentInfolt.append(filter_item)
        return investmentInfolt

    def relationChartInfo(self,etre):
        """关系族谱"""
        relationNodeList1 = []
        relationNodeList2 = []
        relationNodeList3 = []
        List1  = etre.xpath('//div[@class="relation-nodeList1"]/div[@class="relation-node-list"]')
        List2  = etre.xpath('//div[@class="relation-nodeList2"]/div[@class="relation-node-list"]')
        List3  = etre.xpath('//div[@class="relation-nodeList3"]/div[@class="relation-node-list"]')
        for _ in List1:
            item = {}
            item['camepanyName'] = _.xpath('.//text()')
            relationNodeList1.append(item)

        for _ in List2:
            item = {}
            if _.xpath('.//text()') == '更多':
                item['relationName'] = "-"
            else :
                item['relationName'] = _.xpath('.//text()')

            relationNodeList2.append(item)

        for _ in List3:
            item = {}
            if _.xpath('.//text()') == '更多':
                item['camepany'] = "-"
            else:
                item['camepany'] = _.xpath('.//text()')
            relationNodeList3.append(item)
        items = {}
        items["relationNodeList1"] = relationNodeList1
        items["relationNodeList2"] = relationNodeList2
        items["relationNodeList3"] = relationNodeList3
        return items

    @decorter(["cpwsJudgeTime","cpwsIdentity","cpwsName","cpwsResult"])
    def lawSuitsInfo(self,etree):
        """裁判文书"""
        etre = etree
        lawSuitsInfolt = []
        lawSuitsInfo_lt = etre.xpath('//div[@id="m133"]/div/table//tr[1]/following-sibling::tr')
        count = 0
        for _ in lawSuitsInfo_lt:

            item = {}
            # 判决时间 身份 判决书名 判决结果
            item["cpwsJudgeTime"] = "".join(_.xpath('.//td[2]//text()'))
            item["cpwsIdentity"] = "".join(_.xpath('.//td[5]//text()'))
            item["cpwsName"] = "".join(_.xpath('.//td[3]//text()'))
            item["cpwsResult"] = "-"
            filter_item = self.filiters(item)
            lawSuitsInfolt.append(filter_item)
        return lawSuitsInfolt

    @decorter(["zCaseTime","zCaseNum","zTarget","zCourt"])
    def executedPersonInfo(self,etree):
        """被执行人"""
        etre = etree
        executedPersonInfolt = []
        executedPersonInfo_lt = etre.xpath('//div[@id="m137"]//ul[2]/li')
        for _ in executedPersonInfo_lt:
            item = {}
            # 立案时间  案号 执行标的 执行法院
            item["zCaseTime"] =  "".join(_.xpath('.//div[2]//text()'))
            item["zCaseNum"] =  "".join(_.xpath('.//div[4]//text()'))
            item["zTarget"] =  "".join(_.xpath('.//div[3]//text()'))
            item["zCourt"] =  "".join(_.xpath('.//div[5]//text()'))
            filter_item = self.filiters(item)
            executedPersonInfolt.append(filter_item)
        return  executedPersonInfolt

    @decorter(["aLawfulDay","aCaseNum","aCaseReason","aJudge","aAppellor","aDefendant"])
    def courtNoticeInfo(self,etree):
        """开庭公告"""
        etre = etree
        courtNoticeInfolt = []
        courtNoticeInfo_lt = etre.xpath('//table[@class="common_tb court-anno-tb"]//tr[2]')
        for _ in courtNoticeInfo_lt:
            item = {}
            # 开庭日期  案号 案由 审判长/主审人 原告/上诉人 被告/上诉人
            item["aLawfulDay"] = "".join(_.xpath('.//td[2]//text()'))
            item["aCaseNum"] = "".join(_.xpath('.//td[3]//text()'))
            item["aCaseReason"] = "".join(_.xpath('.//td[4]//text()'))
            item["aJudge"] = "-"
            item["aAppellor"] = "".join(_.xpath('.//td[6]//text()'))
            item["aDefendant"] = "".join(_.xpath('.//td[7]//text()'))
            filter_item = self.filiters(item)
            courtNoticeInfolt.append(filter_item)
        return courtNoticeInfolt

    @decorter(["cDate","cType","aDefendant","cJudge","cInfo"])
    def noticesInfo(self,etree):
        """法院公告"""
        etre = etree
        noticesInfolt = []
        noticesInfo_lt = etre.xpath('//div[@id="m134"]//tr[1]/following-sibling::tr')
        for _ in noticesInfo_lt:
            item = {}
            # 发布日期 公告类型 当事人 公告法院 内容
            item["cDate"] = "".join(_.xpath('.//td[2]//text()'))
            item["cType"] = "".join(_.xpath('.//td[5]//text()'))
            item["aDefendant"] = "-"
            item["cJudge"] = "".join(_.xpath('.//td[6]//text()'))
            item["cInfo"] = "-"
            filter_item = self.filiters(item)
            noticesInfolt.append(filter_item)
        return noticesInfolt

    @decorter(["diName","diIdentify","diLowMan","diPublishTime","diCourt","dProvince","diDepend","dFilingDate","diNum","diUnit","diPerform","diDuty","diStatus"])
    def executionInfo(self,etre):
        """失信信息"""
        executionInfolt = []
        executionInfo_lt = etre.xpath('//div[@id="m136"]//ul[2]')
        for _ in executionInfo_lt:
            item = {}
            #被执行人姓名/名称  身份证号码/组织机构代码  法定代表人 发布日期 执行法院 省份 执行依据文号 立案时间 案号
            #做出执行依据单位 被执行人履行情况 生效法律文书确定的义务 失信被执行人为具体情形
            item["diName"] = "-"
            item["diIdentify"] = "-"
            item["diLowMan"] = "-"
            item["diPublishTime"] = "-"
            item["diCourt"] = "".join(_.xpath('./li[1]/div[4]/text()'))
            item["dProvince"] = "".join(_.xpath('./li[1]/div/span/text()'))
            item["diDepend"] = "".join(_.xpath('.//li[2]/div[2]/text()'))
            item["dFilingDate"] = "".join(_.xpath('.//li[2]/div[4]/text()'))
            item["diNum"] = "".join(_.xpath('.//li[1]/div[2]/text()'))
            item["diUnit"] = "".join(_.xpath('.//li[3]/div[2]/text()'))
            item["diPerform"] = "".join(_.xpath('.//li[5]/div[2]/text()'))
            item["diDuty"] = "".join(_.xpath('.//li[4]/div[2]/text()'))
            item["diStatus"] = "".join(_.xpath('.//li[6]/div[2]/text()'))
            filter_item = self.filiters(item)
            executionInfolt.append(filter_item)
        return executionInfolt

    @decorter(["ruInTime","ruSection","ruInCause","ruOutTime","ruOutCause"])
    def abnormalInfo(self,etre):
        """经营异常"""
        abnormalInfolt = []
        abnormalInfo_lt = etre.xpath('//div[@id="m121"]/table//tr[2]')

        for _ in abnormalInfo_lt:
            item = {}
            # 列入日期 做出决定机关 列入经营异常名录原因 移出日期 移出经营异常名录原因
            item["ruInTime"] = "".join(_.xpath('.//td[2]/text()'))
            item["ruSection"] = "".join(_.xpath('.//td[4]/text()'))
            item["ruInCause"] = "".join(_.xpath('.//td[3]/text()'))
            item["ruOutTime"] = "-"
            item["ruOutCause"] = "-"
            filter_item = self.filiters(item)
            abnormalInfolt.append(filter_item)
        return  abnormalInfolt

    @decorter(["eyTime","eyStatus","eyoName","eyoMoneyNum","eyoNum","eyRegisterNum","eyoMan","eyMan","eyNum"])
    def equityInfo(self,etre):
        """股权出质"""
        equityInfolt = []
        equityInfo_lt = etre.xpath('//div[@id="m129"]/table//tr[2]')
        for _ in equityInfo_lt:
            item = {}
            #登记日期 状态 出质人 出质股权数 出质人证件号码 登记编号 标的方 质权人 质权人证件号码
            item["eyTime"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyStatus"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyoName"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyoMoneyNum"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyoNum"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyRegisterNum"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyoMan"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyMan"] = "".join(_.xpath('.//td[3]/text()'))
            item["eyNum"] = "".join(_.xpath('.//td[3]/text()'))
            filter_item = self.filiters(item)
            equityInfolt.append(filter_item)
        return equityInfolt

    def caseInfo(self,etre):
        """立案信息"""
        caseInfolt = []
        item ={}
        # 案号 承办法官 法官助理 立案时间 开庭时间 结束时间 案件状态 原告 被告
        item["caseNum"] = "-"
        item["caseJudge"] = "-"
        item["caseHelper"] = "-"
        item["caseTime"] = "-"
        item["caseOpen"] = "-"
        item["endTime"] = "-"
        item["caseStatus"] = "-"
        item["plaintiff"] = "-"
        item["defendant"] = "-"
        caseInfolt.append(item)
        return caseInfolt

    def equityFreezeInfo(self,etre):
        """股权冻结"""
        equityFreezeInfolt = []
        # equityFreezeInfo_lt = etre.xpath('//div[@id="m129"]/table//tr[2]')
        item = {}
        # 执行法院 执行法院 执行裁定文书号 执行通知文书号 其它投资权益的数额 被执行人证件种类 被执行人证件号码 冻结期限自
        # 冻结期限至 冻结期限 公示日期 失效时间 失效原因
        item["frzCourt"]="-"
        item["frzThings"]="-"
        item["frzExeNum"]="-"
        item["frzNotNum"]="-"
        item["frzPHNum"]="-"
        item["frzType"]="-"
        item["frzCode"]="-"
        item["frzFrom"]="-"
        item["frzTo"]="-"
        item["frzLine"]="-"
        item["frzShowDate"]="-"
        item["frzOutTime"]="-"
        item["frzOutReason"]="-"
        equityFreezeInfolt.append(item)
        return equityFreezeInfolt

    def tddyInfo(self,etre):
        """土地抵押"""
        tddyInfolt = []
        item = {}
        # 土地编号 行政区 土地面积 抵押面积 评估金额 抵押金额 土地位置 抵押土地用途 土地他项权利人证号
        # 土地使用权证号 土地抵押人名称 土地抵押人性质 土地抵押权人 抵押土地权属性质与使用权类型 土地抵押登记起始时间 土地抵押登记结束时间
        item["lmNum"]= "-"
        item["lmArea"]= "-"
        item["lmOcreage"]= "-"
        item["lmAcreage"]= "-"
        item["lmMoney"]= "-"
        item["lmBeMoney"]= "-"
        item["lmLocation"]= "-"
        item["lmUse"]= "-"
        item["lmOtherCode"]= "-"
        item["lmUseCode"]= "-"
        item["lmManName"]= "-"
        item["lmManIdenty"]= "-"
        item["lmMan"]= "-"
        item["lmType"]= "-"
        item["lmFrom"]= "-"
        item["lmTo"]= "-"
        tddyInfolt.append(item)
        return tddyInfolt

    @decorter(["rzGoodsName","rzRank","rzTime","rzNum","rzValue","rzMoney","rzRatio","rzName","rzNews"])
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
            # 产品名称 级别 时间 轮次  估值 金额 比例 投资方 新闻来源
            item["rzGoodsName"] = "-"
            item["rzRank"] = "-"
            item["rzTime"] = "".join(_.xpath('.//td[2]//text()'))
            item["rzNum"] = "".join(_.xpath('.//td[5]//text()'))
            item["rzValue"] = "".join(_.xpath('.//td[6]//text()'))
            item["rzMoney"] = "".join(_.xpath('.//td[4]//text()'))
            item["rzRatio"] = "".join(_.xpath('.//td[7]//text()'))
            item["rzName"] = "".join(_.xpath('.//td[8]//text()'))
            item["rzNews"] = "".join(_.xpath('.//td[9]//text()'))
            filter_item = self.filiters(item)
            rzxx.append(filter_item)
        return rzxx

    @decorter(["roductName","FRound","aluation","stablishDate","roductLabe","erritory","ntr"])
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
            # 产品名称 当前融资轮次 估值 成立日期 产品标签 所属地 简介
            item["productName"] = "".join(_.xpath('.//td[2]/text()'))
            item["CFRound"] = "".join((_.xpath('.//td[4]/text()')))
            item["valuation"] = "-"
            item["establishDate"] = "".join(_.xpath('.//td[7]/text()'))
            item["productLabe"] = "".join(_.xpath('.//td[5]/text()'))
            item["territory"] = "".join(_.xpath('.//td[3]/text()'))
            item["Intr"] = "".join(_.xpath('.//td[6]/text()'))
            filter_item = self.filiters(item)
            jpxx.append(filter_item)

        return jpxx

    @decorter(["productName","establishDate","CFRound","productLabe","territory","productIntr"])
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
            # 产品名称 成立日期 当前融资轮次 产品标签 所属地 产品介绍
            item["productName"] = "".join(_.xpath('.//td[2]/text()'))
            item["establishDate"] = "-"
            item["CFRound"] = "-"
            item["productLabe"] = "".join(_.xpath('.//td[3]/text()'))
            item["territory"] = "-"
            item["productIntr"] = "".join(_.xpath('.//td[4]/text()'))
            filter_item = self.filiters(item)
            qyyw.append(filter_item)

        return qyyw

    @decorter(["Name", "position", "introd"])
    def coreteam(self,etre):
        """核心团队"""

        coreteam = []
        coreteam_lt = etre.xpath('//div[@id="m166"]//tr[1]/following-sibling::tr')

        for _ in coreteam_lt:
            item = {}
            # 许可文件编号 许可文件名称 有效期自 有效期至 许可机关 许可内容
            item["Name"] = "".join(_.xpath('.//td[2]/text()'))
            item["position"] = "".join(_.xpath('.//td[3]/text()'))
            item["introd"] = "".join(_.xpath('.//td[4]/text()'))
            filter_item = self.filiters(item)
            coreteam.append(filter_item)

        return coreteam

    @decorter(["gsLicenceNum","gsLicenceName","gsDeadlineStart","gsDeadlineEnd","gsOrgan","gsInfo"])
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
            # 许可文件编号 许可文件名称 有效期自 有效期至 许可机关 许可内容
            item["gsLicenceNum"] = "".join(_.xpath('.//td[2]/text()'))
            item["gsLicenceName"] = "".join(_.xpath('.//td[3]/text()'))
            item["gsDeadlineStart"] = "".join(_.xpath('.//td[4]/text()'))
            item["gsDeadlineEnd"] = "".join(_.xpath('.//td[5]/text()'))
            item["gsOrgan"] = "".join(_.xpath('.//td[6]/text()'))
            item["gsInfo"] = "".join(_.xpath('.//td[7]/text()'))
            filter_item = self.filiters(item)
            xzxk.append(filter_item)

        return xzxk

    @decorter(['AdministrativeLicense ','LicensingAuthority','ApprovalDecisionDate'])
    def xzxkxyzg(self,etre):
        """
        行政许可 信用中国
        :param etree:
        :return:
        """
        xzxkxyzg = []
        xzxkxyzg_lt = etre.xpath('//div[@id="m152"]//tr[1]/following-sibling::tr')

        for _ in xzxkxyzg_lt:
            item = {}
            # 行政许可书文编号 许可决定机关 许可决定日期
            item["AdministrativeLicense "] = "".join(_.xpath('.//td[2]/text()'))
            item["LicensingAuthority"] = "".join(_.xpath('.//td[3]/text()'))
            item["ApprovalDecisionDate"] = "".join(_.xpath('.//td[4]/text()'))
            filter_item = self.filiters(item)
            xzxkxyzg.append(filter_item)
        return xzxkxyzg

    @decorter(['releaseDate','position','salary','Education','experience','region'])
    def zpxxinfo(self,etre):
        """招聘信息"""
        zpxxinfo = []

        zpxxinfo_lt = etre.xpath('//div[@id="n151"]//tr[1]/following-sibling::tr')

        for _ in zpxxinfo_lt:
            item = {}
            # 发布日期  招聘岗位 月薪 学历 工作经营 地区
            item["releaseDate"] = "".join(_.xpath('.//td[2]/text()'))
            item["position"] = "".join(_.xpath('.//td[3]/text()'))
            item["salary"] = "".join(_.xpath('.//td[4]/text()'))
            item["Education"] = "".join(_.xpath('.//td[5]/text()'))
            item["experience"] = "".join(_.xpath('.//td[6]/text()'))
            item["region"] = "".join(_.xpath('.//td[7]/text()'))
            filter_item = self.filiters(item)
            zpxxinfo.append(filter_item)
        return zpxxinfo

    @decorter(['appraisalYear','creditLevel','type','number','Company'])
    def taxRating(self,etre):
        """税务评级"""
        taxRating = []

        taxRating_lt = etre.xpath('//div[@id="m153"]//tr[1]/following-sibling::tr')

        for _ in taxRating_lt:
            item = {}
            # 评价年度  纳税人信用级别 类型 纳税人识别号 评价单位
            item["appraisalYear"] = "".join(_.xpath('.//td[2]/text()'))
            item["creditLevel"] = "".join(_.xpath('.//td[3]/text()'))
            item["type"] = "".join(_.xpath('.//td[4]/text()'))
            item["number"] = "".join(_.xpath('.//td[5]/text()'))
            item["Company"] = "".join(_.xpath('.//td[6]/text()'))

            filter_item = self.filiters(item)
            taxRating.append(filter_item)
        return taxRating

    @decorter(['wxgznum','wxnum','intro'])
    def wxnum(self,etre):
        """微信公众号"""
        wxnum = []

        wxnum_lt = etre.xpath('//div[@id="n1512"]//tr[1]/following-sibling::tr')

        for _ in wxnum_lt:
            item = {}
            # 微信公众号  微信 简介
            item["wxgznum"] = "".join(_.xpath('.//td[2]/text()'))
            item["wxnum"] = "".join(_.xpath('.//td[3]/text()'))
            item["intro"] = "".join(_.xpath('.//td[5]/text()'))
            filter_item = self.filiters(item)
            wxnum.append(filter_item)
        return wxnum

    @decorter(['IssueDate','NameBond','BondCode','BondCode','BondType','LatestRating'])
    def BondInformation(self,etre):
        """债券信息"""
        BondInformation = []

        BondInformation_lt = etre.xpath('//div[@id="n1516"]//tr[1]/following-sibling::tr')

        for _ in BondInformation_lt:
            item = {}
            # 发行日期 债券名称 债券代码 债券类型 最新评级
            item["IssueDate"] = "".join(_.xpath('.//td[2]/text()'))
            item["NameBond"] = "".join(_.xpath('.//td[3]/text()'))
            item["BondCode"] = "".join(_.xpath('.//td[4]/text()'))
            item["BondType"] = "".join(_.xpath('.//td[5]/text()'))
            item["LatestRating"] = "".join(_.xpath('.//td[6]/text()'))
            filter_item = self.filiters(item)
            BondInformation.append(filter_item)
        return BondInformation

    @decorter(["certiDate","certiType","certiEndTime","certiNum","ceriStatus","certiMore"])
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
            # 发证日期  证书类别 截止日期 证书编号 状态 备注
            item["certiDate"] = "".join(_.xpath('.//td[4]/text()'))
            item["certiType"] = "".join(_.xpath('.//td[2]/text()'))
            item["certiEndTime"] = "".join(_.xpath('.//td[5]/text()'))
            item["certiNum"] = "".join(_.xpath('.//td[3]/text()'))
            item["ceriStatus"] = "-"
            item["certiMore"] = "-"

            filter_item = self.filiters(item)
            zzzs.append(filter_item)

        return zzzs

    @decorter(["pAllName","pName","pClassify","pField","pDescribe"])
    def cpxx(self,etree):
        """
        解析行产品信息信息
        :param etree:
        :return:
        """
        etre = etree

        cpxx = []
        cpxx_lt = etre.xpath('//div[@id="n1511"]//tr[1]/following-sibling::tr')

        for _ in cpxx_lt:
            item = {}

            # 产品名称 产品简称 产品分类 领域 描述
            item["pAllName"] = "".join(_.xpath('.//td[2]/text()'))
            item["pName"] = "".join(_.xpath('.//td[3]/text()'))
            item["pClassify"] = "".join(_.xpath('.//td[4]/text()'))
            item["pField"] = "".join(_.xpath('.//td[5]/text()'))
            item["pDescribe"] = "".join(_.xpath('.//td[6]/text()'))
            filter_item = self.filiters(item)

            # 产品图片 图片url 图片名称
            pImage ={}
            pImage["piUrl"] = "https:" + str("".join(_.xpath('.//td[2]/img/@src')))
            pImage["piName"] = item["pAllName"]
            item["pImage"] = pImage

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

    @decorter(["bPublishTime","bTitle","bMan","bArea","bClassify"])
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
            # 发布时间 标题(描述) 采购人 所属地区 项目分类
            item["bPublishTime"] = "".join(_.xpath('.//td[2]/text()'))
            item["bTitle"] = "".join(_.xpath('.//td[3]/text()'))
            item["bMan"] = "".join(_.xpath('.//td[4]/text()'))
            item["bArea"] = "-"
            item["bClassify"] = "-"
            filter_item = self.filiters(item)
            zbxx.append(filter_item)

        return zbxx

    @decorter(["tmName","tmRegisterNum","tmStatus","tmClassify","tmApplyTime","tmDeadline","tmSection",
               "tmAnnounceNum","tmAnnounceDate","tmrAnnounceNum","tmrAnnounceDate","tmApplyMan","tmApplyAddres",
               "tmGoodsService","tmApplyFlow"])
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
            # 商标名称 注册号 状态 国际分类 申请时间 专用权期限 代理机构 初审公告号 初审公告日期 注册公告号 注册公告日期
            #  申请人 申请地址 商品服务列表 申请流程
            item["tmName"] = "".join(_.xpath('.//td[4]/text()'))
            item["tmRegisterNum"] = "".join(_.xpath('.//td[5]//img/@src'))
            item["tmStatus"] = "".join(_.xpath('.//td[7]/text()'))
            item["tmClassify"] = "".join(_.xpath('.//td[6]/text()'))
            item["tmApplyTime"] = "".join(_.xpath('.//td[2]/text()'))
            item["tmDeadline"] = "-"
            item["tmSection"] = "-"
            item["tmAnnounceNum"] = "-"
            item["tmAnnounceDate"] = "-"
            item["tmrAnnounceNum"] = "-"
            item["tmrAnnounceDate"] = "-"
            item["tmApplyMan"] = "-"
            item["tmApplyAddres"] = "-"
            item["tmGoodsService"] = "-"
            item["tmApplyFlow"] = "-"
            # item["详情页面URL"] = "".join(_.xpath('.//td[8]/a/@href'))
            filter_item = self.filiters(item)
            sbxx.append(filter_item)

        return sbxx

    @decorter(["piType","piApplyPublishNum","piApplyAnnounceDate","piInventName","piDetails"])
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
            # 类型 申请公布号 申请公布日期 发明名称 详情信息
            item["piType"] = "".join(_.xpath('.//td[7]/text()'))
            item["piApplyPublishNum"] = "".join(_.xpath('.//td[5]//text()'))
            item["piApplyAnnounceDate"] = "".join(_.xpath('.//td[2]/text()'))
            item["piInventName"] = "".join(_.xpath('.//td[3]/text()'))
            item["piDetails"] = "-"
            filter_item = self.filiters(item)
            zlxx.append(filter_item)

        return zlxx

    @decorter(["swAllName","swName","swregisterNum","swClassifyNum","swVersionNum","swOwner","swPublishDate","swRegisterDate"])
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
            # 软件全称  软件简称 登记号 分类号 版本号 著作权人(国籍) 首次发表日期 登记日期
            item["swAllName"] = "".join(_.xpath('.//td[3]/text()'))
            item["swName"] = "".join(_.xpath('.//td[4]//text()'))
            item["swregisterNum"] = "".join(_.xpath('.//td[5]/text()'))
            item["swClassifyNum"] = "".join(_.xpath('.//td[6]/text()'))
            item["swVersionNum"] = "".join(_.xpath('.//td[7]/text()'))
            item["swOwner"] = "-"
            item["swPublishDate"] = "-"
            item["swRegisterDate"] = "-"

            filter_item = self.filiters(item)
            rjzz.append(filter_item)

        return rjzz

    @decorter(["pwName","pwregisterNum","pwCategory","pwFinishDate","pwRegisterDate","pwPublishDate"])
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
            # 作品名称 登记号 类别 创作完成日期 登记日期 首次发布日期
            item["pwName"] = "".join(_.xpath('.//td[2]/text()'))
            item["pwregisterNum"] = "".join(_.xpath('.//td[3]//text()'))
            item["pwCategory"] = "".join(_.xpath('.//td[4]/text()'))
            item["pwFinishDate"] = "".join(_.xpath('.//td[5]/text()'))
            item["pwRegisterDate"] = "".join(_.xpath('.//td[6]/text()'))
            item["pwPublishDate"] = "".join(_.xpath('.//td[7]/text()'))

            filter_item = self.filiters(item)
            rjzz.append(filter_item)

        return rjzz

    @decorter(["eyRegisterNum","eyStatus","eyoName","eyoMoneyNum","eyoMan","eyMan","eyNum","eyTime","eMore"])
    def pawneeInfo(self,etre):
        """质权人"""
        pawneeInfolt = []
        item = {}

        # 登记编号 状态 出质人 出质股权数 出质人证件号码 质权人 质权人证件号码 登记日期 备注
        item["eyRegisterNum"]= "-"
        item["eyStatus"]= "-"
        item["eyoName"]= "-"
        item["eyoMoneyNum"]= "-"
        item["eyoMan"]= "-"
        item["eyMan"]= "-"
        item["eyNum"]= "-"
        item["eyTime"]= "-"
        item["eMore"]= "-"
        pawneeInfolt.append(item)
        return pawneeInfolt

    @decorter(["elecNum","signDate","district","lArea","lSource","lLevel","dealPrive","useLife","class","location",
               "pName","lUse","lUseMan","approUnit","supplyWay","agreeDeliveryTime","agreeStartTime","actualStartTime",
               "agreeCompleTime","actualCompleTime","agreeMaxVolume","agreeMinVolume"])
    def tdgsInfo(self,etre):
        """地块公式"""
        tdgsInfo = []
        item = {}
        # 电子监管号 签订日期 土地面积 行政区 土地来源 土地级别 成交价格 使用年限 行业分类 土地位置 项目名称
        # 土地用途 土地使用权人 批准单位 供地方式 约定交地时间 约定开工时间 实际开工时间 约定竣工时间 实际竣工时间 约定容积率上限 约定容积率下限
        item["elecNum"] = "-"
        item["signDate"]= "-"
        item["district"]= "-"
        item["lArea"]= "-"
        item["lSource"]= "-"
        item["lLevel"]= "-"
        item["dealPrive"]= "-"
        item["useLife"]= "-"
        item["class"]= "-"
        item["location"]= "-"
        item["pName"]= "-"
        item["lUse"]= "-"
        item["lUseMan"]= "-"
        item["approUnit"]= "-"
        item["supplyWay"]= "-"
        item["agreeDeliveryTime"]= "-"
        item["agreeStartTime"]= "-"
        item["actualStartTime"]= "-"
        item["agreeCompleTime"]= "-"
        item["actualCompleTime"]= "-"
        item["agreeMaxVolume"]= "-"
        item["agreeMinVolume"]= "-"
        tdgsInfo.append(item)
        return tdgsInfo

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
