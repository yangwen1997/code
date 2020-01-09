# encoding=utf-8
'''
@author :   yangwenlong
@file   :   xpath.py
@inter  :  企查查规则解析模块
'''
import time
from lxml.etree import HTML
from datetime import datetime


class QCC_XPATH(object):

    def __init__(self,resp,keys):
        # self.resp = resp
        self.etre = HTML(resp)
        self.keys = keys

    def gsxx(self):
        '''
        工商信息
        '''
        try:
            dict = {}
            # 统一社会信用代码 企业名  组织机构代码 工商注册号 经营状态 所属行业 法人 注册资本  成立日期
            dict["companyName"] = "".join(self.etre.xpath('//div[@class="company-name"]/text()')).replace('\n',"").replace(" ","")
            dict["creditCode"] = ''.join(self.etre.xpath('//div[contains(text(),"统一社会信用代码")]/following-sibling::div/text()'))
            dict["organizationCode"]  = "".join(self.etre.xpath('//div[contains(text(),"组织机构代码")]/following-sibling::div/text()'))
            dict["registerNum"] = "".join(self.etre.xpath('//div[contains(text(),"工商注册号")]/following-sibling::div/text()'))
            dict["businessState"] = "".join(self.etre.xpath('//div[contains(text(),"登记状态")]/following-sibling::div/text()'))
            dict["industry"] = "".join(self.etre.xpath('//div[contains(text(),"所属行业")]/following-sibling::div/text()'))
            dict["legalMan"] = "".join(self.etre.xpath('//div[@class="pull-left"]//div[contains(text(),"法定代表人")]/following-sibling::div/a/text()'))
            dict["registerMoney"] = "".join(self.etre.xpath('//table[@class="info-table"]//tr[3]//div[contains(text(),"注册资本")]/following-sibling::div/text()'))
            dict["registerTime"] = "".join(self.etre.xpath('//div[contains(text(),"成立日期")]/following-sibling::div/text()'))
           #  登记机关 核准日期 营业期限 企业类型 企业地址 经营范围 人员规模 参保人数
            dict["registOrgan"] = "".join(self.etre.xpath('//div[contains(text(),"登记机关")]/following-sibling::div/text()'))
            dict["confirmTime"] = "".join(self.etre.xpath('//div[contains(text(),"核准日期")]/following-sibling::div/text()'))
            dict["businessTimeout"] = "".join(self.etre.xpath('//div[contains(text(),"营业期限")]/following-sibling::div/text()'))
            dict["companyType"] = "".join(self.etre.xpath('//div[contains(text(),"企业类型")]/following-sibling::div/text()'))
            dict["registerAddress"] = "".join(self.etre.xpath('//div[contains(text(),"企业地址")]/following-sibling::div/text()'))
            dict["businessScope"] = "".join(self.etre.xpath('//div[contains(text(),"经营范围")]/following-sibling::div/text()'))
            dict["personnelScale"] = "".join(self.etre.xpath('//div[contains(text(),"人员规模")]/following-sibling::div/text()'))
            dict["insuredPersons"] = "".join(self.etre.xpath('//div[contains(text(),"参保人数")]/following-sibling::div/text()'))

            # 曾用名 经营方式 来源网站
            dict["usedName"] = None
            dict["operation"] = "".join(self.etre.xpath('//div[contains(text(),"经营方式")]/following-sibling::div/text()'))
            dict["websource"] = 'https://qichacha.com'
            dict["storageTime"] = datetime.now()
            return dict
        except Exception as e:
            print(e)

