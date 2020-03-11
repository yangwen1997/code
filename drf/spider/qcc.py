#coding=utf-8
'''
@author : yangwnlong
@file  : qcc
@inter : 企查查爬虫程序
'''
import requests
# from lxml.etree import HTML
s = requests.session()
# s.headers.update({
# "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
# })
# url = 'https://m.qichacha.com/search?key=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'
# resp = s.get(url=url)
# resp.encoding = 'utf-8'
#
# etre = HTML(resp.text)
# a_lt = etre.xpath('//div[@class="list-item"]/ancestor::a/@href')
# if a_lt:
#     url = "https://m.qichacha.com" + a_lt[0]
#     resp = s.get(url=url)
#     resp.encoding = 'utf-8'
#     print(resp.text.encode("GBK","ignore"))
#
data = {
    'companyName' : "小鸭顶呱呱有限公司"
}
# url = 'http://127.0.0.1:8001/index/'
# url = 'http://10.2.1.57:8005/index/'
url = 'http://10.2.1.57:8005/sdxy/index/'
# resp = s.post(url=url,data=data)
import execjs
import re
# url = 'https://www.qixin.com/'

resp = s.post(url=url,data=data)
resp.encoding ='utf-8'
# print(resp.text.encode('GBK','ignore'))
# jstext = "".join(re.findall('<script>(.*?)</script>',resp.text,re.S))
print(resp.text)
# print(jstext)

import time
# print(time.strftime("%Y-%m-%d", time.localtime()))
print(time.localtime())
