import os
import json
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from cookiespool.config import *
from cookiespool.db import RedisClient
from pyvirtualdisplay import Display
from login.WeChat.test import WeChatCookies

class CookiesGenerator(object):
    def __init__(self, website='default'):
        """
        父类, 初始化一些对象
        :param website: 名称
        :param browser: 浏览器, 若不使用浏览器则可设置为 None
        """
        self.website = website
        self.cookies_db = RedisClient('cookies', self.website)
        self.accounts_db = RedisClient('accounts', self.website)
        self.init_browser()

    def __del__(self):
        #self.close()
        pass
    
    def init_browser(self):
        """
        通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        if BROWSER_TYPE == 'PhantomJS':
            caps = DesiredCapabilities.PHANTOMJS
            caps[
                "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
            self.browser = webdriver.PhantomJS('/Users/ahua/Desktop/phantomjs/bin/phantomjs',desired_capabilities=caps)
            self.browser.set_window_size(500, 1400)
        elif BROWSER_TYPE == 'Chrome':
            self.display = Display(visible=0, size=(800, 800))
            self.display.start()
            self.option = webdriver.ChromeOptions()
            self.option.add_argument('--no-sandbox')
            self.browser  = webdriver.Chrome(executable_path='/users/lichao/Toolkit/driver/chromedriver_wechat', chrome_options=self.option)


    
    def new_cookies(self, username, password):
        """
        新生成Cookies，子类需要重写
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError
    
    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        return cookies
    
    def run(self):
        """
        运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        accounts_usernames = self.accounts_db.usernames()
        # print(accounts_usernames)
        cookies_usernames = self.cookies_db.usernames()
        # print(cookies_usernames)
        for username in accounts_usernames:
            if not username in cookies_usernames:
                password = self.accounts_db.get(username)
                print('正在生成Cookies', '账号', username, '密码', password)
                result = self.new_cookies(username, password)
                # 成功获取
                if result.get('status') == 1:
                    cookies = self.process_cookies(result.get('content'))
                    print('成功获取到Cookies', cookies)
                    if self.cookies_db.set(username, json.dumps(cookies)):
                        print('成功保存Cookies')
                # 密码错误，移除账号
                elif result.get('status') == 2:
                    print(result.get('content'))
                    if self.accounts_db.delete(username):
                        print('成功删除账号')
                else:
                    print(result.get('content'))
        else:
            print('所有账号都已经成功获取Cookies')
    
    def close(self):
        """
        关闭
        :return:
        """
        try:
            print('Closing Browser')
            self.browser.close()
            del self.browser
            os.system('pkill -f "/users/lichao/Toolkit/driver/chromedriver"')
            os.system('pkill -f "/opt/google/chrome/chrome"')
            os.system('pkill -f "/usr/bin/google-chrome"')
        except TypeError:
            print('Browser not opened')
        
        try:
            print('Closing Display')
            self.display.stop()
            del self.display
        except TypeError:
            print('Display not opened')
            
class WeChatCookiesGenerator(CookiesGenerator):

    def __init__(self, website='WeChat'):

        CookiesGenerator.__init__(self, website)
        self.website = website

    def new_cookies(self, username, password):
        """
        生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        return WeChatCookies(username, password,self.browser).main()
