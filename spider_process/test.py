import requests

s = requests.session()

s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
})

resp = s.get(url="http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?s21=%E4%B8%8A%E6%B5%B7%E6%B3%95%E9%99%A2")
resp.encoding = 'utf-8'
print(resp.text)