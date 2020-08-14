# encoding='utf-8'
'''
@author yangwenlong
@inter 美团酒店爬虫程序
'''

import execjs
import requests
import math
import hashlib
import asyncio

from common import mt_spider_base,SPIDERDB,get_log

log = get_log()

JD_PCPId = SPIDERDB["MTDB"]["JD_PCPId"]
JD_PC_DATA_info =  SPIDERDB["MTDB"]["JD_PC_DATA_info"]


class jd_spider(object):
    def __init__(self):
        self.base_class = mt_spider_base()
        self.page = 1
        self.offset = 20

    def data_poiid_save(self,poiidlt, category):
        """
        保存列表页数据ID到mongo
        :param poiidlt:
        :return:
        """
        for _ in poiidlt:
            item = {}
            item["poiid"] = _["poiid"]
            item["city"] = _["cityName"]
            item["name"] = _["name"]
            item["category"] = category
            item["scoreIntro"] = _["scoreIntro"]
            item["addr"] = _["addr"]
            item["posdescr"] = _["posdescr"]
            item["info_url"] = f"https://hotel.meituan.com/{str(_['poiid'])}/"
            item["_id"] = hashlib.md5((str(item["poiid"]) + str(item["name"])).encode('utf-8')).hexdigest()
            JD_PCPId.save(item)
            log.info(f"数据{item['_id']}存入mongo成功.........")

    async def jd_spider_start(self,areid=None,category=None):
        """酒店爬虫程序"""
        try:

            
            # 首页抓取
            url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&cityId=10&offset=' + str(self.offset-20) + f"&limit=20&startDay=20200618&endDay=20200618&q=&sort=defaults&areaId={areid}"
            resp = self.base_class.get_req(url)
            poiidlt = resp.json()["data"]["searchresult"]
            dateCount = int(resp.json()["data"]["totalcount"])
            self.data_poiid_save(poiidlt,category)
            self.offset += 20

            # 分页获取逻辑
            if dateCount > 20:
                page = math.ceil(dateCount / 20)
            else:
                page = 1

            while self.page < page:
                try:
                    url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&cityId=10&offset=' + str(
                        self.offset - 20) + f"&limit=20&startDay=20200618&endDay=20200618&q=&sort=defaults&areaId={areid}"

                    resp = resp = self.base_class.get_req(url)
                    poiidlt = resp.json()["data"]["searchresult"]
                    dateCount = int(resp.json()["data"]["totalcount"])
                    self.data_poiid_save(poiidlt, category)
                    log.info(f"第{areid}类-第{self.page}页的数据抓取完成。。。。")
                    self.page += 1
                    self.offset += 20

                except Exception as e:
                    log.info(e)

            print(f"第{areid}类数据抓取完毕")
            
        except Exception as e:
            log.info(e)

    def jd_dateinfo_spider(self):
        """酒店详情页面数据抓取"""
        import redis
        from lxml.etree import HTML
        red_cli = redis.Redis(host="172.16.75.38", port=6379, db=15)
        count = red_cli.scard('jd_mt_url')

        while count:
            try:
                data = red_cli.srandmember('jd_mt_url')
                item = eval(data)
                url = item["info_url"]
                # url = "https://hotel.meituan.com/1704822983/"
                resp = self.base_class.get_req(url)
                if '<meta http-equiv="refresh" content="0; url=http://www.meituan.com/error/" />' == resp.text:
                    red_cli.srem('jd_mt_url', data)
                    log.info("无效的页面")
                    count -= 1
                else:
                    etre = HTML(resp.text)
                    phone = "".join(etre.xpath('//li[@class="mb10 m20 fc6 fs14"]/div[2]/text()')).replace("电话：","")
                    if phone:
                        if "/" in phone:
                            item["tel"] = phone.split("/")[0]
                            item["phone"] = phone.split("/")[1]
                        else:
                            item["phone"] = phone
                        JD_PC_DATA_info.save(item)
                        red_cli.srem('jd_mt_url',data)
                        log.info(f"{item['_id']}存入mongo完成....")
                        count -= 1
                    else:
                        # if "暂时没有符合的酒店" in resp.text:
                        red_cli.srem('jd_mt_url', data)
                        count -= 1
                        log.info("页面暂未获取到手机号")
                    count -= 1
            except Exception as e:
                print(e)



async def main(x):
    # 多协程的方式传入不同地区的区域ID增加列表页数据抓取的速度
    spider_start = jd_spider()
    await spider_start.jd_dateinfo_spider()

def url_list_start():
    areidLT = ["664", "9138", "9139", "9142", "9143", "9144", "9250", "9551", "12307", "12308", "12591", "13407",
               "13881",
               "25213", "38727", "38860"]
    coun = [main(areidLT[_]) for _ in range(len(areidLT))]

    tasks = [asyncio.ensure_future(_) for _ in coun]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

def to_redis():
    """拉取数据存入REDIS"""
    import redis
    red_cli = redis.Redis(host="172.16.75.38", port=6379, db=15)

    result = JD_PCPId.find({"city" : "上海"})

    for _ in result:
        red_cli.sadd("jd_mt_url",str(_))
        log.info("数据存入redis完成.........")

def data_start(*args):
    spider_start = jd_spider()
    spider_start.jd_dateinfo_spider()

def mains():
    from concurrent.futures import ThreadPoolExecutor
    executor = ThreadPoolExecutor(max_workers=11)
    for i in range(10):
        executor.submit(data_start)

if __name__ == '__main__':
    # url_list_start()
    # to_redis()
    mains()
    

