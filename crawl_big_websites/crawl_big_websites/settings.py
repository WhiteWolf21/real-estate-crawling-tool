# -*- coding: utf-8 -*-

# Scrapy settings for crawl_big_websites project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawl_big_websites'

SPIDER_MODULES = ['crawl_big_websites.spiders']
NEWSPIDER_MODULE = 'crawl_big_websites.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl_big_websites (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
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
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'crawl_big_websites.middlewares.CrawlBigWebsitesSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#     # 'crawl_big_websites.middlewares.CrawlBigWebsitesDownloaderMiddleware': 543,
#     'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'crawl_big_websites.pipelines.CrawlBigWebsitesPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# # Scrapy User Agents

# USER_AGENTS = [
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/57.0.2987.110 '
#      'Safari/537.36'),  # chrome
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/61.0.3163.79 '
#      'Safari/537.36'),  # chrome
#     ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
#      'Gecko/20100101 '
#      'Firefox/55.0'),  # firefox
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/61.0.3163.91 '
#      'Safari/537.36'),  # chrome
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/62.0.3202.89 '
#      'Safari/537.36'),  # chrome
#     ('Mozilla/5.0 (X11; Linux x86_64) '
#      'AppleWebKit/537.36 (KHTML, like Gecko) '
#      'Chrome/63.0.3239.108 '
#      'Safari/537.36'),  # chrome
# ]

# # Scrapy Rotating Proxies

# ROTATING_PROXY_LIST = [
#     '85.10.219.101:1080',
#     '203.189.143.201:65309',
#     '47.52.90.94:808',
#     '36.74.109.38:3128',
#     '178.128.63.7:44321',
#     '1.20.101.149:44778',
#     '85.10.219.99:1080',
#     '219.76.243.115:3128',
#     '118.99.100.49:8080',
#     '109.224.1.210:50617',
#     '159.65.11.59:44321',
#     '119.76.142.25:8080',
#     '138.68.8.149:8118',
#     '178.128.115.5:44321',
#     '178.128.118.47:44321',
#     '182.52.51.53:60441',
#     '159.224.44.19:37190',
#     '162.246.18.77:3128',
#     '79.143.179.56:3128',
#     '61.244.118.132:8118'
# ]