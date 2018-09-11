# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join


#使用CrawlSpider实现双向爬取
#LinkExtractor专门查找url地址
class ToMobileSpider(CrawlSpider):
    name = 'tomobile'

    start_urls = ['http://dg.zu.fang.com']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="rentid_D10_01"]')),
        Rule(LinkExtractor(restrict_xpaths='//*[@class="title"]'), callback='parse_item')
             )

    def parse_item(self, response):
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath("title", '//*[@class="tab-cont clearfix"]/h1/text()')
        l.add_xpath("price", '//*[@class="trl-item sty1"]/i/text()',
                    MapCompose(float))
        l.add_xpath("image_url", '//*[@class="bigImg"]/img[1]/@src')
        return l.load_item()

