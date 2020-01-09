#encoding=utf-8
from rest_framework import serializers
from .models import Jbxx

class JbxxSerializer(serializers.Serializer):
    """序列化模型"""
    companyname = serializers.CharField(max_length=255)
    creditcode =serializers.CharField(max_length=255)
    organizationcode = serializers.CharField(max_length=255)
    registernum = serializers.CharField(max_length=255)
    businessstate = serializers.CharField(max_length=255)
    industry = serializers.CharField(max_length=255)
    legalman = serializers.CharField(max_length=255)
    registermoney = serializers.CharField(max_length=255)
    registertime = serializers.CharField(max_length=255)
    registorgan = serializers.CharField(max_length=255)
    confirmtime = serializers.CharField(max_length=255)
    businesstimeout = serializers.CharField(max_length=255)
    companytype = serializers.CharField(max_length=255)
    registeraddress = serializers.CharField(max_length=255)
    businessscope = serializers.CharField()
    personnelscale = serializers.CharField(max_length=255)
    insuredpersons = serializers.CharField(max_length=255)
    usedname = serializers.CharField(max_length=255)
    operation = serializers.CharField(max_length=255)
    websource = serializers.CharField(max_length=255)
    storagetime = serializers.DateTimeField()
