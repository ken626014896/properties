

import  scrapy
import urllib
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request

#30倍速的爬取,不用进入房源页面，直接在索引页爬取
class Spider1Spider(scrapy.Spider):
    name="fast"
    start_urls={
        'http://dg.zu.fang.com',

    }

    def parse(self,response):


        next_selector=response.xpath('//*[@id="rentid_D10_01"]/a[7]//@href')

        for url in next_selector.extract():

            yield Request(urllib.parse.urljoin(response.url,url))

        selectors=response.xpath('//*[@class="list hiddenMap rel"]')
        for selector in selectors:
            print (selector)
            yield self.parse_item(selector,response)

    def parse_item(self,selector,response):
        l=ItemLoader(item=PropertiesItem(),selector=selector)
        l.add_xpath("title",'.//*[@class="title"]/a/text()')
        l.add_xpath("price", './/*[@class="price"]/text()',
                    MapCompose(float))
        make_url=lambda i :urllib.parse.urljoin(response.url,i)
        l.add_xpath("item_url", './/*[@class="title"]/a/@href',
                    MapCompose(make_url))
        l.add_value("nextpage_url",response.url)
        return  l.load_item()


