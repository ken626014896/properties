

import  scrapy
import urllib
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request
import  re


from selenium import webdriver


class Spider1Spider(scrapy.Spider):
    name="test2"
    start_urls={
        'https://mp.weixin.qq.com/s?timestamp=1540781615&src=3&ver=1&signature=JZLnGaok3l0FikahmrOFG99EdVpvS1B6b0VtlBDM1z5zPWwZ7a90fQQU6RrEUP3pnAjeNBE5Kwm5819N4HypQZ*GH2GEd8-G8GvV0t0F7IF-elTjPu2JYun6J4AeLHUESRrBDBTFHs*EOe9XRgSmOe-0d8sIn3iPnTI09zz6Jjc=',
    }
    custom_settings = {

        "COOKIES_ENABLED": True
    }
    #driver创建
    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\chromedriver.exe'

        chrome_options = webdriver.ChromeOptions()
        PROXY = "https://113.91.64.29:9797/"
        chrome_options.add_argument('--proxy-server=https://113.91.64.29:9797')
        self.browser = webdriver.Chrome(
            executable_path=PHANTOMJS_PATH,
            chrome_options=chrome_options)

        # self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,
        #                                    # service_args=["--load-images=false", "--disk-cache=true"],
        #                                   )

        self.browser.set_page_load_timeout(30)

    # 结束时关闭浏览器
    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def parse(self,response):
        print ("666666666666666")

        l=ItemLoader(item=PropertiesItem(),response=response)
        l.add_xpath("title",'//*[@class="title"]/text()')
        l.add_xpath("price", '//*[@class="trl-item sty1"]/i/text()',
                    MapCompose(float))

        return  l.load_item()






