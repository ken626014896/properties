

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

class Spider1Spider(scrapy.Spider):
    name="test1"
    start_urls={
        #养老
        'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%85%BB%E8%80%81&ie=utf8&_sug_=n&_sug_type_=',
        #军事
        'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%86%9B%E4%BA%8B&ie=utf8&_sug_=n&_sug_type_=',
        #科技
        'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%A7%91%E6%8A%80&ie=utf8&_sug_=y&_sug_type_=',
        #娱乐
        'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%A8%B1%E4%B9%90&ie=utf8&_sug_=n&_sug_type_=',
        #学习
        'https://weixin.sogou.com/weixin?type=1&s_from=input&query=%E5%AD%A6%E4%B9%A0&ie=utf8&_sug_=n&_sug_type_='

        # "http://weixin.sogou.com/weixin?type=1&s_from=input&query=%E7%AC%94%E5%90%A7%E8%AF%84%E6%B5%8B%E5%AE%A4&ie=utf8&_sug_=n&_sug_type_=",
        # 'http://weixin.sogou.com/weixin?type=1&s_from=input&query=it%E4%B9%8B%E5%AE%B6&ie=utf8&_sug_=n&_sug_type_='

        # 'http://weixin.sogou.com/weixin?query=%E7%A7%91%E6%8A%80&_sug_type_=&sut=960&lkt=0%2C0%2C0&s_from=input&_sug_=y&type=1&sst0=1537598169226&page=1&ie=utf8&w=01019900&dr=1',
        # 'http://weixin.sogou.com/weixin?query=%E7%A7%91%E6%8A%80&_sug_type_=&sut=960&lkt=0%2C0%2C0&s_from=input&_sug_=y&type=1&sst0=1537598169226&page=2&ie=utf8&w=01019900&dr=1',

    }
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

    def parse(self,response):
        #因为公众号主页不断变化，所以要先查询再进去
        # msg = response.xpath('//*[@class="p2"]/text()').extract()
        # if (len(msg) != 0):
        #     print (msg[0])
        # page_url=response.xpath('//*[@class="tit"]/a/@href').extract()[0]
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
                continue


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
        #修改每张图片的地址
        # i = 0
        # for img in img_url_list:
        #     img_url_list[i] = img + "&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1&retryload=1"
        #     i = i + 1

        #判断出现空集时的操作
        if len(img_url_list) == 0 :
            l.add_value("img_url_list", "无")
        else:
            l.add_value("img_url_list",img_url_list)


        # if len(context_list) == 0:
        #     l.add_value("context_list", "无")
        # else:
        #     l.add_value("context_list", context_list)



        # l.add_xpath("context_list", '//*[@class="rich_media_content "]/p/text()')

        return l.load_item()

