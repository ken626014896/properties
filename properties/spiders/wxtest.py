import  scrapy
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join
from selenium import webdriver
from scrapy.http import Request

class Spider1Spider(scrapy.Spider):
    name = 'wx'

    start_urls = ['https://mp.weixin.qq.com']

    custom_settings = {

    "COOKIES_ENABLED": True,
    # "AUTOTHROTTLE_ENABLED": True,
    # "DOWNLOAD_DELAY": True
    }

    # driver创建
    def __init__(self):
        PHANTOMJS_PATH = 'E:\python\phantomjs.exe'
        self.browser = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH,
                                           service_args=["--load-images=false", "--disk-cache=true"])

        self.browser.set_page_load_timeout(30)

    # 结束时关闭浏览器
    def closed(self, spider):
        print("spider closed")
        self.browser.close()


    def start_requests(self):  # 重构start_requests方法
        # 这个cookies_str是抓包获取的
        # 将cookies_str转换为cookies_dict
        cookies_str='noticeLoginFlag=1; remember_acct=ken626014896%40163.com; pgv_pvid=7807481550; eas_sid=r1y5p354T97535b5x0E6S4R4c2; RK=7IR16PCBaL; ptcz=a4e408f89f5ecf4f5e48ab40078d9ee0ae324f81cbb2ac3215ef835edd4566ce; LW_uid=R1m513s5c565H781Y0O0A0y3O5; pgv_pvi=2265807872; ptui_loginuin=626014896; pt2gguin=o0626014896; luin=o0626014896; lskey=00010000fd7285492c5a555ffb2d8f4605de7a678bfa4d927358cbe4b63e4393af7a1d69b5dfaa58d0b1e782; o_cookie=626014896; pac_uid=1_626014896; ua_id=IF66kY8xWClEKOMMAAAAAIsyx7uaep47Qh9HZyeRxPQ=; mm_lang=zh_CN; noticeLoginFlag=1; LW_sid=V1P5M3k6q7u462b6t8Y9m6S2J3; rewardsn=; wxtokenkey=777; sig=h01ea3680e19f46eb9a51b376a694fd074baf5ab107fe1d51d9dcee053ce995692151d75a05f2eba4f3; pgv_si=s8438865920; ticket=f423c4112751f0528d8b4733fe281a9d026ec770; ticket_id=gh_33c3009fc80b; uuid=128de0b2827658e631e120aeded58a8f; cert=2aLS_dVJLH6KaYvRdC3uf9YiZpmh_Zwb; data_bizuin=3580562212; bizuin=3513805982; data_ticket=vwdomKp927McRIAtNFBUcb28KIHbeI2kUSSn6g6UMJxMqBNN3NUlttgsIgRWNuOC; slave_sid=cjZKNVd3eHBtWF9EUEZtdG1pYllfMEhoNXYwOGFrOW1kUVluOHpOZnZZMUFSRW9ReEQ3UXVsUnp0ZkRDVUdVS1RkOHBUZjU5VkU3dGVIS05KSFRTeDNRMmE2VDQ0V2hsWWtHTjZJTk9fS3g5eUI0dUJaalkzVFFJYnpxR1RiV1FweG9FSTV4TkwxRUduMUlG; slave_user=gh_33c3009fc80b; xid=659dcca0712c06ca960c9a3073eb9c04; openid2ticket_oJAtr1RKRVT1Zp7a7tkJ6osHQi6U=3ix65NjQ4IknT+uFCgaxkRUoLs0PnmzAFsfAxMXmO4s='
        cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split('; ')}
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse_page,
            cookies=cookies_dict
        )

    # 处理响应内容
    def parse_page(self, response):
        print (response.url)
        page_url_0 = response.xpath('//*[@class="weui-desktop-home-notice__title"]/text()').extract()
        if len(page_url_0)==0:
            print ("0000000000000000")
        else:
         print (page_url_0)

         menu__name = response.xpath('//*[@class="weui-desktop-menu__name"]/text()').extract()
         if len(page_url_0) == 0:
             print ("0000000000000000")
         else:
             print (menu__name)
        return Request('https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=814293006&lang=zh_CN', callback=self.parse_next)

    def parse_next(self, response):
        item__name = response.xpath('//*[@class="tpl_item img"]/text()').extract()
        if len(item__name) == 0:
            print ("0000000000000000")
        else:
            print (item__name)

