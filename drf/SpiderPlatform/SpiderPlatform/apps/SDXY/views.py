#encoding=utf-8
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from .models import Jbxx
from .spiders import Spider

class sdxy(APIView):

    def post(self,request):
        dict = {}
        key = request.POST.get("companyName","")
        # result_lt = Jbxx.objects.using('sdxydb').filter(companyname=key)
        result_lt = None
        if result_lt:
            item = {}
            item["db"] = "sdxy"
            item["table"] = "jbxx"
            item["webSourse"] = 'https://shuidi.cn/'

            dict["code"] = 200
            dict["message"] = "数据抓取保存成功"
            dict["data"] = item
        else:
            try:
                RUN = Spider(key)
                dicts = RUN.jbxx_spider()

                if dicts:
                    try:

                        jbxx = Jbxx()
                        # 统一社会信用代码 企业名  组织机构代码 工商注册号 经营状态 所属行业 法人 注册资本  成立日期
                        jbxx.companyname = dicts["companyName"]
                        jbxx.creditcode = dicts["creditCode"]
                        jbxx.organizationcode = dicts["organizationCode"]
                        jbxx.registernum = dicts["registerNum"]
                        jbxx.businessstate = dicts["businessState"]
                        jbxx.industry = dicts["industry"]
                        jbxx.legalman = dicts["legalMan"]
                        jbxx.registermoney = dicts["registerMoney"]
                        jbxx.registertime = dicts["registerTime"]

                        jbxx.registorgan = dicts["registOrgan"]
                        jbxx.confirmtime = dicts["confirmTime"]
                        jbxx.businesstimeout = dicts["businessTimeout"]
                        jbxx.companytype = dicts["companyType"]

                        jbxx.registeraddress = dicts["registerAddress"]
                        jbxx.businessscope = dicts["businessScope"]
                        jbxx.personnelscale = dicts["personnelScale"]
                        jbxx.insuredpersons = dicts["insuredPersons"]
                        jbxx.usedname = dicts["usedName"]
                        jbxx.operation = dicts["operation"]
                        jbxx.websource = dicts["webSource"]
                        print(dicts)
                        jbxx.storagetime = dicts["storageTime"]

                        jbxx.save(force_update=True)



                        item = {}
                        item["db"] = "test"
                        item["table"] = "jbxx"
                        item["webSourse"] = 'https://shuidi.cn/'
                        dict["code"] = 200
                        dict["message"] = "数据抓取保存成功"
                        dict["data"] = item
                    except Exception as e:
                        dict["code"] = 203
                        dict["message"] = "抓取成功，信息存储失败"
                        dict["data"] = None
                        return Response(dict)
                else:
                    dict["code"] = 201
                    dict["message"] = "未找到匹配的公司名"
                    dict["data"] = None
            except Exception as e:
                dict["code"] = 202
                dict["message"] = "网站信息抓取失败"
                dict["data"] = None

        return Response(dict)
