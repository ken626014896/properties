import  scrapy
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from selenium import webdriver


class Spider1Spider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    custom_settings = {

    "COOKIES_ENABLED": True,
    # "AUTOTHROTTLE_ENABLED": True,
    # "DOWNLOAD_DELAY": True
    }

    # driver创建
    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,
                                           service_args=["--load-images=false", "--disk-cache=true"])

        self.browser.set_page_load_timeout(30)

    # 结束时关闭浏览器
    def closed(self, spider):
        print("spider closed")
        self.browser.close()
    def start_requests(self):
        burl = "http://www.xicidaili.com/nn/"
        for i in range(1, 5):
            yield scrapy.Request(url=burl + str(i), callback=self.parse)

    def parse(self, response):

        item_selector = response.xpath('//*[@class="odd"]')


        for s in item_selector:
            content = s.xpath('.//td/text()').extract()

            scheme = content[5]
            if scheme == 'HTTP' or scheme == 'HTTPS':
                print ('%s://%s:%s' % (scheme.lower(), content[0], content[1]))
