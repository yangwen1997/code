from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from .sdxy.spider import Spider,start
from .sdxy.basic_nfo import basc_Spider,basc_start

s = requests.session()
s.headers.update({
    "User-Agent" :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
})


def result_judge(resp,item,dict):
    """结果判断复制"""
    if resp != 'IP无效' and resp != "未搜索到公司" and resp != "公司名不匹配" and resp != '页面为空':
        dict["data"] = resp
    elif resp == "未搜索到公司" or resp == "公司名不匹配" or resp == '页面为空':
        item["errMsg"] = "未找到符合条件的查询结果，请更改关键词重新查询"
        dict["err_msg"] = item

    else:
        item["errMsg"] = "实时查询结果失败，请点击重新尝试"
        dict["err_msg"] = item

class sdxy_data_search(APIView):
    """
    水滴信用全量信息
    """
    def post(self,request):
        dict = {}
        item = {}
        try:
            dict["code"] = 200

            company = request.POST.get("company_name","")
            if company:
                resp = start(key=company)
                result_judge(resp=resp,item=item,dict=dict)
            else:
                item["errMsg"] = "请输入正确的公司名"
                dict["err_msg"] = item

        except Exception as e:
            item["errMsg"] = "服务器错误"
            dict["err_msg"] = item

        return Response(dict)

class sdxy_basic(APIView):
    """水滴信用接口"""
    def post(self,request):
        dict = {}
        dict["code"] = 200
        item = {}
        try:
            company = request.POST.get("company_name",None)
            ApiType = request.POST.get("ApiType",None)
            if company:
                resp = basc_start(key=company,ApiType=ApiType)
                result_judge(resp=resp,item=item,dict=dict)
            else:
                item["errMsg"] = "请输入正确的公司名"
                dict["err_msg"] = item
        except Exception as e:
            item["errMsg"] = "服务器错误"
            dict["err_msg"] = item

        return Response(dict)


class bdxy_basic(APIView):

    def post(self,request):
        """
        百度信用基本信息接口
        :param request:
        :return:
        """
        dict = {}
        dict["code"] = 200
        item = {}
        try:
            company = request.POST.get("company_name", None)
            ApiType = request.POST.get("ApiType", None)
            if company:
                data = {'company_name': company,}
                url = ""
                if ApiType == '全部信息查询' or ApiType is None:
                    pass
                elif ApiType == '基本信息查询':
                    url = 'http://172.16.74.78:1234/add/Tyccompany/'
                resp = s.post(url, data=data)
                resp.encoding = 'utf-8'
                dict["data"] = resp.json()

            else:
                item["errMsg"] = "服务器错误"
                dict["err_msg"] = item

        except Exception as e:
            print(e)

        return Response(dict)
