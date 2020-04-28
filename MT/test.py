import requests
import time
import re
import json
ts = int(time.time()) * 1000
s = requests.session()

s.headers.update({

})

def getword(word):
    url = 'https://fanyi.baidu.com/sug'
    data = {
        "kw":word
    }
    resp = s.post(url,params=data)
    resp.encoding = 'utf-8'
    print(resp.text)
    # resp = json.loads("".join(re.findall(r'\((.*?)\)',resp.text)))["origtxt"]
    print(resp)
getword("你好")