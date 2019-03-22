import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join

import django

django.setup()


from adminpage.models import Official
from homepage.models import Category


#测试连接django  数据库
class ToMobileSpider(CrawlSpider):
    name = 'testdj'

    start_urls = ['http://dg.zu.fang.com']


    def parse(self, response):
        sort_list = [x.sort for x in Category.objects.all()]
        official_list = [{'name':x.name,'sort':x.sort} for x in Official.objects.all()]
        print(sort_list)
        print(official_list)



