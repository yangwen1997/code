# encoding= utf-8
from django.test import TestCase

# Create your tests here.

import requests

s = requests.session()
s.headers.update({
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
})
url = 'http://127.0.0.1:8000/Shareholder/'
# url = 'http://127.0.0.1:8000/index/'
data = {
    "companyName": "阿里巴巴（中国）网络技术有限公司"
}
resp = s.post(url=url,data=data)
print(resp.text)
