from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DbInfo

class DBmanage(APIView):

    def post(self,request):
        """
        DB数据库管理接口
        :param request:
        :return:
        """
        dict = {}
        dict["code"] = 200
        data_lt = []
        datdName = request.POST.get("datdName")
        try:
            result = DbInfo.objects.filter(title=datdName)
            for _ in result.values():
                _["dates"] = eval(_["dates"])
                print(_)
                data_lt.append(_)
            dict["msg"] = data_lt

        except Exception as e:
            print(e)
            dict["code"] = 405
            dict["errmsg"] = '服务器内部错误'
        return Response(dict)
