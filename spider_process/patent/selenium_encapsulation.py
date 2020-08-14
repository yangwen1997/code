from selenium.webdriver.common.action_chains import ActionChains

class Encap(object):

    def __init__(self,browser):
        self.browser = browser
        self.browser.implicitly_wait(20)

    def move_to(self,target,types):
        """移动方法属性封装
        :param target 目标
        :param types 规则类型
        """
        try:
            target_to = None
            if types == "xpath":
                target_to = self.browser.find_element_by_xpath(target)
            elif types == "css":
                target_to = self.browser.find_element_by_css_selector(target)
            ActionChains(self.browser).move_to_element(target_to).perform()

        except Exception as e:
            print("匹配语法错误-移动方法")

    def click_to(self,target,types):
        """
        点击方法
        :param target:
        :param types:
        :return:
        """
        try:

            target_to = None
            if types == 'xpath':
                self.browser.find_element_by_xpath(target).click()
            elif types == 'css':
                self.browser.find_element_by_css_selector(target).click()

        except Exception as e:
            print("匹配语法错误-点击方法")


    def send_keys(self,target,types,msg):
        """
        向页面填充数据，模拟人工，缺点慢，无需模拟时尽量使用js填充
        :param msg :填充的内容
        """
        try:
            if types == 'xpath':

                self.browser.find_element_by_xpath(target).send_keys(msg)
            elif types == 'css':
                pass
        except Exception as e:
            pass

    def windows_to_page(self):
        """
        页面跳转，默认跳到为-1
        :return:
        """
        try:
            self.browser.switch_to.window(self.browser.window_handles[-1])
        except Exception as e:
            print("窗口跳转错误")

    def selenium_execjs(self,js):
        """
        js 执行
        :return:
        """
        try:
            self.browser.execute_script(js)
        except Exception as e:
            print("js语句错误，请检查")

    def selenium_close(self):
        """
        关闭浏览器
        :return:
        """
        try:
            self.browser.close()
        except:
            pass
    def selenium_text(self):
        """获取页面信息"""
        try:
            return self.browser.page_source
        except:
            pass