

import  scrapy
from properties.items import PropertiesItem
import urllib
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request



from selenium import webdriver

class Spider1Spider(scrapy.Spider):
    name="test1"
    start_urls={
        "http://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%AC%94%E5%90%A7%E8%AF%84%E6%B5%8B%E5%AE%A4&ie=utf8&_sug_=n&_sug_type_=",
        'http://weixin.sogou.com/weixin?type=1&s_from=input&query=it%E4%B9%8B%E5%AE%B6&ie=utf8&_sug_=n&_sug_type_='
    }

    # driver创建
    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,service_args=["--load-images=false", "--disk-cache=true"])

        self.browser.set_page_load_timeout(30)
    #结束时关闭浏览器
    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def parse(self,response):
        #因为公众号主页不断变化，所以要先查询再进去
        page_url_0=response.xpath('//*[@class="tit"]/a/@href').extract()[0]
        page_url=urllib.parse.urljoin(response.url,page_url_0)

        return Request(page_url,callback=self.parse_next)
    def parse_next(self,response):
        #现在在公众号主页 现在准备跳转的各个推送网页,
        #这里推送的新闻列表使用js加载的，不可以用传统的方法

        #检测网页是否访问过快导致要输入验证码
        msg=response.xpath('//*[@class="weui_cells_tips"]/text()').extract()
        if(len(msg)!=0  and msg=="为了保护你的网络安全，请输入验证码"):
             print ("访问过于频繁,要输入验证码了0.0")

        print ('公众号地址为：' + response.url)

        item_selector = response.xpath('//*[@class="weui_media_bd"]')

        for item in item_selector:

            # 抽取内容的url
            item_url_0 = item.xpath('.//*[@class="weui_media_title"]/@hrefs').extract()

            item_url = urllib.parse.urljoin(response.url, item_url_0[0])

            # 抽取内容的简介列表
            describe = item.xpath('.//*[@class="weui_media_desc"]/text()').extract()

            if(len(describe)==0):
                 describe.append('无')

            # 抽取内容的发表时间
            publish_time=item.xpath('.//*[@class="weui_media_extra_info"]/text()').extract()
            print ("每个推送的url" + item_url)

            # 使用request中的meta属性传递信息给parse_item
            yield Request(item_url, meta={"dec": describe[0],"publish_time":publish_time[0]}, callback=self.parse_item)



    def parse_item(self,response):

        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath("title", '//*[@class="rich_media_title"]/text()',MapCompose(str.strip))
       # l.add_xpath("time", '//*[@id="publish_time"]/text()',MapCompose(str.strip))
        l.add_xpath("come_from", '//*[@id="js_name"]/text()', MapCompose(str.strip))
        l.add_value("describe", response.meta["dec"])
        l.add_value("publish_time", response.meta["publish_time"])

        return l.load_item()