

import  scrapy
from properties.items import PropertiesItem

from scrapy.loader import ItemLoader
from scrapy.loader.processors import  MapCompose,Join

from scrapy.http import FormRequest,Request
from selenium import webdriver


import urllib
import json

class Spider1Spider(scrapy.Spider):
    name="pixiv"
    start_urls = {"https://www.pixiv.net/"}

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
        cookies_str = 'first_visit_datetime_pc=2018-08-22+23%3A35%3A10; p_ab_id=0; p_ab_id_2=4; device_token=32801ffa8ffdfd351012e2b35d6a70d7; privacy_policy_agreement=1; c_type=23; a_type=0; b_type=1; module_orders_mypage=%5B%7B%22name%22%3A%22sketch_live%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22tag_follow%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22recommended_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22showcase%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22fanbox%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22user_events%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; yuid=IykoV0A39; login_ever=yes; ki_r=; __utmz=235335808.1535095298.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=4841777=1^9=p_ab_id=0=1^10=p_ab_id_2=4=1^11=lang=zh=1; _td=3824bf8a-3fc4-4237-9d0c-e62f87291c54; _ga=GA1.2.559416141.1535095298; login_bc=1; _gid=GA1.2.1414543717.1536335197; howto_recent_view_history=63181921; limited_ads=%7B%22header%22%3A%22%22%2C%22responsive%22%3A%22%22%2C%22illust_responsive%22%3A%22%22%7D; tag_view_ranking=RTJMXD26Ak~BU9SQkS-zU~y8GNntYHsi~Lt-oEicbBr~jH0uD88V6F~uusOs0ipBx~xZ6jtQjaj9~NpsIVvS-GF~qtVr8SCFs5~qiO14cZMBI~tgP8r-gOe_~gooMLQqB9a~jhuUT0OJva~65aiw_5Y72~Is0SiXyaWb~zyKU3Q5L4C~kGYw4gQ11Z~MSNRmMUDgC~oCR2Pbz1ly~sZ1KTSypMM~4ZEPYJhfGu~NXxDJr1D_u~fg8EOt4owo~nQRrj5c6w_~wU5dbYkh4O~2pZ4K1syEF~R3lr4__Kr8~AdHuyJ9D0T~K8esoIs2eW~kwQ7-a01CG~wdNuwZX6JD~mf6rICH32i~1DreUdF52S~t6fkfIQnjP~WgYXPwwlZn~P-jVO8CNUe~NlYn1jwtuG~plqXT5B4--~IiPOQFKWOO~YRDwjaiLZn~KHhKRc2P1_~JHsz5uV6h2~xfYGFeocXg~pzzjRSV6ZO~_RfiUqtsxe~WcTW9TCOx9~UX647z2Emo~_pwIgrV8TB~OUkihvwBMZ~isFf_CMYqz~QLvl6kE4lC~pUiZrwGSn4~9LhLC1Kxwa~h9fEA3tOFb~Ms9Iyj7TRt~NE-E8kJhx6~50ydG8OUmH~fn5nUXtjWI~qpeZSmEVVP~7eyUzBENF5~bXMh6mBhl8~Cj5DZjEKpk~-qP3pM5H97~MHugbgF9Xo~-sp-9oh8uv~DNf_U6TMoC~zcefxGBLt4~t2ErccCFR9~f-c_0dUV8c~28gdfFXlY7~gnTtYdDB_b~azESOjmQSV~uKsA-LcJvn~QjJSYNhDSl~DhsFaGyxgs~cpt_Nk5mjc~BQv9ZOKrJ7~Ie2c51_4Sp~LgUnHb4aPq~flb2ZnuOIx~_iaP-J1xu4~3W4zqr4Xlx~R_O4FX9MRI~_qEgMLCvnG~zxRuGIr7SD~MOq5w-NBVz~G2Ul3C-Rl0~uVYW_mXFnG~w_fCM-S2TE~E8plmQ7kUK~dQZopxFsxX~AlDva0XKC6~WxVAdUQMC-~bX7kls1wXg~1HuE7w0nKg~mFuvKdN_Mu~V6GgaEP-Fi~Hxq8PxNg7w~wWMD6tyDBD~C1vT0qTTDK; __utma=235335808.559416141.1535095298.1536397076.1536470874.8; __utmc=235335808; is_sensei_service_user=1; OX_plg=pm; __utmt=1; ki_t=1534948598858%3B1536471156524%3B1536477548875%3B6%3B26; __utmb=235335808.26.10.1536470874; _gat=1; PHPSESSID=4841777_178f17cb20a4b2ffb98fde44db5f5558'  # 抓包获取
        # 将cookies_str转换为cookies_dict
        cookies_dict = {i.split('=')[0]: i.split('=')[1] for i in cookies_str.split('; ')}
        yield scrapy.Request(
            'https://www.pixiv.net/',
            callback=self.parse_page,
            cookies=cookies_dict
        )

    # 处理响应内容
    def parse_page(self, response):
        #print (response.text)
        next_url=response.xpath('//*[@id="column-misc"]/section[2]/ul/li[2]/a/@href').extract()


        much_img_url = urllib.parse.urljoin(response.url, next_url[0])
        return Request(much_img_url, callback=self.get_img_url)

    def get_img_url(self,response):
        item_url_list=response.xpath('//*[@class="ranking-image-item"]/a/@href').extract()
        # for  item_url in item_url_list:
        #     yield Request(urllib.parse.urljoin(response.url, item_url), callback=self.download_img)

        return Request(urllib.parse.urljoin(response.url, item_url_list[0]), callback=self.download_img)

    def download_img(self,response):
        l = ItemLoader(item=PropertiesItem(), response=response)
        url=response.xpath('//*[@class="_2r_DywD"]/@src').extract()
        print ('11111111')
        print (url)








