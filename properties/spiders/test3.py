

import  scrapy
from properties.items import PropertiesItem
import urllib
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request


from selenium import webdriver
import codecs
from selenium.webdriver.chrome.options import Options
class Spider1Spider(scrapy.Spider):
    name="test3"
    start_urls=['https://www.baidu.com/']

    def __init__(self):
        # PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        # self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,service_args=["--load-images=false", "--disk-cache=true"])
        #
        # self.browser.set_page_load_timeout(30)
        PHANTOMJS_PATH = 'E:\python\chromedriver.exe'
        chrome_options = Options()
        chrome_options.add_argument("no-sandbox")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
        chrome_options.add_argument('lang=zh_CN.UTF-8')
        # 更换头部
        chrome_options.add_argument( 'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
        self.browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=PHANTOMJS_PATH)

    def closed(self, spider):
      print("spider closed")
      self.browser.close()

    def parse(self, response):
        sort_url_name = urllib.parse.quote('科技')
        home_url= 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_='% sort_url_name

        yield Request(home_url, callback=self.parse2)
    def parse2(self,response):
        msg = response.xpath('//*[@class="txt-box"]').extract()
        for i in msg:
            print('hi',i)

        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_value("title", '题目')
        l.add_value("describe", '介绍')

        return l.load_item()








        





