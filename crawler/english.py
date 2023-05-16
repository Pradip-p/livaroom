#!/usr/bin/env python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
import base64
from lazy_crawler.lib.user_agent import get_user_agent
import gc
import json
import js2xml
import time

class LazyCrawler(LazyBaseCrawler):

    name = "englishelm"

    allowed_domains = ['englishelm.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 4,'LOG_LEVEL': 'DEBUG',
        
        'CONCURRENT_REQUESTS' : 1,'CONCURRENT_REQUESTS_PER_IP': 1,

        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,'RETRY_TIMES': 2,

        "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,

        'ITEM_PIPELINES' :  {
            'lazy_crawler.crawler.pipelines.EnglishElmDBPipeline': 300
        }
    }
    categories = [
        {'living':['https://englishelm.com/collections/living-room-furniture'],
         'dining':['https://englishelm.com/collections/dining-room-furniture'],
         'bed':['https://englishelm.com/collections/bedroom-furniture'],
         'lighting':['https://englishelm.com/collections/lighting-collection-1'],
         'rugs':['https://englishelm.com/collections/rugs'],
         'outdoor':['https://englishelm.com/collections/outdoor-collection'],
         'accessories':['https://englishelm.com/collections/accessories'],
         'kitchen':['https://englishelm.com/collections/kitchen-collection']
        }
    ]
    proxy = 'p.webshare.io:80'
    # user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    user_pass = base64.encodebytes("gkoffhkj-rotate:9qsx6zrpagq6".encode()).decode()

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
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
        ###add
        # 'Proxy-Authorization': 'Basic ' + user_pass,
    }

    def start_requests(self): #project start from here.
        for category in self.categories:
            category = category.items()
            for key, value in category:
                category_name = key
                urls = value
                for url in urls:
                    time.sleep(5)
                    yield scrapy.Request(url, self.parse_json, dont_filter=True,
                        # meta={'proxy': 'http://' + self.proxy},
                        headers= self.HEADERS
                        )
        # url = 'https://englishelm.com/collections/all'
        # yield scrapy.Request(url, self.parse_json, dont_filter=True,headers=self.HEADERS)


    def parse_json(self, response):
        # script_content = response.xpath('//script[@id="web-pixels-manager-setup"]/text()').extract_first()
        next_script_content = response.xpath('//script[@id="web-pixels-manager-setup"]/following-sibling::script[not(@id)]/text()').extract_first()
        parsed = js2xml.parse(next_script_content)
        # meta_dict = json.loads(parsed.xpath("//var[@name='meta']/object")[0].to_dict())['object']

        results = js2xml.jsonlike.make_dict(
            parsed.xpath("//var[@name='meta']/object")[0])
        products = results['products']
        # yield {'products':products}
        for product in products:
            yield{"variants": product['variants'] } 
            
        time.sleep(5)

        # scripts = response.css('#web-pixels-manager-setup').get('')

        # start_index = scripts.find('{"collection"')
        # end_index = scripts.find('});}', start_index) + 1
        # json_data = scripts[start_index:end_index]

        # json_load = json.loads(json_data)
        # data = json_load['collection']
        # productVariants = data['productVariants']
        # variants = []
        # for product in productVariants:
        #     src = product['image'].get('src')
        #     price = product['price'].get('amount')
        #     title = product['product'].get('title')
        #     vendor = product['product'].get('vendor')
        #     type_ = product['product'].get('type')
        #     sku = product['sku']
        #     barcode = product['id']
        #     variant =  {
        #         'sku':sku,
        #         'price':price,
        #         'title':title,
        #         'vendor':vendor,
        #         'barcode':barcode
        #     }
        #     variants.append(variant)

        # yield {'variants': variants}

        next_page = response.xpath('//ul[@class="pagination-page"]/li[@class="text"]/a[@title="Next"]/@href').extract_first()
        if next_page:
            url = 'https://englishelm.com{}'.format(next_page)
            time.sleep(5)
            yield scrapy.Request(url, self.parse_json, dont_filter=True,
                    # meta={'proxy': 'http://' + self.proxy},
                    headers= self.HEADERS
                    )

        gc.collect()

settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished