import requests


s = requests.session()

s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
})

resp = s.get("https://www.feigua.cn")
resp.encoding = 'utf-8'

print(resp.text)