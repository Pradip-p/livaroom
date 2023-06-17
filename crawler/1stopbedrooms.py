#!/usr/bin/env python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.user_agent import get_user_agent
import gc
import time
from scrapy.spidermiddlewares.httperror import HttpError
import json

class LazyCrawler(LazyBaseCrawler):
    name = "1stopbedrooms"

    allowed_domains = ['1stopbedrooms.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 64,
        'CONCURRENT_REQUESTS_PER_IP': 64,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
        'RETRY_TIMES': 2,
        # "COOKIES_ENABLED": True,
        'DOWNLOAD_TIMEOUT': 10,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.ColemanDBPipeline': None
        }
    }

    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }
    
    
    def start_requests(self):  # Project starts from here.
        headers = {
            'User-Agent': get_user_agent('random'),
            **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
        }
        url = 'https://www.1stopbedrooms.com/all-furniture'
        
        yield scrapy.Request(
            url,
            self.parse_url,
            dont_filter=True,
            errback=self.errback_http_ignored,
            headers=headers
        )
    def parse_url(self, response):
        urls = response.xpath('//a[@class="subcategories-section almost-sb-button"]/@href').extract()
        
        headers = {
            'User-Agent': get_user_agent('random'),
            **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
        }
        for url in urls:
            yield scrapy.Request(
                url,
                self.parse_item,
                dont_filter=True,
                errback=self.errback_http_ignored,
                headers=headers
            )
    
    def parse_item(self, response):
        data_optipns = response.xpath('//div[@class="dinamyc-configurable-products has-items"]/@data-options').extract()
        for item in data_optipns:
            yield{'variants': json.loads(item)}
            
        next_url = response.xpath('//a[@class="next i-next"]/@href').extract_first()
        print('*'*100, next_url)
        if next_url:
            headers = {
                'User-Agent': get_user_agent('random'),
                **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
            }
            
            yield scrapy.Request(
                next_url,
                self.parse_item,
                dont_filter=True,
                errback=self.errback_http_ignored,
                headers=headers
            )
            
        gc.collect()
        
    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 430:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(240)  # Wait for 4 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

            if response.status == 503:
                self.logger.info(f"Ignoring response {response.url} with status code {response.status}")
                time.sleep(480)  # Wait for 8 minutes (adjust as needed)
                return self._retry_request(response.request, reason=failure.getErrorMessage(), spider=self)

    def _retry_request(self, request, reason, spider):
        retryreq = request.copy()
        retryreq.meta['retry_times'] = request.meta.get('retry_times', 0) + 1
        retryreq.dont_filter = True
        return retryreq
    
    

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start()  # The script will block here until the crawling is finished
