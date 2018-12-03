# -*- coding: utf-8 -*-

# Scrapy settings for properties project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'properties'

SPIDER_MODULES = ['properties.spiders']
NEWSPIDER_MODULE = 'properties.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'properties (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

#连接到apperyio的设置
ITEM_PIPELINES={#'scrapyapperyio.ApperyIoPipeline':300,
                   #"properties.pipelines.imgpipelines":300,


                }
APPERYIO_DB_ID='5b9609522e22d76250529a58'
APPERYIO_USERNAME="root"
APPERYIO_PASSWORD="pass"
APPERYIO_COLLECTION_NAME="Publish"

#配置下载图像功能
IMAGES_STORE="data/imgs"
ROBOTSTXT_OBEY = False
MAGES_URLS_FIELD='image_url'  # 该字段的值为XxxItem中定义的存储图片链接的image_urls字段
#IMAGES_RESULT_FIELD='title'   # 该字段的值为XxxItem中定义的存储图片信息的images字段
IMAGES_THUMBS={'small':(30,30)}

# import sys
# sys.path.append('../../wxproject')
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'wxproject.settings'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'properties.middlewares.PropertiesSpiderMiddleware': 543,

# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'properties.middlewares.PropertiesDownloaderMiddleware': 543,
#
# 'properties.middlewares.MyproxiesSpiderMiddleware':541,
# 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,
#
# 'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None,


# 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':540,
# 'properties.middlewares.IPPOOLS':541,
# # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : 542,
# # 'properties.middlewares.UAPOOLS':543,



'properties.middlewares.JavaScriptMiddleware': 543,
'properties.middlewares.JavaScriptMiddlewareOfPixiv': 543,
'properties.middlewares.TestMiddleware': 543,


# 'properties.middlewares.RandomUserAgentMiddleware': 543,
#  'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None, #这里要设置原来的scrapy的useragent为None，否者会被覆盖掉

}
RANDOM_UA_TYPE='random'

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
#数值越低，组件的优先级越高
#    'properties.pipelines.PropertiesPipeline': 300,
'properties.pipelines.jsonpelines': 310,  #把数据写入文件管道
'properties.pipelines.JiandanPipeline': 300,#下载图片管道
'properties.pipelines.testpelines': 320,


}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

FEED_EXPORT_ENCODING = 'utf-8'

