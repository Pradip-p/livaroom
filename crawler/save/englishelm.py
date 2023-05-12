import os
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lazy_crawler.crawler.spiders.base_crawler import LazyBaseCrawler
from lazy_crawler.lib.cleaner import strip_html
import base64
from lazy_crawler.lib.user_agent import get_user_agent
import gc

class LazyCrawler(LazyBaseCrawler):

    name = "englishelm"

    custom_settings = {
    'DOWNLOAD_DELAY': 2,
    'LOG_LEVEL': 'DEBUG',
    'CONCURRENT_REQUESTS': 1,  # Increase to handle more simultaneous requests
    'CONCURRENT_ITEMS': 32,  # Increase to handle more simultaneous items being processed
    'CONCURRENT_REQUESTS_PER_IP': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'RETRY_TIMES': 2,
    'COOKIES_ENABLED': True,
    'DOWNLOAD_TIMEOUT': 180,
    'ITEM_PIPELINES': {
        'lazy_crawler.crawler.pipelines.DjangoDBPipeline': None
    }
}


    # custom_settings = {
    #     'DOWNLOAD_DELAY': 0.5,
    #     'LOG_LEVEL': 'DEBUG',
    #     'CONCURRENT_REQUESTS' : 32,'CONCURRENT_REQUESTS_PER_IP': 32,
    #     'CONCURRENT_REQUESTS_PER_DOMAIN': 32,'RETRY_TIMES': 200,
    #     "COOKIES_ENABLED": True,'DOWNLOAD_TIMEOUT': 180,
    #     'ITEM_PIPELINES' :  {
    #     'lazy_crawler.crawler.pipelines.DjangoDBPipeline': None
    #     }
    # }
    
    proxy = 'p.webshare.io:80'
    # user_pass = base64.encodebytes("hpiukvrn-rotate:yahyayahya".encode()).decode()
    user_pass = base64.encodebytes("gkoffhkj-rotate:9qsx6zrpagq6".encode()).decode()
    
    def start_requests(self): #project start from here.
        url = 'https://englishelm.com/collections/all'

        yield scrapy.Request(url, self.parse_url, dont_filter=True,
            meta={'proxy': 'http://' + self.proxy},
            headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
            'User-Agent': get_user_agent('random')
            })

    def parse_url(self, response):
        urls = response.xpath('//div[@class="product-image image-swap"]/a[@class="product-grid-image"]/@href').extract()
        for _url in urls:
            url = 'https://englishelm.com{}{}'.format(_url,'.js')
            
            yield scrapy.Request(url, self.parse_details, dont_filter=True, 
                meta={'proxy': 'http://' + self.proxy,
                },
                headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
                'User-Agent': get_user_agent('random')
                })

        next_url = response.xpath('//ul[@class="pagination-page"]/li[last()]/a/@href').extract_first()
        if next_url:
            url = 'https://englishelm.com{}'.format(next_url)
            print('*'*100, next_url)

            yield scrapy.Request(url, self.parse_url, dont_filter=True,
                meta={'proxy': 'http://' + self.proxy,
                },
                headers={'Proxy-Authorization': 'Basic ' + self.user_pass,
                'User-Agent': get_user_agent('random')
            })

    def parse_details(self, response):
        res = response.json()
        p_handle = res['handle']
        p_id = res['id'] 
        p_title = res['title']
        p_description = res['description']
        p_published_at = res['published_at']
        p_created_at = res['created_at']
        p_vendor = res['vendor']
        p_tags = res['tags']
        p_price = int(res['price']) / 100
        p_price_min = int(res['price_min']) / 100
        p_price_max = int(res['price_max']) / 100
        p_available = res['available']
        p_price_varies = res['price_varies']
        p_url = res['url']
        product_url = 'https://englishelm.com{}'.format(p_url)
        p_prodcut_type = res['type']
        p_featured_image = 'https:{}'.format(res['featured_image'])

        # images = res['images']
        variants = res['variants']
        variant_list = []
        for variant in variants:
            _id = variant['id']
            sku = variant['sku'].strip()
            price = int(variant['price'])/100
            name = variant['name']
            barcode = variant['barcode']

            variant_dict = {
                '_id': _id,
                'title': name,
                'sku': sku,
                'price':  price,
                'barcode':barcode
            }
            variant_list.append(variant_dict)
            
        yield {
            'product_id': p_id,
            'handle':p_handle,
            'published_at':p_published_at,
            'created_at':p_created_at,
            'vendor':p_vendor,
            'prodcut_type':p_prodcut_type,
            'tags':p_tags,
            'title': p_title,
            'price': p_price,
            'price_min':p_price_min,
            'price_max':p_price_max,
            'available':p_available,
            'price_varies':p_price_varies,
            'product_url': product_url,
            'featured_image': p_featured_image,
            'description': strip_html(str(p_description)),
            'variants': variant_list
        }
        gc.collect()


settings_file_path = 'lazy_crawler.crawler.settings'
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
process = CrawlerProcess(get_project_settings())  
process.crawl(LazyCrawler)
process.start() # the script will block here until the crawling is finished