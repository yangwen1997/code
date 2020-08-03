# from zheye import zheye
# z = zheye()
#
# import requests
#
# s = requests.session()
# s.headers.update({
#
# })
# positions = z.Recognize(r'E:\code\chineseocr-app\trademark_ocr_notice\zheye-master\realcap\a.jpg')
#
# print(positions)


e = {
"captcha": "",
"clientId": "c3cef7c66a1843f8b3a9e6a1e3160e20",
"grantType": "password",
"lang": "en",
"password": "dgg962540",
"refSource": "other_https://www.zhihu.com/signin",
"signature": "fa8ae135f43058666659269b1cedae91170e1c5d",
"source": "com.zhihu.web",
"timestamp": "1594087177200",
"username": "3045871342@qq.com",
"utmSource": "undefined",
}

js = "function get(){a = encodeURIComponent(%s)return a}"%(e)

import execjs
from urllib import parse

# etx = execjs.compile(js)
# a = etx.call("get")
# print(execjs.get().name)
# print(a)

print(parse.quote(e))