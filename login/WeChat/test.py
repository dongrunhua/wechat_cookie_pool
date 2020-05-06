import time
import os
import json
import re
from PIL import Image
from selenium import webdriver
from lxml import html



class WeChatCookies(object):

    def __init__(self, username, password,browser):
        self.username = username
        self.password = password
        self.Browner  = browser


    # 获取cookie
    def get_cookie(self):
        
        self.Browner.delete_all_cookies()
        
        url = 'https://mp.weixin.qq.com'

        self.Browner.get(url)
        # 获取账号输入框
        ID = self.Browner.find_element_by_name('account')
        # 获取密码输入框
        PW = self.Browner.find_element_by_name('password')

        ID.send_keys(self.username)
        PW.send_keys(self.password)
        # 获取登录button，点击登录
        self.Browner.find_element_by_class_name('btn_login').click()

        # 等待扫二维码
        time.sleep(5)
        current_url = self.Browner.current_url
        print(current_url)
        # 获取二维码
        os.system("rm /users/Server/wechat_cookie/erweima/*")
        self.Browner.save_screenshot('erweima/'+self.username+'.png')

        while 1:
            current_url = self.Browner.current_url
            print(current_url)
            if re.search('token=\d+',current_url):
                ck = self.Browner.get_cookies()
                ck = { i['name']:i['value'] for i in ck }
                self.html = self.Browner.page_source
                return ck
            time.sleep(1)

    # 获取token，在页面中提取
    def Token(self,cookie):
        etree = html.etree
        h = etree.HTML(self.html)
        url = h.xpath('//a[@title="首页"]/@href')[0]
        token = re.findall('\d+',url)[0]
        cookie['token'] = token
        cookie['count'] = '0'
        return cookie

    def main(self):
        cookie = self.get_cookie()
        cookie = self.Token(cookie)

        result = {
            "status": 1,
            'content': cookie
        }

        return result


if __name__ == '__main__':
    webdriver = webdriver.Chrome(executable_path='/users/lichao/Toolkit/driver/chromedriver_wechat', chrome_options=self.option)
    username = ''
    password = ''
    WeChat = WeChatCookies(username, password,webdriver)
    print(WeChat.main())