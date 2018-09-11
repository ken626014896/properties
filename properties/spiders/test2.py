

import  scrapy
import urllib
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request


from selenium import webdriver


class Spider1Spider(scrapy.Spider):
    name="test2"
    start_urls={
        'http://mp.weixin.qq.com/profile?src=3&timestamp=1536301651&ver=1&signature=5OSEP63Mkz70iH4EQYvS*0vER3f8gcZizWxaWGxTU4-D-WwcnPjJwc-yX4Ow93cXUKY*r01TUSp56ddHCH*P8A==',

    }

    def parse(self,response):
        item_selector=response.xpath('//*[@class="weui_media_title"]/@hrefs')
        for url in item_selector.extract():
            # 使用request中的meta属性传递信息给parse_item

            item_url=urllib.parse.urljoin(response.url,url)
            print ("每个内容的url" + item_url)
            #抽取内容的简介
            describe=response.xpath('//*[@class="weui_media_desc"]/text()').extract()
            yield Request(item_url,meta={"dec":describe},callback=self.parse_item)

    def parse_item(self,response):
        l=ItemLoader(item=PropertiesItem(),response=response)
        l.add_xpath("title",'//*[@class="rich_media_title"]/text()',MapCompose(str.strip))
        l.add_xpath("time", '//*[@id="publish_time"]/text()')
        l.add_value("describe",response.meta["dec"])
        return  l.load_item()

