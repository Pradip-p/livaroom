# -*- coding: utf-8 -*-
import os
from lazy_crawler.lib.user_agent import get_user_agent

BOT_NAME = "lazy_py_crawler"

SPIDER_MODULES = ["lazy_crawler.crawler.spiders"]
NEWSPIDER_MODULE = "lazy_crawler.crawler.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
ROBOTSTXT_OBEY = False


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

ITEM_PIPELINES = {
    'lazy_crawler.crawler.pipelines.EnglishElmDBPipeline': 300,
    'lazy_crawler.crawler.pipelines.LivaroomDBPipeline': 400
    }

RETRY_TIMES = 3


# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs


FEED_EXPORT_ENCODING = 'utf-8'

DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 30

RANDOMIZE_DOWNLOAD_DELAY = True

REACTOR_THREADPOOL_MAXSIZE = 128

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 0.25
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 128
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True
RETRY_ENABLED = True

################################################################
# PROXY SETTINGS
################################################################
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 401, 403, 404, 405, 406, 407, 408, 409, 410, 429]
# 

DOWNLOADER_MIDDLEWARES = {
    'lazy_crawler.crawler.middlewares.CrawlerSpiderMiddleware': 400,
    # 'lazy_crawler.crawler.middlewares.RandomUserAgentMiddleware': 120,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Disable the default user agent middleware
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
    'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,


    'scrapy.spidermiddlewares.referer.RefererMiddleware': 80,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,  # Disable the default retry middleware

    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 130,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': 900,

}


FAKEUSERAGENT_PROVIDERS = [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # This is the first provider we'll try
    'scrapy_fake_useragent.providers.FakerProvider',  # If FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # Fall back to USER_AGENT value
]

USER_AGENT = get_user_agent('random')
