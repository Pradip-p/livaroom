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

from products.models import Product

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
        product_id = item.get('id')
        handle = item.get('handle')
        product_title = item['title']
        category_name = ''
        variants = item.get('variants')
        for variant in variants:
            title = product_title+' - '+variant.get('title')
            sku = variant.get('sku')
            price_livaroom = variant.get('price')
            variant_id = variant.get('id')
            if variant.get('barcode'):
                barcode = variant.get('barcode')
            else:
                barcode = 'NA'

            # if variant['featured_image']:
            #     if variant['featured_image'].get('src'):
            #         featured_image = variant['featured_image'].get('src')
            #     else:
            #         featured_image = 'NA'
            # else:
            #     featured_image = 'NA'

            try:
                # Attempt to retrieve an existing Product object with the given SKU
                product = Product.objects.get(sku=sku)
                
                # If the object exists, update its attributes with the new data
                product_id = product_id
                variant_id = variant_id
                product.category_name = category_name
                product.title = title
                product.handle = handle
                product.barcode = barcode
                # product.featured_image = featured_image
                product.price_livaroom = price_livaroom
                
                product.save()  # Save the changes to the database
                
            except Product.DoesNotExist:
                # If the object doesn't exist, create a new one
                product = Product.objects.create(
                    product_id=product_id, variant_id = variant_id,
                    category_name=category_name, title=title, handle=handle,
                    sku=sku, barcode=barcode,
                    price_livaroom=price_livaroom)

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
                existing_product = Product.objects.get(sku=variant.get('sku'))
                existing_product.price_englishelm = variant.get('price')
                existing_product.save()
                return variant
            except Product.DoesNotExist:
                return ''