import time
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium_encapsulation import Encap

class zyLogin():

    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(zyLogin, *args, **kwargs)
            cls._instance.chrome_options = Options()
            cls._instance.chrome_options.add_argument('--no-sandbox')
            cls._instance.chrome_options.add_argument('--disable-dev-shm-usage')
            cls._instance.chrome_options.binary_location = r"D:\software\chrome\TSBrowser\TSBrowser.exe"
            cls._instance.browser = webdriver.Chrome(executable_path=r'D:\software\chromedriver\chromedriver.exe',
                                       chrome_options=cls._instance.chrome_options)
            cls._instance.url = 'https://www.incopat.com/newLogin'
        return cls._instance

    def login(self):
        """登录"""

        self.browser.get(self.url)
        self.browser.execute_script("document.getElementById('u').click();document.getElementById('u').value = 'dggzy01';document.getElementById('p').value = '746740';document.getElementById('loginBtn').click()")

        try:
            time.sleep(1)
            alert = self.browser.switch_to.alert
            alert.accept()
            time.sleep(3)

        except Exception as e:
            print("没有alert弹窗")
        finally:

            return self.browser

class pytterter_spider(Encap):


    def run(self,startTime='20000101',endTime='20000201'):
        """
        专利程序入口函数
        :return:
        """
        # 点击 高级搜索并选择指定条件
        self.move_to(target='//div[@class="menu"]//a[@class="checked"]',types='xpath')
        self.click_to(target='//*[@id="container_simple"]/div[1]/div[3]/div/div[2]/ul/li[2]/ol/li[2]/a',types='xpath')
        self.click_to(target='//select[@id="date_select"]',types='xpath')
        self.click_to(target='//select[@id="date_select"]/option[1]',types='xpath')
        self.click_to(target='//input[@id="datepicker"]',types='xpath')
        self.send_keys(target='//input[@id="datepicker"]',types='xpath',msg=str(startTime))
        self.send_keys(target='//input[@id="datepicker1"]',types='xpath',msg=str(endTime))
        self.click_to(target='//input[@id="checkall"]',types='xpath')
        self.click_to(target='//input[@id="zhcn"]',types='xpath')

        # 点击跳转到详情页并展示100条数据每页
        self.click_to(target='.button >.retrieval',types='css')
        time.sleep(5)
        self.selenium_execjs(js="document.querySelectorAll('.page_left > a')[2].click()")

        # 获取数据并进行逻辑处理
        self.get_info()

    def get_info(self):
        try:
            data_info = self.browser.find_elements_by_xpath('//div[@class="title-name"]/a')

            for _ in data_info:
                # 点击详情
                _.click()
                self.windows_to_page()
                print(self.selenium_text())
                self.selenium_close()
                self.windows_to_page()

        except Exception as e:
            pass


spider = pytterter_spider(zyLogin().login())
spider.run()

