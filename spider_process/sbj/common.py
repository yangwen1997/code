import pymongo
import redis

from random import choice

MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]

sbj_DB = pymongo.MongoClient(host='172.16.75.28',port=27017)

#url表
scjd_urlDB = sbj_DB["SBJ"]["scjddateurl"]
yyjd_urlDB = sbj_DB["SBJ"]["yyjddateurl"]
sbps_urlDB = sbj_DB["SBJ"]["sbpsdateurl"]

#详情信息表
scjd_DB = sbj_DB["SBJ"]["scjddate"]
yyjd_DB = sbj_DB["SBJ"]["yyjddate"]
sbps_DB = sbj_DB["SBJ"]["sbpsdate"]


# redis
red_cli = redis.Redis(host="172.16.75.38",port=6379,db=15)


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


import os
import logging
import time
def logger(FILE_NAME):
    """
    日志配置
    :param FILE_NAME: 日志文件名(全路径 )
    :return:日志记录生成器
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y %H:%M:%S',
        filename=FILE_NAME,
        filemode='w'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging

def get_log():
    real_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + "/log/"
    file_name = "{}_爬虫程序_{}.log".format(real_path,time.strftime("%Y-%m-%d",time.localtime()))
    log = logger(file_name)
    return log


import requests
import hashlib

from lxml.etree import HTML,tostring

class sbjws_base(object):
    """商标局文书基类"""
    def __init__(self):
        self.s = requests.session()
        self.s.headers.update({
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        })
        self.proxy,self.ipItem = ABY()
        self.IPcount = 0
        self.log = get_log()
        self.page = 1
        self.pageTotal = 2
        self.pagenum = 2

    def get_proxy(self):
        """
        请求代理IP
        :return:
        """
        self.ipItem["flag"] = "0"
        STATIC_IP.save(self.ipItem)
        self.proxy, self.ipItem = ABY()

    def get_req(self,url):
        """
        get请求封装，超过3次停止请求，自动更新替换IP
        :param url:
        :return:
        """
        try:
            if self.IPcount < 3:
                # resp = self.s.get(url=url,proxies=self.proxy,timeout=30)
                resp = self.s.get(url=url,timeout=30)

                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    return resp
                else:
                    self.get_proxy()
                    self.IPcount += 1
                    self.log.info("页面状态码错误，更换IP")
            else:
                self.log.info("请求超过3次出错停止请求")
                self.get_proxy()
                self.IPcount = 0
                return None
        except Exception as e:
            self.get_proxy()
            self.IPcount += 1
            self.log.info("超时出错")

    def post_req(self,url,data):
        """
        post请求封装，超过3次停止请求，自动更新替换IP
        :param url:
        :return:
        """
        try:
            if self.IPcount < 3:
                resp = self.s.post(url=url,data=data,proxies=self.proxy,timeout=60)

                if resp.status_code == 200:
                    resp.encoding = resp.apparent_encoding
                    return resp
                else:
                    self.get_proxy()
                    self.IPcount += 1
                    self.log.info("页面状态码错误，更换IP")
            else:
                self.log.info("请求超过3次出错停止请求")
                self.get_proxy()
                self.IPcount = 0
                return None
        except Exception as e:
            self.get_proxy()
            self.IPcount += 1
            self.log.info("超时出错")

    def urlxpath(self,resp):
        """
        列表页url解析
        :param resp:
        :return:
        """
        ETRE = HTML(resp.text)
        urllt = ETRE.xpath('//div[@class="link"]//tr/td[2]/a/@href')
        nametext = ETRE.xpath('//div[@class="link"]//tr/td[2]/a/p/text()')
        return urllt,nametext

    def urlltsave(self,dateurl,datename,category):
        """
        保存数据到mongo
        :param dateurl:
        :param datename:
        :return:
        """
        item = {}
        item["dateurl"] = "http://wssq.sbj.cnipa.gov.cn:9080" + dateurl.replace('\n',"")
        item["_id"] = hashlib.md5(item["dateurl"].encode('utf-8')).hexdigest()
        item["datename"] = datename
        item["category"] = category
        item["flag"] = "0"
        if category == "商标注册审查决定文书":
            try:
                scjd_urlDB.insert(item)
                self.log.info(f"数据{item['_id']}插入mongo......")
            except Exception as e:
                print(e)
        elif category == "商标异议决定文书":
            try:
                yyjd_urlDB.insert(item)
                self.log.info(f"数据{item['_id']}插入mongo......")
            except Exception as e:
                print(e)
                exit()
        elif category == "商标评审裁定/决定文书":
            try:

                sbps_urlDB.insert(item)
                self.log.info(f"数据{item['_id']}插入mongo......")
            # sbps_urlDB.save(item)
            except Exception as e:
                print(e)
                exit()

    def fun_to_redis(self,category):
        result = None
        if category == "商标注册审查决定文书":
            result = scjd_urlDB.find()
            # result = scjd_urlDB.find({"flag":"0"})
        elif category == "商标异议决定文书":
            result = yyjd_urlDB.find()
            # result = yyjd_urlDB.find({"flag": "0"})
        elif category == "商标评审裁定/决定文书":
            result = sbps_urlDB.find()
            # result = sbps_urlDB.find({"flag": "0"})

        for _ in result:
            _["flag"] = "1"
            if category =="商标注册审查决定文书":
                red_cli.sadd("scjd_urlDB",str(_))
                try:
                    scjd_urlDB.find_one_and_update({"_id":_["_id"]},{"$set":{"flag":"1"}})
                except Exception as e:
                    print(e)
                    exit()

            elif category =="商标异议决定文书":
                red_cli.sadd("yyjd_urlDB",str(_))

                try:
                    yyjd_urlDB.find_one_and_update({"_id":_["_id"]},{"$set":{"flag":"1"}})
                except Exception as e:
                    print(e)
                    exit()

            elif category == "商标评审裁定/决定文书":
                red_cli.sadd("sbps_urlDB",str(_))


                try:
                    sbps_urlDB.find_one_and_update({"_id":_["_id"]},{"$set":{"flag":"1"}})
                except Exception as e:
                    print(e)
                    exit()
            print("数据存入redis成功。。。。。")

    def fun_spider_dateInfo(self,redis_name):
        """
        根据指定的名称抓取不同的页面程序
        :param redis_name: mongo_db键名以及redis缓存表名
        :return:
        """
        import re
        count = red_cli.scard(redis_name)
        mongo_db = {
            "scjd_urlDB": scjd_DB,
            "yyjd_urlDB": yyjd_DB,
            "sbps_urlDB": sbps_DB,
        }
        time_dict = {
            "Jan":"01",
            "Feb":"02",
            "Mar":"03",
            "Apr":"04",
            "May":"05",
            "Jun":"06",
            "Jul":"07",
            "Aug":"08",
            "Sep":"09",
            "Oct":"10",
            "Nov":"11",
            "Dec":"12",
        }

        data_db = mongo_db[redis_name]
        while count:
            try:
                data = red_cli.srandmember(redis_name)
                item = eval(data)
                url = item["dateurl"]
                resp = self.get_req(url)

                if resp:
                    etre = HTML(resp.text)
                    html_info = etre.xpath('//div[@class="Three_xilan_02"]')
                    item["tag_text"] = tostring(html_info[0], method='html',encoding='utf-8').decode()

                    html_time = re.findall(r'(\w+\s\w+ \d+ \d+:\d+:\d+ CST \d+)',resp.text)
                    item["Year"] = html_time[0].split(" ")[-1]
                    item["Month"] = time_dict[html_time[0].split(" ")[1]]
                    item["dateTime"] = item["Year"] + "年" + item["Month"] + "月" + html_time[0].split(" ")[2] + "日"
                    try:
                        data_db.insert(item)
                    except:
                        print("数据跟新完毕")
                        exit()
                    red_cli.srem(redis_name,data)
                    self.log.info(f"数据{item['_id']}存入mongo完成。。。")
                    count -= 1
                else:
                    self.log.info(f"url-3次请求结果为空")
                    time.sleep(2)
            except Exception as e:
                self.log.info(e)