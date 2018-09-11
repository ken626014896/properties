# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline

class PropertiesPipeline(object):
    def __init__(self):
        pass

    #可选实现，做参数初始化等
    # doing something
    def process_item(self, item, spider):
        # item (Item 对象) – 被爬取的item
        # spider (Spider 对象) – 爬取该item的spider
        # 这个方法必须实现，每个item pipeline组件都需要调用该方法，
        # 这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理。
        print (len(item["title"]))
        return item

    def open_spider(self, spider):
        pass
    # spider (Spider 对象) – 被开启的spider
    # 可选实现，当spider被开启时，这个方法被调用。

    def close_spider(self, spider):
        pass
# spider (Spider 对象) – 被关闭的spider
# 可选实现，当spider被关闭时，这个方法被调用

class imgpipelines(ImagesPipeline):


    def get_media_requests(self,item,info):
        return Request(item["image_url"][0])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item