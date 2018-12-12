

import  scrapy
from properties.items import PropertiesItem
import urllib
from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from scrapy.http import Request
import re
from  urllib.parse import urljoin
import time

from selenium import webdriver


#导入django数据库
import django

django.setup()
from adminpage.models import Official
from homepage.models import Category

class Spider1Spider(scrapy.Spider):
    name="test1"
    start_urls = ['https://www.baidu.com/']

    custom_settings = {

        "COOKIES_ENABLED":False,
        "DOWNLOAD_DELAY": 0.25,


    }


    # driver创建
    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,service_args=["--load-images=false", "--disk-cache=true"])

        self.browser.set_page_load_timeout(30)
    #结束时关闭浏览器
    def closed(self, spider):
        print("spider closed")
        self.browser.close()
    def parse(self, response):
        sort_list = [x.sort for x in Category.objects.all()]
        official_list = [{'name': x.name, 'sort': x.sort} for x in Official.objects.all()]
        for sort in sort_list:
            sort_url_name = urllib.parse.quote(sort)
            home_url= 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_='% sort_url_name
            sort=None

            yield Request(home_url, callback=self.getHomepage, meta={"sort": sort})
        for official in  official_list:
            official_url_name = urllib.parse.quote(official.get('name'))
            home_url = 'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_=' % official_url_name
            sort =official.get('sort')


            yield Request(home_url, callback=self.getHomepage, meta={"sort": sort})

    def getHomepage(self,response):
        #因为公众号主页不断变化，所以要先查询再进去


        #根据上层函数传来的sort是否有值，判断是默认爬虫的分类，还是管理员增加的公众号

        hint=response.meta['sort']
        if(hint==None):
            msg = response.xpath('//*[@class="p2"]/text()').extract()
            if (len(msg) != 0):
                print (msg[0])
            page_url_list=response.xpath('//*[@class="tit"]/a/@href').extract()

            #推送的类型
            sort=response.xpath('//*[@class="query"]/@value').extract()


            #只拿前三个公众号
            temp=0
            for  page_url in page_url_list:


                if temp<=2:
                   temp = temp + 1
                   yield Request(page_url, callback=self.parse_next,meta={"sort": sort[0]})
        else:
            msg = response.xpath('//*[@class="p2"]/text()').extract()
            if (len(msg) != 0):
                print(msg[0])
            page_url_list = response.xpath('//*[@class="tit"]/a/@href').extract()

            # 推送的类型
            sort = hint

            yield Request(page_url_list[0], callback=self.parse_next, meta={"sort": sort})


        #
        # return Request(page_url_list[0],callback=self.parse_next,meta={"sort": sort[0]})
    def parse_next(self,response):
        #现在在公众号主页 现在准备跳转的各个推送网页,
        #这里推送的新闻列表使用js加载的，不可以用传统的方法

        #获取类别
        sort=response.meta['sort']
        #检测网页是否访问过快导致要输入验证码
        msg=response.xpath('//*[@class="weui_cells_tips"]/text()').extract()
        if(len(msg)!=0 ) :
             print ("访问过于频繁,要输入验证码了0.0")


        comefrom=response.xpath('//*[@class="profile_nickname"]/text()').extract()[0]
        item_selector = response.xpath('//*[@class="weui_media_box appmsg"]')

        for item in item_selector:
            # 不要全部爬取
            #判断日期之后再爬取
            publish_time = item.xpath('.//*[@class="weui_media_extra_info"]/text()').extract()

            #获取当前
            strtime = time.strftime('%Y.%m.%d', time.localtime(time.time()))
            listtime = strtime.split(".")

            # item发表时间
            pt = publish_time[0]

            ptlist = re.split('[年月日]', pt)

            # 相差时间天数
            diff = int(listtime[2]) - int(ptlist[2])
            if int(listtime[1]) == int(ptlist[1]) and diff <= 1: #只拿今天的推送
                # 抽取内容的url
                item_url_0 = item.xpath('.//*[@class="weui_media_title"]/@hrefs').extract()

                item_url = urljoin(response.url, item_url_0[0])

                # 抽取内容的简介列表
                describe = item.xpath('.//*[@class="weui_media_desc"]/text()').extract()

                if (len(describe) == 0):
                    describe.append('无')

                # 抽取内容的发表时间
                publish_time = item.xpath('.//*[@class="weui_media_extra_info"]/text()').extract()
                # 抽取内容的图片
                image_url = item.xpath('.//*[@class="weui_media_hd"]/@style').extract()

                if (len(image_url) == 0):
                    image_url.append("www.baidu.com")

                else:
                    images = re.split('[()]', image_url[0])
                    print("每个推送的图片地址" + images[1])

                yield Request(item_url,
                              meta={"dec": describe[0], "publish_time": publish_time[0], "pageurl": response.url,
                                    "imgurl": images[1],'sort':sort}, callback=self.parse_item)

            else:
                continue



    def parse_item(self,response):

        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath("title", '//*[@class="rich_media_title"]/text()',MapCompose(str.strip))
       # l.add_xpath("time", '//*[@id="publish_time"]/text()',MapCompose(str.strip))
        l.add_xpath("come_from", '//*[@id="js_name"]/text()', MapCompose(str.strip))
        l.add_value("describe", response.meta["dec"])
        l.add_value("publish_time", response.meta["publish_time"])
        l.add_value("page_url", response.meta["pageurl"])
        l.add_value("item_url", response.url)
        l.add_value("img_url", response.meta["imgurl"])
        l.add_value("sort", response.meta["sort"])



        author=response.xpath('//*[@class="rich_media_meta rich_media_meta_text"]/text()').extract()
        if len(author)==0 or len(author)==1:
            l.add_value("author", "原创")
        else:
            l.add_value("author", author[0], MapCompose(str.strip))


        #爬取全部图片url
        temp_selector = response.xpath('//*[@class="rich_media_content "]')

        for temp in temp_selector:
            img_url_list = temp.xpath('.//img/@data-src').extract()
            # context_list = temp.xpath('.//span/text()').extract()

        # 爬取全部内容样式
        all_context=response.xpath('//*[@class="rich_media_content "]').extract()
        l.add_value("temp1", all_context[0])



        #判断出现空集时的操作
        if len(img_url_list) == 0 :
            l.add_value("img_url_list", "无")
        else:
            l.add_value("img_url_list",img_url_list)




        return l.load_item()

