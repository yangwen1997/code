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

data = {
    'companyName' : "顶呱呱"
}
url = 'http://127.0.0.1:8083/index/'
# url = 'http://127.0.0.1:8083/sdxy/index/'
resp = s.post(url=url,data=data)
#
print(resp.text)

# def ABY():
#     proxyHost = "http-dyn.abuyun.com"
#     proxyPort = "9020"
#
#     # 代理隧道验证信息
#     proxyUser = "HQ74H343NC8P83MD"
#     proxyPass = "72425EBF9493543B"
#
#     proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
#         "host": proxyHost,
#         "port": proxyPort,
#         "user": proxyUser,
#         "pass": proxyPass,
#     }
#
#     proxies = {
#         "http": proxyMeta,
#         "https": proxyMeta,
#     }
#     # print(proxies)
#     return proxies
# from lxml.etree import HTML
# import time
# import urllib.parse
# zg = str({"sid": int(time.time()*1000),"updated": int(time.time()*1000),"info": int(time.time()*1000),"superProperty": "{}","platform": "{}","utm": "{}","referrerDomain": ""})
# zg_ = urllib.parse.quote(zg)
#
# s.headers.update({
#     "Connection": "keep-alive",
#     "Upgrade-Insecure-Requests": "1",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
#     "Sec-Fetch-User": "?1",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     # "Cookie": f"zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f={zg_}",
# })
# url = "https://www.qichacha.com/search?key=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4 "
# #
# count = 100
# while count:
#     proxy = ABY()
#     resp = s.get(url=url,proxies=proxy)
#     resp.encoding = resp.apparent_encoding
#     ETRE = HTML(resp.text)
#     res = "".join(ETRE.xpath('//tbody[@id="search-result"]/tr[1]/td/a/@href'))
#     print(res)
#     print(count)
#     count -= 1



