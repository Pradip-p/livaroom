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
        'DOWNLOAD_DELAY': 2,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 32,
        'CONCURRENT_REQUESTS_PER_IP': 32,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 13,
        'RETRY_TIMES': 2,
        # "COOKIES_ENABLED": True,
        'DOWNLOAD_TIMEOUT': 10,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.Stopbedrooms': 300
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
        urls = ['https://www.1stopbedrooms.com/brand/lh-imports',
                'https://www.1stopbedrooms.com/brand/malouf',
                'https://www.1stopbedrooms.com/brand/modway',
                'https://www.1stopbedrooms.com/brand/j-and-m',
                'https://www.1stopbedrooms.com/brand/manhattan-comfort',
                'https://www.1stopbedrooms.com/brand/moes-home',
                'https://www.1stopbedrooms.com/brand/baxton-studio',
                'https://www.1stopbedrooms.com/brand/meridian',
                'https://www.1stopbedrooms.com/brand/zuo-modern',
                ]
        # url = 'https://www.1stopbedrooms.com/brand/modway'
    
        for url in urls:
            yield scrapy.Request(
            url,
            self.parse_item,
            dont_filter=True,
            errback=self.errback_http_ignored,
            headers=headers
            )
            
        # url = 'https://www.1stopbedrooms.com/all-furniture'
        # url = 'https://www.1stopbedrooms.com/bedroom/beds'
        # url = 'https://www.1stopbedrooms.com/brand/malouf'
        
        
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
        product_urls = response.xpath('//span[@class="product-name"]/a/@href').extract()
        for url in product_urls:
            headers = {
                'User-Agent': get_user_agent('random'),
                **self.HEADERS,  # Merge the HEADERS dictionary with the User-Agent header
            }
            
            yield scrapy.Request(
                url,
                self.parse_sku,
                dont_filter=True,
                errback=self.errback_http_ignored,
                headers=headers,
                meta={'data_optipns': data_optipns}
            )
        #next page
        next_url = response.xpath('//a[@class="next i-next"]/@href').extract_first()
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
            
    def parse_sku(self, response):
        start_index = response.text.find('var inline_scripts_data')
        if start_index != -1:
            start_index = response.text.find('{"protection_plan":', start_index)
            if start_index != -1:
                end_index = response.text.find('};', start_index) + 1
                json_data = response.text[start_index:end_index]
                data = json.loads(json_data)
                products = data.get('bloomreachPixelProducts')
                
                data_optipns = response.meta['data_optipns']
                
                for id, product in products.items():
                    # yield product 
                    sku = product['sku']
                    mpn = product['mpn']
                    for data in data_optipns:
                        data = json.loads(data)
                        for id, item in data.items():
                            if item['upc'] == sku:
                                item['sku'] = mpn
                                yield item
                                
                                
                                
                            # {'is_mattress': False, 'image': 'https://cdn.1stopbedrooms.com/media/i/catalog:keepframe/catalog/product/g/r/gracelton-cream-velvet-king-bed_0qb24396204.jpg', 'imageclass': None, 'hoverimage': 'https://cdn.1stopbedrooms.com/media/i/catalog:keepframe/catalog/product/g/r/gracelton-cream-velvet-king-bed_0qb24396204_1.jpg', 'hoverimageclass': '', 'name': 'Gracelton Cream Velvet King Bed', 'link': 'https://www.1stopbedrooms.com/gracelton-cream-velvet-king-bed', 'upc': '0qb24396204', 'product_ships_via': 'Free Delivery', 'quick_ship': False, 'price': '$1,680.00', 'old_price': '$1,920.59', 'is_instock': True}

                    # {'prod_id': 'qb1222261', 'sku': 'qb1222261', 'name': 'Donnica Silver Accent Sconce', 'mpn': 'A8010154', 'url': 'https://www.1stopbedrooms.com/donnica-silver-accent-sconce', 'producttype': 'Wall Sconce', 'img': 'https://cdn.1stopbedrooms.com/media/i/thumb_72:keepframe/catalog/product/d/o/donnica-silver-accent-sconce_qb1222261.jpg'}
                
                # print(data_optipns)
            else:
                print("Data not found")
        else:
            print("Variable not found")

        
            
        gc.collect()
        
    def errback_http_ignored(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            if response.status in  [430, 403]:
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
