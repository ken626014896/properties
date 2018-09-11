

import  scrapy
import urllib
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request

#进入房源页面爬取
class Spider1Spider(scrapy.Spider):
    name="manual"
    start_urls={
        'http://dg.zu.fang.com',

    }

    def parse(self,response):


        next_selector=response.xpath('//*[@id="rentid_D10_01"]/a[7]//@href')
        for url in next_selector.extract():
            print("1房源所在索引页面" + response.url)
            yield Request(urllib.parse.urljoin(response.url,url))

        item_selector=response.xpath('//*[@class="title"]/a//@href')
        for url in item_selector.extract():
            # 使用request中的meta属性传递信息给parse_item

            url3=urllib.parse.urljoin(response.url,url)
            print ("每个房源的url" + url3)
            print("2房源所在索引页面"+response.url)
            yield Request(urllib.parse.urljoin(response.url,url),meta={"urlll":url3},callback=self.parse_item)

    def parse_item(self,response):
        l=ItemLoader(item=PropertiesItem(),response=response)
        l.add_xpath("title",'//*[@class="tab-cont clearfix"]/h1/text()')
        l.add_xpath("price", '//*[@class="trl-item sty1"]/i/text()',
                    MapCompose(float))
        l.add_value("nextpage_url2",response.meta["urlll"])
        return  l.load_item()

