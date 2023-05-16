#!/usr/bin/env python
import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
import gc
import json
import time
import shopify
from shopify import PaginatedIterator

class LazyCrawler(LazyBaseCrawler):

    name = "livaroom"

    allowed_domains = ['livaroom.com']

    custom_settings = {
        'DOWNLOAD_DELAY': 4,
        'LOG_LEVEL': 'DEBUG',
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 2,
        'COOKIES_ENABLED': True,
        'DOWNLOAD_TIMEOUT': 180,
        'ITEM_PIPELINES': {
            'lazy_crawler.crawler.pipelines.LivaroomDBPipeline': 400
        }
    }

    start_urls  = ['https://livaroom.com/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        API_KEY = "2b4e323d3129443363269802ebca49df"
        API_SECRET_KEY = '60d668593ffa6e9a65d3e02301c37d0d'
        API_ACCESS_TOKEN = "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"
        api_version = "2023-01"  # Set your desired API version

        SHOP_NAME = 'livaroom'

        shop_url = f"https://{API_KEY}:{API_ACCESS_TOKEN}@{SHOP_NAME}.myshopify.com/admin/api/2023-01"
        shopify.ShopifyResource.set_site(shop_url)
        self.shop = shopify.Shop.current()

    def parse(self, response):
        # Retrieve all products
        for page in PaginatedIterator(shopify.Product.find()):
            # for items in page:

            # Iterate over each product
            for product in page:
                data = product.to_json()
                json_data = data.decode('utf-8')  # Decode the bytes data into a string
                json_data = json.loads(json_data)
                product_data = json_data['product']
                yield product_data
        gc.collect()


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished