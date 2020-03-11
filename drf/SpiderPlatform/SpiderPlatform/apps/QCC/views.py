#encoding=utf-8

# Create your views here.
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from .spider import QCC
from .models import Jbxx,ShareHolder
from .serializers import JbxxSerializer

def sucess_result(dict,dbname,table):
    """正确的返回结果"""
    item = {}
    item["db"] = dbname
    item["table"] = table
    item["webSourse"] = 'https://qichacha.com'
    dict["code"] = 200
    dict["message"] = "数据抓取保存成功"
    dict["data"] = item
    return dict

class JBXX(APIView):
    """
    企查查爬虫程序基本信息接口服务
    """
    def post(self,request):
        dict = {}
        companyname = request.POST.get('companyName')

        if companyname:
            dict["code"] = 200
            # result_lt = Jbxx.objects.filter(companyname=companyname)
            result_lt =None
            if result_lt:
                item = {}
                item["db"] = "test"
                item["table"] = "jbxx"
                item["webSourse"] = 'https://qichacha.com'
                dict["code"] = 200
                dict["message"] = "数据抓取保存成功"
                dict["data"] = item

            else:
                dicts = {}
                try:
                    RUN = QCC(keys=companyname)
                    dicts = RUN.spider_run_jbxx()
                    if dicts:
                        pass
                    else:
                        dict["code"] = 201
                        dict["message"] = "未找到匹配的公司名"
                        dict["data"] = None
                        return Response(dict)
                except Exception as e:
                    dict["code"] = 202
                    dict["message"] = "网站信息抓取失败"
                    dict["data"] = None

                try:
                    jbxx = Jbxx()
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
                    jbxx.websource = dicts["websource"]
                    jbxx.storagetime = dicts["storageTime"]
                    jbxx.save(force_update=True)
                    dict = sucess_result(dict, "test", 'jbxx')

                except Exception as e:
                    dict["code"] = 203
                    dict["message"] = "抓取成功，信息存储失败"
                    dict["data"] = None
                    return Response(dict)

        else:
            dict["code"] = 201
            dict["message"] = "未找到匹配的公司名"
            dict["data"] = None

        return Response(dict)

class Shareholder(APIView):
    """企查查工商股东信息接口服务"""

    def post(self,request):
        dict = {}
        companyname = request.POST.get('companyName')
        # 如果获取到提交的公司名字

        if companyname:
            dict["code"] = 200

            result = ShareHolder.objects.filter(companyname=companyname)

            # 从数据库中进行查询，如果没有查到进行抓取，查到直接返回结果
            if result:
                item = {}
                item["db"] = "test"
                item["table"] = "shareholder"
                item["webSourse"] = 'https://qichacha.com'
                dict["code"] = 200
                dict["message"] = "数据抓取保存成功"
                dict["data"] = item
            else:
                try:
                    RUN = QCC(keys=companyname)
                    dicts = RUN.spider_run_Shareholder()
                    if dicts:
                        for _ in dicts:
                            db = ShareHolder()
                            db.companyname = _['companyname ']
                            db.shareholdername = _['shareholdername ']
                            db.shareholderatio = _['shareholderatio ']
                            db.shareholdetype = _['shareholdetype ']
                            db.subscription = _['subscription ']
                            db.subscriptiondate = _['subscriptiondate ']
                            print('111111')
                            print(db)
                            db.save()
                        dict = sucess_result(dict, "test", 'shareholder')

                    elif dicts == '解析失败':
                        dict["code"] = 202
                        dict["message"] = "网站信息抓取失败"
                        dict["data"] = None
                        return Response(dict)
                    else:
                        dict["code"] = 201
                        dict["message"] = "未找到匹配的公司名"
                        dict["data"] = None
                        return Response(dict)
                except Exception as e:
                    dict["code"] = 203
                    dict["message"] = "抓取成功，信息存储失败"
                    dict["data"] = None
                    return Response(dict)


        else:
            # 如果未获取到提交的公司名字
            dict["code"] = 201
            dict["message"] = "未找到匹配的公司名"
            dict["data"] = None

        return Response(dict)
