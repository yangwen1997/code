import requests
import pymongo
import hashlib
from random import randint,choice



url = 'https://lskdjf3lw34iu9w.dafacloudapp.com/v1/users/register'

# 静态IP数据库
MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

APP =  MONGO_DB["YANG"]["app"]
def ABY():
    """随机返回代理IP"""
    try:
        # IP = STATIC_IP.find({"flag":"1"})
        IP = STATIC_IP.find().limit(9).skip(10)
        # IP = STATIC_IP.find().limit(19)

        ip = choice([_ for _ in IP])

        proxies = {
            "http": "http://" + ip["ip_parmas"],
            "https": "https://" + ip["ip_parmas"],
        }
        return proxies,ip
    except Exception as e:
        print(e)
        return None

class IP(object):
    def __init__(self):
        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.s = requests.session()
        self.s.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Cookie": "__snaker__captcha=RAryA7TprzbSNhur; _9755xjdesxxd_=32; YD00972884761583%3AWM_NI=6IVUeCeO8Il9hIFjiuWBcOsN4JghgqA3VwI5ZPXVFI4C4j8pubAoJMQWp4%2FFE4E4Sz5vnvBo7wjaVABk1SRH4CXprfhVDZCmqoU18l8ftwnzeugzZTrsen59xGwBC%2FbKN1k%3D; YD00972884761583%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee82e7618ab4e194f93f94b08bb3d45e868a8eaaf15db4bb9ca7db339cbf87a3e22af0fea7c3b92af6979ab6e849a791f8aaef33ac978a8bec7f959eadb0f246f896a989e67b83ed9a98cc3f9a9098b7c543f89dfc8bbb7cb7be8f90c9479389c0d5ae4e87ec8bd5d272f7aaa297c165f5a9a682d54b82b5ffb4d144f89d9891f16eac8a8cbbc267b3b19bd2bb68fcbabc98ed72a7aba99bd960b2adab8fb833bc99b9a3c225a29582d2ea37e2a3; YD00972884761583%3AWM_TID=1AilI%2FnoU5JAAEFRQAYqGoaDQHsTadRM; gdxidpyhxdE=Z4uulOoKEm%2BCiZqxKIR0UExVHV%5CWSufCBsW4roeMketwJ0lRlmJG6%2F8DNPZ%2B1OuULn%2BfdqGGMRhdoI2uMD9xAMiW5%2B0V7CMncBkU4feCbmjUpUC6zS55%2B0l5RL5Q80ljymTCL96yMTIrWP%2BZqSJHVL%2FMNnOV04xTjxfpiBk3%5CdGsTTfX%3A1596014550307",
            "Referer": "https://lskdjf3lw34iu9w.dafacloudapp.com/register",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        })

    def get_proxy(self):
        """
        请求代理IP
        :return:
        """
        self.ipItem["flag"] = "0"
        STATIC_IP.save(self.ipItem)
        self.proxy, self.ipItem = ABY()

    def post_req(self,url,data):
        """
        post请求封装，超过3次停止请求，自动更新替换IP
        :param url:
        :return:
        """
        try:
            if self.IPcount < 3:
                # resp = self.s.post(url=url,data=data,proxies=self.proxy)
                resp = self.s.post(url=url,data=data)

                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    return resp
                else:
                    self.get_proxy()
                    self.IPcount += 1
                    print("页面状态码错误，更换IP")
            else:
                print("请求超过3次出错停止请求")
                self.get_proxy()
                self.IPcount = 0
                return None
        except Exception as e:
            self.get_proxy()
            self.IPcount += 1
            print("超时出错")

s = IP()




while 1:
    def getint():
        return str(randint(0,9))
    inviteCode = getint() + getint() + getint() + getint() + getint() + getint() + getint() + getint()
    data = {
        "inviteCode":inviteCode ,
        "userName": "adssagfgssgffs",
        "password": "2587f14276c8bb82dd56f5c0915b3f75",
        "type": "1"
    }
    resp = s.post_req(url=url,data=data)

    if resp:
        resp.encoding = 'utf-8'
        res = resp.json()
        if res["msg"] == "请先验证滑动码":
            item = {}
            item["_id"] = hashlib.md5(inviteCode.encode("utf-8")).hexdigest()
            item["value"] = inviteCode
            APP.save(item)
            print('item["_id"]')
        else:
            print("失败的邀请码")
    else:
        print("连续3次请求失败")

