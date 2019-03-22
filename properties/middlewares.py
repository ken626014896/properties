# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium .common.exceptions import NoSuchElementException
import  urllib
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL  import  Image

class PropertiesSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PropertiesDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from selenium.common.exceptions import TimeoutException

#公众号的中间件
class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        # hint=0
        # if "profile" in request.url:
        # hint = 1
        if spider.name == 'test1' :

            try:
                spider.browser.get(request.url)
               # spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            except TimeoutException as e:
                print('超时')
                spider.browser.execute_script('window.stop()')
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8",
                                request=request)

#pixiv的中间件
class JavaScriptMiddlewareOfPixiv(object):
    def process_request(self, request, spider):
        hint=0
        if "member_illust" in request.url:
            hint = 1
        if spider.name == 'pixiv' and hint ==1:

            try:

                spider.browser.get(request.url)

            except TimeoutException as e:
                print('超时')
                spider.browser.execute_script('window.stop()')

            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8",
                                request=request)

#测试的中间件
import json
class TestMiddleware(object):
    def process_request(self, request, spider):

        if spider.name == 'test3':

            try:

                spider.browser.get(request.url)


                captcha_msg = spider.browser.find_element_by_xpath('//*[@class="p2"]')
                # while captcha_msg:
                while captcha_msg:

                        print(captcha_msg.text)
                        spider.browser.get_screenshot_as_file('hahaha.jpg')


                        wait = WebDriverWait(spider.browser, 10)
                        input_captcha = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="seccodeInput"]')))
                        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]')))

                        print(input_captcha.tag_name,submit_button.tag_name)
                        # input_captcha= spider.browser.find_element_by_xpath('//*[@id="seccodeInput"]')
                        # submit_button=spider.browser.find_element_by_xpath('//*[@id="submit"]')
                        captcha_pic = spider.browser.find_element_by_xpath('//*[@id="seccodeImage"]')
                        # captcha_pic_url = captcha_pic.get_attribute('src')
                        # with open('captcha_pic.png', 'wb') as fp:
                        #     res = urllib.request.urlopen(url=captcha_pic_url)
                        #     fp.write(res.read())
                        left = captcha_pic.location['x']
                        top = captcha_pic.location['y']
                        right = captcha_pic.location["x"] + captcha_pic.size['width']
                        bottom = captcha_pic.location['y'] + captcha_pic.size['height']
                        im = Image.open('hahaha.jpg')
                        im = im.crop((left, top, right, bottom))
                        im.save('hahaha.jpg')

                        spider.browser.get_screenshot_as_file('hahaha2.jpg')
                        temp = input('输入验证码:')
                        input_captcha.send_keys(temp)
                        spider.browser.get_screenshot_as_file('hahaha3.jpg')
                        # submit_button.click()

                        submit_button.send_keys(Keys.ENTER)
                        # js = 'document.getElementById("submit").click();'
                        # spider.browser.execute_script(js)

                        spider.browser.get_screenshot_as_file('hahaha4.jpg')
                        time.sleep(10)

                        spider.browser.get_screenshot_as_file('hahaha5.jpg')

                        captcha_msg = spider.browser.find_element_by_xpath('//*[@class="p2"]')
                return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                        encoding="utf-8",
                                        request=request)

            except NoSuchElementException as e:
                    return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
                                        encoding="utf-8",
                                        request=request)
               # spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            except TimeoutException as e:
                print('超时')
                spider.browser.execute_script('window.stop()')

            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8",
                                request=request)



from fake_useragent import UserAgent
#这是一个随机UserAgent的包，里面有很多UserAgent
class RandomUserAgentMiddleware(object):

    def __init__(self, crawler):

        super(RandomUserAgentMiddleware, self).__init__()


        self.ua = UserAgent()

        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')  # 从setting文件中读取RANDOM_UA_TYPE值




    @ classmethod
    def from_crawler(cls, crawler):

        return cls(crawler)



    def process_request(self, request, spider):

        def get_ua():


            '''Gets random UA based on the type setting (random, firefox…)'''


            return getattr(self.ua, self.ua_type)

        hint = 0
        if "profile" in request.url:
            hint = 1
        if spider.name == 'test1' and hint == 1:
            user_agent_random = get_ua()

            request.headers.setdefault('User-Agent', user_agent_random)  # 这样就是实现了User-Agent的随即变换





import random
class MyproxiesSpiderMiddleware(object):

    def process_request(self, request, spider):
        if spider.name=="test2":
            '''对request对象加上proxy'''
            proxy = self.get_random_proxy()
            print("this is request ip:" + proxy)
            request.meta['proxy'] = proxy



    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if spider.name == "test2":
            print("this is test2")
            if response.status != 200:
                proxy = self.get_random_proxy()
                print("this is response ip:" + proxy)
                # 对当前reque加上代理
                request.meta['proxy'] = proxy
                return request
            else:
                print("this is 200")

            return response


    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        while 1:
            with open('proxies.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        return proxy













import random
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware #代理ip，这是固定的导入
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware #代理UA，固定导入


class IPPOOLS(HttpProxyMiddleware):
   def __init__(self,ip=''):
       '''初始化'''
       self.ip=ip
   def process_request(self, request, spider):
       if spider.name == "test2":
           '''使用代理ip，随机选用'''
           proxy = self.get_random_proxy()  # 随机选择一个ip

           print("this is request ip:" + proxy)
           try:
               request.meta["proxy"] = proxy
           except Exception:

               pass

           return None







   def get_random_proxy(self):
       '''随机从文件中读取proxy'''
       while 1:
           with open('proxies.txt', 'r') as f:
               proxies = f.readlines()
           if proxies:
               break
           else:
               time.sleep(1)
       proxy = random.choice(proxies).strip()
       return proxy



class UAPOOLS(UserAgentMiddleware):
     def __init__(self,user_agent=''):
         self.user_agent=user_agent
     def process_request(self, request, spider):
         '''使用代理UA，随机选用'''
         ua=random.choice(self.user_agent_pools)
         print ('当前使用的user-agent是'+ua)
         try:
             request.headers.setdefault('User-Agent',ua)
         except Exception:

             pass
     user_agent_pools=[
         'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3',
         'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3',
         'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
     ]
