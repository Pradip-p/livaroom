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

from products.models import Variant

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
        variants = item.get('variants')
        for variant in variants:
            try:
                existing_product = Variant.objects.get(sku=variant.get('sku'))
                existing_product.price_livaroom = variant.get('price')
                existing_product.save()
                return variant
            except Variant.DoesNotExist:
                return ''



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
            