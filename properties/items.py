# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import codecs


class PropertiesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #推送的类别
    sort=scrapy.Field()


    title=scrapy.Field()

    #公众号url
    page_url=scrapy.Field()
    describe=scrapy.Field()


    img_url=scrapy.Field()

    item_url=scrapy.Field()


    come_from=scrapy.Field()
    publish_time=scrapy.Field()

    # 作者 可有可无
    author = scrapy.Field()

    img_url_list = scrapy.Field()
    context_list =scrapy.Field()
    # 待定数据
    temp1 =scrapy.Field()  #已用于存储全文样式
    temp2 =scrapy.Field()  #已用于存储图片名字
    temp3 =scrapy.Field()


