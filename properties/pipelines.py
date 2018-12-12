# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import asyncio
from  properties import  settings
import os
from  urllib  import  request
from properties.items import PropertiesItem

#导入django数据库
import django

django.setup()

from homepage.models import Post

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

#下载图片的中间件
class imgpipelines(ImagesPipeline):


    def get_media_requests(self,item,info):
        return Request(item["image_url"][0])

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item
#新的下载图片中间件
class JiandanPipeline(object):

    def process_item(self, item, spider):
        if spider.name=="test1":
            print("进入图片中间件")
            dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)  # 存储路径
            #http://img01.store.sogou.com/net/a/04/link?appid=100520029&url=
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            img_name_list=[]
            #下载正文图片
            for image_url in item['img_url_list']:
                print('图片地址',image_url)
                # list_name = image_url.split('/')
                # file_name = list_name[len(list_name) - 2]  # 图片名称
                #
                # #获取数据格式，判断是是jpg还是gif
                # whichformat=list_name[len(list_name) - 3]
                # img_format=whichformat.split('_')[1]
                # print('图片格式是', img_format)
                file_name,img_format=self.getNameAndFormat(image_url)

                img_name=file_name+'.'+img_format
                img_name_list.append(img_name)

                file_path = '%s/%s' % (dir_path, file_name)
                # print 'file_path',file_path
                if os.path.exists(file_name):
                    continue
                with open(file_path+'.'+img_format, 'wb') as file_writer:
                    conn = request.urlopen(image_url)  # 下载图片
                    file_writer.write(conn.read())
                file_writer.close()
            #将图片的名字存储，方便后续处理
            item['temp2']=img_name_list


            #下载标题处的图片
            new_img_url=self.download_img(item,dir_path)
            #把item['img_url']中url替换成图片名字

            item['img_url'][0]=new_img_url

            return item
        else:
            return  item



    def download_img(self,item,dir_path):
            image_url =item['img_url'][0]

            # list_name = image_url.split('/')
            # file_name = list_name[len(list_name) - 2]  # 图片名称
            #
            # # 获取数据格式，判断是是jpg还是png
            # whichformat = list_name[len(list_name) - 3]
            # #得到图片格式
            # img_format = whichformat.split('_')[1]
            file_name, img_format = self.getNameAndFormat(image_url)

            img_name = file_name + '.' + img_format


            file_path = '%s/%s' % (dir_path, file_name)
            # print 'file_path',file_path

            with open(file_path + '.' + img_format, 'wb') as file_writer:
                conn = request.urlopen(image_url)  # 下载图片
                file_writer.write(conn.read())
            file_writer.close()

            return  img_name

    def getNameAndFormat(self, img_url):
        list_name = img_url.split('/')
        file_name = list_name[len(list_name) - 2]  # 图片名称

        # 获取数据格式，判断是是jpg还是png
        whichformat = list_name[len(list_name) - 3]
        # 得到图片格式
        img_format = whichformat.split('_')[1]

        return file_name, img_format
    # async midtemp
    #
    # def dowPicture(self,file_path,img_format,image_url):
    #             with open(file_path + '.' + img_format, 'wb') as file_writer:
    #                 conn = request.urlopen(image_url)  # 下载图片
    #                 file_writer.write(conn.read())
    #             file_writer.close()

#导出到django数据库的中间件
class jsonpelines(object):


    def __init__(self):
        pass
    # 使用codecs模块的打开方式，可以指定编码打开，避免很多编码问题
    #        self.file=codecs.open("dataio.json","w",encoding="utf-8")

    def process_item(self,item,spider):

        if(spider.name== 'test1'):
            print('写入数据库')
            Post.objects.get_or_create(title=item['title'][0],
                                       come_from=item['come_from'][0],
                                       publish_time=item['publish_time'][0],
                                       describe=item['describe'][0],
                                       img_url=item['img_url'][0],
                                       author=item['author'][0],
                                       sort=item['sort'][0],
                                       temp1=item['temp1'],
                                       temp2=item['temp2']
                                       )



            # lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            # self.file.write(lines)
            return item
        else:
            return item


    def spider_closed(self, spider):
        pass



class testpelines(object):


    def __init__(self):
    # 使用codecs模块的打开方式，可以指定编码打开，避免很多编码问题
           self.file=codecs.open("dataio.json","w",encoding="utf-8")

    def process_item(self,item,spider):

        if(spider.name== 'test3'):

            return item
        else:
            return item


    def spider_closed(self, spider):
        self.file.close()
