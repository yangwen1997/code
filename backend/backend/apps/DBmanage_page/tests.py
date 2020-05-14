from django.test import TestCase

# Create your tests here.


import requests

data = {
    "datdName":"裁判文书",
}
s = requests.session()
resp = s.post('http://172.16.75.38:8001//dbmanage/dbpage',data=data)
print(resp.text)
