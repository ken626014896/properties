

import  scrapy
from properties.items import PropertiesItem
import urllib
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request


from selenium import webdriver

class Spider1Spider(scrapy.Spider):
    name="test3"
    start_urls={
        "http://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%AC%94%E5%90%A7%E8%AF%84%E6%B5%8B%E5%AE%A4&ie=utf8&_sug_=n&_sug_type_="
    }

    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,service_args=["--load-images=false", "--disk-cache=true"])

        self.browser.set_page_load_timeout(30)

    def closed(self, spider):
      print("spider closed")
      self.browser.close()

    def parse(self,response):
        #因为公众号主页不断变化，  所以要先查询再进去
        page_url_0=response.xpath('//*[@class="tit"]/a/@href').extract()[0]
        page_url=urllib.parse.urljoin(response.url,page_url_0)

        return Request(page_url,callback=self.parse_next)
    def parse_next(self,response):
        #现在在公众号主页 现在准备跳转的新闻网页,
        #这里推送的新闻列表使用js加载的，不可以用传统的方法
        print ('公众号地址为：' + response.url)
        bodyy = response.xpath('//*[@class="weui_media_title"]/@hrefs').extract()
        #这里的是一个已经通过加载了的显式的url列表 不再是js加载的
        print (bodyy)


        





