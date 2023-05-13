from scrapy import signals
import datetime
import os
import django
from pathlib import Path
import sys
from django.db.models import Q
from django.db import transaction

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

sys.path.append(str(BASE_DIR))  # Add the base directory to the PYTHONPATH

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Variant, Product

class LivaroomDBPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass
    
    @transaction.atomic
    def process_item(self, item, spider):
        handle = item.get('handle')
        category_name = item.get('category_name')
        variants = item.get('variants')
        for variant in variants:
            title = variant.get('name')
            sku = variant.get('sku')
            price_englishelm = variant.get('price')
            
            if variant.get('barcode'):
                barcode = variant.get('barcode')
            else:
                barcode = 'NA'

            if variant['featured_image']:
                if variant['featured_image'].get('src'):
                    featured_image = variant['featured_image'].get('src')
                else:
                    featured_image = 'NA'
            else:
                featured_image = 'NA'


            Product.objects.create(category_name=category_name, title=title,
                                   handle=handle, sku=sku, barcode=barcode,featured_image=featured_image,
                                   price_englishelm=price_englishelm)
        return item
    
            # try:
            #     featured_image = variant['featured_image'].get('src')
            #     existing_product = Variant.objects.get(sku=variant.get('sku'))
            #     existing_product.price_livaroom = variant.get('price')
            #     existing_product.save()
            #     return variant
            # except Variant.DoesNotExist:
            #     return ''



class EnglishElmDBPipeline(object):
    def __init__(self):
        self.created_time = datetime.datetime.now()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass
    
    @transaction.atomic
    def process_item(self, item, spider):
        
        variants = item.get('variants')

        for variant in variants:
            try:
                Variant.objects.get(sku=variant.get('sku'))
                print('*'*100, 'This product is already exist.')
            except Variant.DoesNotExist:
                Variant.objects.create(
                    title = variant.get('name'),
                    sku = variant.get('sku'),
                    price_englishelm = variant.get('price'),
                    barcode = variant.get('id')
                )                
                return variant
            