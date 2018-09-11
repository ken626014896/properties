# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy




class PropertiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    time=scrapy.Field()

    price=scrapy.Field()

    image_url=scrapy.Field()
    image_paths=scrapy.Field()
    images =scrapy.Field()


    item_url=scrapy.Field()
    nextpage_url=scrapy.Field()
    nextpage_url2 = scrapy.Field()

    PixivImgUrl=scrapy.Field()
    describe=scrapy.Field()

    come_from=scrapy.Field()
    publish_time=scrapy.Field()
    pass
