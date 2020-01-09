#coding=utf-8
'''
@author : yangwenlong
@file : qcc/spider
'''
# import async
# import aiohttp
import requests
from lxml.etree import HTML
from .common import get_log,ABY
from .XPATH import QCC_XPATH
log = get_log()
import re



class QCC(object):
    def __init__(self,keys):
        self.keys = keys
        self.url = 'https://m.qichacha.com'
        self.session = requests.session()
        self.session.headers.update({
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-User": "?1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Cookie": "acw_tc=767bf19515782959354945526e28803ea9568107bbd3940ec9684f47ed; acw_sc__v2=5e12e27f9b0b69742f71286e34dd368551cf381b; PHPSESSID=42n7e1ghdi2j5sk8t4bb9dqhu4; zg_did=%7B%22did%22%3A%20%2216f79c4ca61300-0eb25c6ffa5653-6701b35-1fa400-16f79c4ca62952%22%7D; acw_sc__v3=5e12e27fd4397cdddf41ea4de650082424cad62c; UM_distinctid=16f79c4cae72de-0fa4c0a6fba1ac-6701b35-1fa400-16f79c4cae85b2; CNZZDATA1254842228=79363608-1578295144-https%253A%252F%252Fm.qichacha.com%252F%7C1578295144; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1578040179,1578288898,1578295938; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201578295937637%2C%22updated%22%3A%201578295968430%2C%22info%22%3A%201578295937640%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22m.qichacha.com%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1578295969"
        })



    def get_req(self,url):
        """
        get请求封装
        :param url:
        :return:
        """
        count = 3
        while count:
            try:
                proxies = ABY()
                resp = self.session.get(url,proxies=proxies,timeout=3)
                if resp.status_code == 200:
                    resp.encoding = 'utf-8'
                    return resp.text
                else:
                    print(resp.status_code)

                count -= 1
            except Exception as e:
                log.info(e)

    def base_get(self):
        """
        首次请求
        :param
        :return:
        """
        try:
            count = 1
            while count:
                url = f'https://m.qichacha.com/search?key={self.keys}'
                resp = self.get_req(url)
                etre = HTML(resp)
                a_lt = etre.xpath('//div[@class="list-item"]/ancestor::a/@href')
                etrelt = etre.xpath('//div[@class="list-item"]//div[@class="list-item-name"]')
                if a_lt:
                    return a_lt,etrelt
                else:
                    pass
                count -= 1
        except Exception as e:
            print(e)

    def spider_run_jbxx(self):
        a_lt,etrelt = self.base_get()
        index = 0
        companys = None
        for _ in etrelt:
            name = "".join(_.xpath('.//text()')).strip(" ").replace("\n","")

            if name == self.keys:
                companys = name
                break
            index += 1
        print(companys)
        if companys:
            url = "https://m.qichacha.com" + a_lt[index]
            resp = self.get_req(url)
            #
            RUN = QCC_XPATH(resp,self.keys)
            dict = RUN.gsxx()
            return dict
        else:
            return False


# def main():
#
#     key = "阿里巴巴"
#     RUN = QCC(keys=key)
#     resp = RUN.spider_run_jbxx()
# if __name__ == '__main__':
#     main()
