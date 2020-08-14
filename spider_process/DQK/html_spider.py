#encoding=utf-8
'''
@author yangwenlong
'''

import time
import pymongo
import hashlib
import re

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from lxml.etree import HTML,tostring

MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
# JXS_IP = MONGO_DB["DQK"]["JXS"]
JXS_IP = MONGO_DB["DQK"]["jxs_test"]
TJ_IP = MONGO_DB["DQK"]["TJ"]

class dqkspider(object):
    """抓取 精线索/探迹/CRM 的h5页面初始化累"""

    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(dqkspider, *args, **kwargs)
            cls._instance.chrome_options = Options()
            cls._instance.chrome_options.add_argument('--no-sandbox')
            cls._instance.chrome_options.add_argument('--disable-dev-shm-usage')
            cls._instance.chrome_options.binary_location = r"D:\software\chrome\TSBrowser\TSBrowser.exe"
            cls._instance.browser = webdriver.Chrome(executable_path=r'D:\software\chromedriver\chromedriver.exe',
                                       chrome_options=cls._instance.chrome_options)
            # url: 登陆页面url,js
            cls._instance.dicts = {
                "精线索":"http://sales.jingxiansuo.com/#/user/login",
                "CRM":"https://ukuaiqi.com/login",
                "探迹":"https://user.tungee.com/users/sign-in",
            }
            cls._instance.jsdict = {
                "精线索":[
                    "document.getElementById('username').value='15882449235'",
                    "document.getElementById('password').value='19881121';",
                ],
                "CRM":[],
                "探迹":[
                    "document.querySelectorAll('.ant-input')[0].value='15882449235';",
                    "document.querySelectorAll('.ant-input')[1].value='Dgg962540';",
                ],
            }
        return cls._instance

    def _login(self,Name):
        """登陆处理逻辑"""

        self.browser.implicitly_wait(10)
        URL = self.dicts.get(Name)
        js_lt = self.jsdict.get(Name)
        self.browser.get(URL)

        try:
            # 登录处理逻辑
            count = 0
            for _ in js_lt:
                time.sleep(0.5)
                if Name == "精线索":
                    if Name == "精线索" and (count==0 or count == 1):
                        self.browser.find_element_by_xpath('//input[@id="username"]').click() if count == 0 \
                            else self.browser.find_element_by_xpath('//input[@id="password"]').click()

                    self.browser.execute_script(_)
                if Name == "探迹":
                    if count == 0:
                        self.browser.find_elements_by_css_selector(".ant-input")[0].click()
                        self.browser.find_elements_by_css_selector(".ant-input")[0].send_keys("15882449235")
                    else:
                         self.browser.find_elements_by_css_selector(".ant-input")[1].click()
                         self.browser.find_elements_by_css_selector(".ant-input")[1].send_keys("Dgg962540")

                count += 1


            if Name == "精线索":
                # self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div/div[2]/form/div[4]/div/div/span/button').click()
                self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/form/button').click()

            elif Name == "探迹":
                # 开始位置：定位到元素的原位置
                source = self.browser.find_element_by_xpath('//input[@placeholder="请输入密码"]')

                # 结束位置：定位到元素要移动到的目标位置
                target = self.browser.find_element_by_xpath("//button")

                # 执行元素的拖放操作
                ActionChains(self.browser).drag_and_drop(source, target).perform()

                self.browser.find_element_by_xpath('//button').click()

        except Exception as e:
            print(f"程序异常：{e}")
        else:
            return self.browser


class jxs:

    # 获取精线索的数据格式信息
    def __init__(self):
        self.browser = dqkspider()._login(Name="精线索")
        self.Hierarchy = 0

    def rule(self,xpat,parttens,content,no_dict,item):
        """判断规则
        :param parttens: selenium 对象
        :param parttens：xpath匹配规则
        :param content获取的对象值
        :param no_dict 继承父类的字典
        :param item 存储的字典
        :param Hierarchy 层级字典名字

        """

        sign = xpat.find_element_by_xpath(parttens).get_attribute(content)

        Hierarchy = "Hierarchy" + "_" + str(self.Hierarchy)
        self.Hierarchy += 0
        while 1:
            if sign == no_dict["sucess"]:

                # 有三级分类点击把三级分类存入列表
                item[Hierarchy] = xpat.find_element_by_xpath('./span[3]').get_attribute("title")
                xpat.find_element_by_xpath(".//span[1]").click()
                spans = self.browser.find_elements_by_xpath('//ul[@class="ant-select-tree-child-tree ant-select-tree-child-tree-open"]/li/span[@class="ant-select-tree-node-content-wrapper ant-select-tree-node-content-wrapper-normal"]')
                thre = []
                for i in spans:
                    thre.append(i.text)
                xpat.find_element_by_xpath(".//span[1]").click()
                Hierarchy = "Hierarchy" + "_" + str(self.Hierarchy)
                item[Hierarchy] = thre


            elif sign == no_dict["err"]:
                item[Hierarchy] = xpat.find_element_by_xpath('./span[3]').get_attribute("title")
                break


    def spider_run(self):


        self.browser.find_element_by_xpath('//*[@id="layout"]/main/div/div[2]/div/div[1]/div/div/div[2]/div[2]/a[1]').click()

        # 获取所有的大分类 并删除第一个常用分类导航
        title = self.browser.find_elements_by_xpath('//div[@class="ant-tabs-nav ant-tabs-nav-animated"]//div[@role="tab"]')
        del title[0]

        category_lt = []
        for x in range(len(title)):
            dict = {}
            time.sleep(0.5)
            title[x].click()
            dict["title"] = x
            dict["name"] = title[x].text
            second_title = self.browser.find_elements_by_xpath('//div[@aria-hidden="false"]//div[@class="itemContent___1ARy5"]')
            dict["counts"] = len(second_title)
            category_lt.append(dict)
            if x == 12:
                second_title[0].click()
                self.browser.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary']").click()

        no_dict = {
            "li_1":"ant-select-tree-treenode-switcher-close",
            "li_2":"ant-select-dropdown-menu-item ant-select-dropdown-menu-item-active",
            "sucess":"ant-select-tree-node-content-wrapper ant-select-tree-node-content-wrapper-close",
            "err":"ant-select-tree-node-content-wrapper ant-select-tree-node-content-wrapper-normal",
        }

        for p in category_lt:
            name = p["name"]
            for x in range(p["counts"]):
                time.sleep(0.5)

                # 点击二级标题
                self.browser.find_element_by_xpath("//div[@class='contentItemRight___3ijnw']//span[@class='ant-cascader-picker-label']").click()
                js = f"document.querySelectorAll('.ant-cascader-menu')[0].querySelectorAll('li')[{str(int(p['title'] + 1))}].click()"
                self.browser.execute_script(js)
                jss = f"document.querySelectorAll('.ant-cascader-menu')[1].querySelectorAll('li')[{x}].click()"
                self.browser.execute_script(jss)
                print(name)

                span = self.browser.find_elements_by_xpath('//div[@class="contentItemRight___3ijnw"]/span')
                if len(span) == 2:
                    resp_text = self.browser.find_element_by_xpath('//div[@class="contentItemRight___3ijnw"]//span[2]').text
                    if resp_text == "请选择":
                        items = {}

                        self.browser.find_element_by_xpath('//div[@class="contentItemRight___3ijnw"]//span[2]').click()
                        three_tit = self.browser.find_elements_by_xpath('//ul[@role="listbox"]/li|//div[@role="listbox"]/ul/li')

                        # 判断li标签的class属性
                        t_li = three_tit[0].get_attribute("class")
                        items["secondname"] = self.browser.find_element_by_xpath("//div[@class='contentItemRight___3ijnw']//span[@class='ant-cascader-picker-label']").text
                        items["baseName"] = name
                        if t_li == no_dict["li_1"]:
                            for _ in three_tit:
                                item = {}
                                item["secondname"] = items["secondname"]
                                item["baseName"] = items["baseName"]
                                sign = _.find_element_by_xpath('./span[3]').get_attribute("class")
                                if sign == no_dict["sucess"]:

                                    # 有三级分类点击把三级分类存入列表
                                    item["second_name"] = _.find_element_by_xpath('./span[3]').get_attribute("title")
                                    _.find_element_by_xpath(".//span[1]").click()
                                    spans = self.browser.find_elements_by_xpath('//ul[@class="ant-select-tree-child-tree ant-select-tree-child-tree-open"]/li')
                                    thre = []
                                    for i in spans:
                                        itemss = {}

                                        # 第三级可以继续点击
                                        if i.find_element_by_xpath(".//span[3]").get_attribute("class") ==  no_dict["sucess"]:
                                            itemss["name"] = i.text
                                            i.find_element_by_xpath(".//span[1]").click()
                                            four_span = self.browser.find_elements_by_xpath('//ul[@class="ant-select-tree-child-tree ant-select-tree-child-tree-open"]/li/ul/li/span[3]')

                                            # 处理四级分类
                                            four_lts = []
                                            for four in four_span:
                                                four_lts.append(four.text)
                                            itemss[ itemss["name"]] = four_lts

                                            i.find_element_by_xpath(".//span[1]").click()

                                        elif i.find_element_by_xpath(".//span[3]").get_attribute("class") == no_dict["err"]:
                                            itemss["name"] = i.text

                                        thre.append(itemss)

                                    _.find_element_by_xpath(".//span[1]").click()

                                    item["three_name"] = thre


                                elif sign == no_dict["err"]:
                                    item["second_name"] = _.find_element_by_xpath('./span[3]').get_attribute("title")

                                JXS_IP.save(item)
                        elif t_li == no_dict["li_2"]:
                            # 抓取只有文本的分类
                            item = {}
                            item["secondname"] = items["secondname"]
                            item["baseName"] = items["baseName"]

                            four_lt = []
                            for _ in three_tit:
                                text = _.text
                                four_lt.append(text)
                            item["min_categorys"] = four_lt
                            print(item)
                            JXS_IP.save(item)


                # 打印出那个分类抓取完成
                secondname = self.browser.find_element_by_xpath("//div[@class='contentItemRight___3ijnw']//span[@class='ant-cascader-picker-label']").text
                print(f"{secondname} 完成....")



class tj:
    """
    探迹数据格式获取类
    """
    def __init__(self):
        self.browser = dqkspider()._login(Name="探迹")

    def mouse_move(self,end_xpath):
        # source = self.browser.find_element_by_xpath(start_xpath)
        #
        # # 结束位置：定位到元素要移动到的目标位置
        # target = self.browser.find_element_by_xpath(end_xpath)
        #
        # # 执行元素的拖放操作
        # ActionChains(self.browser).drag_and_drop(source, target).perform()

        ends = self.browser.find_element_by_xpath(end_xpath)
        ActionChains(self.browser).move_to_element(ends).perform()

    def save_to_mongo(self,xpaths,name):
        """获取html存入mongodb数据库"""
        etre = HTML(self.browser.page_source)
        item = {}
        div = etre.xpath(xpaths)[0]
        div_str = tostring(div, encoding='utf-8')
        resp = bytes.decode(div_str)
        item["_id"] = hashlib.md5(name.encode('utf-8')).hexdigest()
        item["html"] = resp
        item["Name"] = name
        TJ_IP.save(item)

    def spider_run(self):

        #  分别点击探迹拓客
        self.browser.find_element_by_xpath('//*[@id="app-content"]/div[1]/div[2]/div[2]/div/div[2]/button').click()

        # self.browser.find_element_by_xpath('//*[@id="/customer-seeking$Menu"]/li[1]/div/span').click()#企业查询

        # 行业分类前缀
        # xpaths = '//div[@class="_2KZXu"]/ul'
        # name = '探迹-探迹行业分类前缀'
        # self.save_to_mongo(xpaths,name)
        #
        # xpaths = '//div[@class="_3Tic2"]//div[@class="ScrollbarsCustom-Content"]/ul'
        #
        # name = '探迹-工业器械及材料'
        # self.save_to_mongo(xpaths,name)
        #
        # start = '//div[@class="_2KZXu"]/ul/li[1]'
        # end = '//div[@class="_2KZXu"]/ul/li[2]'
        # self.mouse_move(start,end)
        # name = '探迹-日用百货'
        # self.save_to_mongo(xpaths,name)
        #
        #
        # start = '//div[@class="_2KZXu"]/ul/li[2]'
        # end = '//div[@class="_2KZXu"]/ul/li[3]'
        # self.mouse_move(start,end)
        # name = '探迹-其他消费品'
        # self.save_to_mongo(xpaths,name)

        # start = '//div[@class="_2KZXu"]/ul/li[1]'
        # end = '//div[@class="_2KZXu"]/ul/li[4]'
        # self.mouse_move(start,end)
        # name = '探迹-租赁/商务服务'
        # self.save_to_mongo(xpaths,name)

        # start = '//div[@class="_2KZXu"]/ul/li[1]'
        # end = '//div[@class="_2KZXu"]/ul/li[5]'
        # self.mouse_move(start,end)
        # name = '探迹-建筑'
        # self.save_to_mongo(xpaths,name)
        #
        # start = '//div[@class="_2KZXu"]/ul/li[5]'
        # end = '//div[@class="_2KZXu"]/ul/li[6]'
        # self.mouse_move(start,end)
        # name = '探迹-计算机/互联网'
        # self.save_to_mongo(xpaths,name)



        # 企业类型
        # xpaths = '//div[@class="YIyq3"]'
        # name = '探迹-企业类型'
        # self.save_to_mongo(xpaths, name)

        # 企业信息全部页面
        # xpaths = '//div[@id="usedBySidebarInBasicformation"]'
        # name = "探迹-企业信息全部页面"
        # self.save_to_mongo(xpaths, name)
        # self.browser.find_element_by_xpath('//*[@id="/customer-seeking$Menu"]/li[2]/div/span').click() #店铺查询


        # 店铺分类
        # xpaths = '//div[@class="_3fKkP"]/ul'
        # name = '探迹-店铺分类'
        # self.save_to_mongo(xpaths, name)
        # print(self.browser.page_source)

        self.browser.find_element_by_xpath('//*[@id="usedBySidebarInBasicformation"]/div[2]/div[2]/div/div/ul/li[4]/div').click()

        # 条件选择
        self.browser.find_element_by_xpath('//*[@id="advanced-filter"]/div[4]/div/div/div/div/div[2]/div/a').click()

        self.browser.find_element_by_xpath('//button[@class="ant-btn ant-btn-default"]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//*[@id="ddd"]/a/div/div/div/div').click()

        # 选择联系人渠道
        end = '//*[@id="tab_menu"]/div/div[1]/div/div/div/div/div[1]/div[3]/div/a'
        self.mouse_move(end)
        end = '//*[@id="ddd"]/div/div/div/div/div[3]/div/a[4]/span'
        # self.mouse_move(end)

        self.browser.find_element_by_xpath(end).click()

        self.browser.find_element_by_xpath("//span[@class='ant-select-search__field__placeholder']").click()

        li_st = self.browser.find_elements_by_xpath("//ul[@class='ant-select-tree']/li/span[1]")

        for _ in li_st:
            _.click()

        etre = HTML(self.browser.page_source)
        resp = etre.xpath("//ul[@class='ant-select-tree']/li/ul")
        title_resp = etre.xpath("//ul[@class='ant-select-tree']/li/span//text()")
        for _ in range(len(title_resp)):
            item = {}
            item["Name"] = title_resp[_]
            item["_id"] = hashlib.md5(title_resp[_].encode('utf-8')).hexdigest()
            div_str = tostring(resp[_], encoding='utf-8')
            item["html"] = bytes.decode(div_str)
            TJ_IP.save(item)
            # print(item)
        # name = '资质证书'
        # self.save_to_mongo(xpaths, name)

        # 媒体信息
        # end = '//*[@id="tab_menu"]/div/div[1]/div/div/div/div/div[1]/div[8]/div/a'
        # self.mouse_move(end)
        # name = '媒体信息'
        # self.save_to_mongo(xpaths, name)

        # 推广信息
        # end = '//*[@id="tab_menu"]/div/div[1]/div/div/div/div/div[1]/div[9]/div/a'
        # self.mouse_move(end)
        # name = '推广信息'
        # self.save_to_mongo(xpaths, name)

        # 产品信息
        # end = '//*[@id="tab_menu"]/div/div[1]/div/div/div/div/div[1]/div[10]/div/a'
        # self.mouse_move(end)
        # name = '产品信息'
        # self.save_to_mongo(xpaths, name)

        # 风险信息
        # end = '//*[@id="tab_menu"]/div/div[1]/div/div/div/div/div[1]/div[11]/div/a'
        # self.mouse_move(end)
        # name = '风险信息'
        # self.save_to_mongo(xpaths, name)

        # 知识产权
        # end = '//*[@id="tab_menu"]/div/div[1]/div/div/div/div/div[1]/div[12]/div/a'
        # self.mouse_move(end)
        # name = '知识产权'
        # self.save_to_mongo(xpaths, name)


        # self.browser.find_element_by_xpath('//*[@id="tab_menu"]/div/div[1]/div/span[2]/span/i/svg').click()


run = jxs()
run.spider_run()