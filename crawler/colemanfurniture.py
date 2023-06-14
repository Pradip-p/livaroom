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
    
    name = "colemanfurniture"

    allowed_domains = ['colemanfurniture.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2,
        # "COOKIES_ENABLED": True,
        'DOWNLOAD_TIMEOUT': 180,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.ColemanDBPipeline': 300
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
    page_number = 1
    
    def start_requests(self):  # Project starts from here.
        headers = {
            'User-Agent': get_user_agent('random'),
            **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
        }
        url = 'https://colemanfurniture.com/living/sofas.htm?p=1'
        yield scrapy.Request(
            url,
            self.parse_json,
            dont_filter=True,
            errback=self.errback_http_ignored,
            headers=headers
        )
    
    def parse_json(self, response):
        next_script_content = response.xpath('//script[@type="application/json"]/text()').extract_first()
        start_index = next_script_content.find('{"data":')  # Find the starting index of the JSON data

        if start_index != -1:
            json_str = next_script_content[start_index:].replace('<!--', '').replace('-->', '')  # Remove the HTML comments
            data = json.loads(json_str)['data']
            products = data['content']['reflektionPayload']['batch'][0]['content']['product']['value']
            yield {"variants": products}
            
            # Next page.
            page = data['content']['reflektionPayload']['batch'][0]
            self.page_number += 1
            total_page = page['total_page']
            
            if self.page_number <= total_page:
                headers = {
                    'User-Agent': get_user_agent('random'),
                    **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
                }
                url = 'https://colemanfurniture.com/living/sofas.htm?p={}'.format(self.page_number)
                yield scrapy.Request(
                    url,
                    self.parse_json,
                    dont_filter=True,
                    errback=self.errback_http_ignored,
                    headers=headers
                )
        
        gc.collect()

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start()  # The script will block here until the crawling is finished
