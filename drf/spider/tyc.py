
import requests
from lxml.etree import HTML
s = requests.session()
s.headers.update({
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
})

url = 'https://m.tianyancha.com/search?key=%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4'
resp = s.get(url=url)
resp.encoding = resp.apparent_encoding
print(resp.text)

etre = HTML(resp.text)
lt = etre.xpath('//div[@class="search-name"]/a/@href')
if lt:
    url = lt[0]
    resp = s.get(url=url)
    resp.encoding = resp.apparent_encoding
    print(resp.text)
