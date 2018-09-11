

import  scrapy
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join



class Spider1Spider(scrapy.Spider):
    name="basic1"
    start_urls={
        'http://dg.zu.fang.com/chuzu/3_161939485_1.htm?channel=1,2',

    }

    def parse(self,response):
        l=ItemLoader(item=PropertiesItem(),response=response)
        l.add_xpath("title",'//*[@class="title"]/text()')
        l.add_xpath("price", '//*[@class="trl-item sty1"]/i/text()',
                    MapCompose(float))

        return  l.load_item()
