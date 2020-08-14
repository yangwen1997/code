import re
import gc


from sbj.common import sbjws_base


class sbj_spider(sbjws_base):

    def fun_zcws(self):
        """
         商标注册审查决定文书列表页爬虫程序
        :return:
        """
        sum = 283
        while self.page <= self.pagenum:
            url = 'http://wssq.sbj.cnipa.gov.cn:9080/tmsve/zccw_getMain.xhtml'
            data = {
                "param.regNum": "",
                "param.tmName": "",
                "param.appCnName": "",
                "param.agentName": "",
                "param.startDate": "",
                "param.endDate": "",
                "pagenum": f"{str(self.page)}",
                "pagesize": "30",
                "sum": str(sum),
                "countpage": "4",
                "gopage": "1"
            }
            try:
                resp = self.post_req(url, data)
                if resp:

                    if self.page == 1:
                        # 替换页码为实际页数
                        self.pagenum = int(re.findall("&nbsp;共(\d+)页&nbsp;", resp.text)[0])

                    if self.pageTotal == 2:
                        # 替换数据总数量
                        self.pageTotal = re.findall('共 <font color="red">(\d+)</font>条记录', resp.text)[0]

                    urllt, nametext = self.urlxpath(resp)

                    lt = []
                    for _ in range(0,len(urllt)):
                        a = "http://wssq.sbj.cnipa.gov.cn:9080" + urllt[_]
                        lt.append(a)
                        self.urlltsave(urllt[_], nametext[_], category="商标注册审查决定文书")
                    print(lt)
                    self.log.info(f"第{str(self.page)}页数据抓取完毕")
                    self.page += 1

                    # 垃圾回收，释放无效的引用计数，最大化减少程序卡顿问题
                    gc.collect()
                else:
                    self.log.info("页面无数据或请求三次失败")
            except Exception as e:
                print(f"当前抓取到第{str(self.page)}页数据时出错")

    def fun_sbyyjd(self):
        """
        商标异议决定书列表页爬虫程序
        :return:
        """
        sum = 38294
        while self.page <= self.pagenum:

            url = 'http://wssq.sbj.cnipa.gov.cn:9080/tmsve/yycw_getMain.xhtml'
            data = {
                "param.regNum": "",
                "param.tmName": "",
                "param.appCnName": "",
                "param.agentName": "",
                "param.startDate": "",
                "param.endDate": "",
                "pagenum": f"{str(self.page)}",
                "pagesize": "30",
                "sum": str(sum),
                "countpage": "1277",
                "gopage": "2"
            }
            try:
                resp = self.post_req(url, data)
                if resp:

                    if self.page == 1:
                        # 替换页码为实际页数
                        self.pagenum = int(re.findall("&nbsp;共(\d+)页&nbsp;", resp.text)[0])

                    if self.pageTotal == 2:
                        # 替换数据总数量
                        self.pageTotal = re.findall('共 <font color="red">(\d+)</font>条记录', resp.text)[0]

                    urllt, nametext = self.urlxpath(resp)

                    for _ in range(len(urllt)):
                        self.urlltsave(urllt[_], nametext[_], category="商标异议决定文书")
                    self.log.info(f"第{str(self.page)}页数据抓取完毕")
                    self.page += 1

                    # 垃圾回收，释放无效的引用计数，最大化减少程序卡顿问题
                    gc.collect()
                else:
                    self.log.info("页面无数据或请求三次失败")
            except Exception as e:
                print(f"当前抓取到第{str(self.page)}页数据时出错")

    def fun_sbps(self):
        """
        商标评审文书列表页爬虫程序
        :return:
        """
        sum = 701597
        self.page = 4
        # self.pagenum = 1631
        self.pagenum = 200
        while self.page <= self.pagenum:
            url = 'http://wssq.sbj.cnipa.gov.cn:9080/tmsve/pingshen_getMain.xhtml'
            data = {
                "param.regNum": "",
                "param.tmName": "",
                "param.appCnName": "",
                "param.agentName": "",
                "param.startDate": "2020-04-01",
                "param.endDate": "2020-07-17",
                "pagenum": f"{str(self.page)}",
                "pagesize": "30",
                "sum": str(sum),
                "countpage": "1631",
                "gopage": "1"
            }
            try:
                resp = self.post_req(url, data)
                if resp:

                    if self.page == 1:
                        # 替换页码为实际页数
                        self.pagenum = int(re.findall("&nbsp;共(\d+)页&nbsp;", resp.text)[0])

                    if self.pageTotal == 2:
                        # 替换数据总数量
                        self.pageTotal = re.findall('共 <font color="red">(\d+)</font>条记录', resp.text)[0]

                    urllt, nametext = self.urlxpath(resp)

                    for _ in range(len(urllt)):
                        self.urlltsave(urllt[_], nametext[_], category="商标评审裁定/决定文书")
                    self.log.info(f"第{str(self.page)}页数据抓取完毕")
                    self.page += 1

                    # 垃圾回收，释放无效的引用计数，最大化减少程序卡顿问题
                    gc.collect()
                else:
                    self.log.info("页面无数据或请求三次失败")
            except Exception as e:
                print(f"当前抓取到第{str(self.page)}页数据时出错")

    def to_redis(self):
        category = "商标评审裁定/决定文书"
        self.fun_to_redis(category)

    def data_info(self,category_index):
        """
        详情页面数据抓取
        :return:
        """

        category_dict = {
            "商标注册审查决定文书": "scjd_urlDB",
            "商标异议决定文书": "yyjd_urlDB",
            "商标评审裁定/决定文书":"sbps_urlDB"
        }

        redis_name = category_dict[category_index]
        self.fun_spider_dateInfo(redis_name)


import threading
def work():
    st = sbj_spider()
    # st.data_info("商标评审裁定/决定文书")
    # st.to_redis()
    st.data_info(category_index="商标评审裁定/决定文书")
for i in range(11):
    t = threading.Thread(target=work)
    t.start()
    print("please wait!")
    # t.join()


# import asyncio
# async def main():
#     # await st.to_redis()
#     await st.data_info('商标评审裁定/决定文书')
# coun = [main() for _ in range(0,15)]
# tasks = [asyncio.ensure_future(_) for _ in coun]
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))