# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


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

                # # 这个cookies_str是抓包获取的
                # cookies_str = 'first_visit_datetime_pc=2018-08-22+23%3A35%3A10; p_ab_id=0; p_ab_id_2=4; device_token=32801ffa8ffdfd351012e2b35d6a70d7; privacy_policy_agreement=1; c_type=23; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22showcase%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; yuid=IykoV0A39; login_ever=yes; ki_r=; __utmz=235335808.1535095298.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=4841777=1^9=p_ab_id=0=1^10=p_ab_id_2=4=1^11=lang=zh=1; _td=3824bf8a-3fc4-4237-9d0c-e62f87291c54; _ga=GA1.2.559416141.1535095298; login_bc=1; _gid=GA1.2.1414543717.1536335197; howto_recent_view_history=63181921; limited_ads=%7B%22header%22%3A%22%22%2C%22responsive%22%3A%22%22%2C%22illust_responsive%22%3A%22%22%7D; tag_view_ranking=RTJMXD26Ak~BU9SQkS-zU~y8GNntYHsi~Lt-oEicbBr~jH0uD88V6F~uusOs0ipBx~xZ6jtQjaj9~NpsIVvS-GF~qtVr8SCFs5~qiO14cZMBI~tgP8r-gOe_~gooMLQqB9a~jhuUT0OJva~65aiw_5Y72~Is0SiXyaWb~zyKU3Q5L4C~kGYw4gQ11Z~MSNRmMUDgC~oCR2Pbz1ly~sZ1KTSypMM~4ZEPYJhfGu~NXxDJr1D_u~fg8EOt4owo~nQRrj5c6w_~wU5dbYkh4O~2pZ4K1syEF~R3lr4__Kr8~AdHuyJ9D0T~K8esoIs2eW~kwQ7-a01CG~wdNuwZX6JD~mf6rICH32i~1DreUdF52S~t6fkfIQnjP~WgYXPwwlZn~P-jVO8CNUe~NlYn1jwtuG~plqXT5B4--~IiPOQFKWOO~YRDwjaiLZn~KHhKRc2P1_~JHsz5uV6h2~xfYGFeocXg~pzzjRSV6ZO~_RfiUqtsxe~WcTW9TCOx9~UX647z2Emo~_pwIgrV8TB~OUkihvwBMZ~isFf_CMYqz~QLvl6kE4lC~pUiZrwGSn4~9LhLC1Kxwa~h9fEA3tOFb~Ms9Iyj7TRt~NE-E8kJhx6~50ydG8OUmH~fn5nUXtjWI~qpeZSmEVVP~7eyUzBENF5~bXMh6mBhl8~Cj5DZjEKpk~-qP3pM5H97~MHugbgF9Xo~-sp-9oh8uv~DNf_U6TMoC~zcefxGBLt4~t2ErccCFR9~f-c_0dUV8c~28gdfFXlY7~gnTtYdDB_b~azESOjmQSV~uKsA-LcJvn~QjJSYNhDSl~DhsFaGyxgs~cpt_Nk5mjc~BQv9ZOKrJ7~Ie2c51_4Sp~LgUnHb4aPq~flb2ZnuOIx~_iaP-J1xu4~3W4zqr4Xlx~R_O4FX9MRI~_qEgMLCvnG~zxRuGIr7SD~MOq5w-NBVz~G2Ul3C-Rl0~uVYW_mXFnG~w_fCM-S2TE~E8plmQ7kUK~dQZopxFsxX~AlDva0XKC6~WxVAdUQMC-~bX7kls1wXg~1HuE7w0nKg~mFuvKdN_Mu~V6GgaEP-Fi~Hxq8PxNg7w~wWMD6tyDBD~C1vT0qTTDK; __utma=235335808.559416141.1535095298.1536397076.1536470874.8; __utmc=235335808; is_sensei_service_user=1; OX_plg=pm; __utmt=1; ki_t=1534948598858%3B1536471156524%3B1536477548875%3B6%3B26; __utmb=235335808.26.10.1536470874; _gat=1; PHPSESSID=4841777_178f17cb20a4b2ffb98fde44db5f5558'  # 抓包获取
                # # 将cookies_str转换为cookies_dict
                # cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split('; ')}
                #
                # spider.browser.add_cookie(cookies_dict)
                # spider.browser.refresh()

               # spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
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
