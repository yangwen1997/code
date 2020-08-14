import requests

import execjs
s = requests.session()

s.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",


})

# resp = s.get('http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=e267cdc29a94ef11d68e49e255d9292b&s8=04')
# Cookie = resp.headers["Set-Cookie"]

# print(Cookie)
s.headers.update({
    # "Cookie":Cookie,
    "Cookie":"HM4hUBT0dDOn80S=1RxwjcrEJospL3Eq.BD3g5BKlG0VEg6P2cz7TSRYsSovRhFONDchJ.k_uINdW.H7; HM4hUBT0dDOn80T=4581LlORAuBluIJOg_.0qP5TLj73IMMl_hGyr5rYjJQQbjvEGhtgNWZUw2a37S6z617DKOxllmJKDCo01KaqGy5YKGf5YVDdbl.nGj7jFvfX7LX0P6fasaxvoK.l2RblLTOA28NSkfGCAYsy3WRJxR_XaxHOWwLG3NQxYhHbDN9jsMS2sE3K8IBWnBHZ0wtfs4ovn2x_ZCxRl8QcoLjUjWkXh",
    # "X-Requested-With": "XMLHttpRequest",
    # "Referer": "http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=e267cdc29a94ef11d68e49e255d9292b&s8=04",
})
# resp = s.get('http://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=e267cdc29a94ef11d68e49e255d9292b&s8=04')
# resp.encoding = 'utf-8'
# print(resp.text)
url = 'http://wenshu.court.gov.cn/website/parse/rest.q4w'
# url = 'http://wenshu.court.gov.cn/website/parse/rest.q4w?HifJzoc9=4WgA9v.Xk7OYZWF3J2rVJVM.dYG42Zl9zlRmFeL4vr8XGn0p6iwiL_VMJ7iIqH09FIiX3mA4Uuq4VVhq5gSp.PNJ4VUjvJ.8XWHFcoKhxQDuWdQeK8fgQTumvkXmqlDlYrsg4.6Jse_ovbgON7uuaGAVKicT9IcwCFu6mRFvzdJ8sEOBzDLw_4VKBAOdMjX0sDOd797K3KIHA4xeuPNDFvbE18BHBfNuo8fFCXaBePqEiQB31kAbGn_NVmcchX0kkVTB9tScm5oO2JWYLDFMb195YtMEyJYJgjNVZYyp17zDm00BGbHuGv94WHh.FLYITVQ9.HjfX03hfCEvOPbFJyVcj6lH6rdECMFIks17jLwMQMZL.UEe5zAQJZRd4TE4377i'
with open(r'E:\code\spider\spider_process\cpws\a.js','r',encoding='utf-8')as fp:
    cipjs = fp.read()
cipetx = execjs.compile(cipjs)
cip = cipetx.call('cip')
token = cipetx.call('Token')
#
data = {
    "pageId": "e267cdc29a94ef11d68e49e255d9292b",
    "s8": "04",
    "sortFields": "s50:desc",
    "ciphertext":cip,
    "pageNum": "1",
    "queryCondition": '[{"key":"s8","value":"04"}]',
    "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
    "__RequestVerificationToken": token,
}


resp = s.post(url,data=data)
resp.encoding = 'utf-8'
print(resp.text)
