

import  scrapy
from properties.items import PropertiesItem
import urllib
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request


from selenium import webdriver
import codecs
class Spider1Spider(scrapy.Spider):
    name="test3"
    start_urls={
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1540911542&ver=1&signature=of8ixxll0a*OBLKudf8xvUesiws3Vxkrs6RjfwIo2in*x9*LNCKxMiDLHRM4LEshPF8nuQBEzJLItYx5wzkOYw==',
    }

    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,service_args=["--load-images=false", "--disk-cache=true"])

        self.browser.set_page_load_timeout(30)

    def closed(self, spider):
      print("spider closed")
      self.browser.close()

    def parse(self,response):
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_value("title", '题目')
        l.add_value("describe", '介绍')

        return l.load_item()








        





