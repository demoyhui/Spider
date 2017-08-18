# -*- coding: utf-8 -*-

# Scrapy settings for LagouProject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#控制并发
CONCURRENT_REQUESTS_PER_DOMAIN = 1  #使爬虫同时只能对每个域名发起一个请求
DOWNLOAD_DELAY =3   #每两次请求之间存在延迟时间为5秒
#Mysql数据库的配置信息
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'lagou'         #数据库名字，请修改
MYSQL_USER = 'root'             #数据库账号，请修改
MYSQL_PASSWD = '123456'         #数据库密码，请修改

MYSQL_PORT = 3306               #数据库端口，在dbhelper中使用
BOT_NAME = 'LagouProject'

SPIDER_MODULES = ['LagouProject.spiders']
NEWSPIDER_MODULE = 'LagouProject.spiders'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'LagouProject (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
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
DEFAULT_REQUEST_HEADERS = {
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
  'Accept-Language':'zh-CN,zh;q=0.8',
  'Host':'www.lagou.com',
  'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36',
  'Connection':'keep-alive'
}
# 使用transCookie.py翻译出的Cookie字典
COOKIE = {'showExpriedCompanyHome': '1', 'PRE_SITE': '', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1502949211', 'PRE_UTM': '', '_putrc': '898B7EED4E87F460', 'index_location_city': '%E6%9D%AD%E5%B7%9E', 'LGRID': '20170817135330-65b8f67c-8310-11e7-896d-5254005c3644', 'JSESSIONID': 'ABAAABAAAGFABEF26AEF8784B5B7A882A42E6052138C577', 'LGUID': '20170721092217-08f5f7cf-6db3-11e7-b96a-525400f775ce', 'unick': '%E5%BC%A0%E4%BA%9A%E8%BE%89', '_gid': 'GA1.2.286872729.1502773844', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F', 'showExpriedIndex': '1', '_ga': 'GA1.2.48583056.1500600144', 'showExpriedMyPublish': '1', 'TG-TRACK-CODE': 'index_navigation', 'hasDeliver': '19', 'PRE_HOST': '', '_gat': '1', 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1502512410,1502626911,1502628414,1502773844', 'LGSID': '20170817135330-65b8f3eb-8310-11e7-896d-5254005c3644', 'X_HTTP_TOKEN': '70f85cc2cdec3e249d99fbd5fdb73b0d', 'user_trace_token': '20170721092216-b224b3ce957742f3b97342fc87749e21', 'login': 'true', 'SEARCH_ID': '0b2f7926a1894aa29f572c8d52409b6b'}


# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'LagouProject.middlewares.LagouprojectSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'LagouProject.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'LagouProject.pipelines.LagouprojectPipeline': 300,#保存到MySql
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
