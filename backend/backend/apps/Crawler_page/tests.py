from django.test import TestCase

# Create your tests here.

import requests
import json

s = requests.session()

s.headers.update({
    'User-Agent' :"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
})
url = 'http://172.16.75.38:8001/crawler/bdxy_basic/'
# url = 'http://127.0.0.1:8000/crawler/bdxy_basic/'
# url = 'http://172.16.74.78:5678/add/Baiducompany/'
# url = 'http://172.16.74.78:1234/add/Tyccompany/'
data = {
    # "company_name" : "aaa",
    "ApiType":"基本信息查询",
    'company_name': "华为技术有限公司",
}
resp = s.post(url,data=data)
resp.encoding = 'utf-8'
print(resp.text)
# {"err_msg":"未找到符合条件的查询结果，请更改关键词重新查询"}
