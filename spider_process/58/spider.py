import requests

s = requests.session()

s.headers.update({
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
})

url = "https://cd.58.com/qzzpfangchanjianzhu/?param8427=1"
resp = s.get(url)
resp.encoding = 'utf-8'
print(resp.text)