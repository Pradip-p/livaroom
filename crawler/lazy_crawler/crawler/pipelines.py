import json
from scrapy import signals
import datetime
import os
import django
from pathlib import Path
import sys
from django.db import transaction
import json
from itemadapter import ItemAdapter
from scrapy.utils.serialize import ScrapyJSONEncoder

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

sys.path.append(str(BASE_DIR))  # Add the base directory to the PYTHONPATH

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from products.models import Product, Vendor, Category

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
        vendor_name = item.get('vendor')
        ###to save vendor first....
        try:
            vendor = Vendor.objects.get(name=vendor_name)
        except Vendor.DoesNotExist:
            vendor = Vendor.objects.create(name=vendor_name)
        ###now save the variant
        for variant in variants:
            title = product_title+' - '+variant.get('title')
            sku = variant.get('sku')
            price_livaroom = variant.get('price')
            variant_id = variant.get('id')
            if variant.get('barcode'):
                barcode = variant.get('barcode')
            else:
                barcode = 'NA'

            try:
                # Attempt to retrieve an existing Product object with the given SKU
                product = Product.objects.get(sku=sku)
                # If the object exists, update its attributes with the new data
                vendor = vendor
                product_id = product_id
                variant_id = variant_id
                product.title = title
                product.handle = handle
                product.barcode = barcode
                product.vendor  = vendor

                # product.featured_image = featured_image
                product.price_livaroom = price_livaroom
                
                product.save()  # Save the changes to the database
                
            except Product.DoesNotExist:
                # If the object doesn't exist, create a new one
                product = Product.objects.create(
                    vendor=vendor,
                    product_id=product_id, 
                    variant_id = variant_id,
                    title=title, handle=handle,
                    sku=sku, barcode=barcode,
                    price_livaroom=price_livaroom,
                    )

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
                sku = variant.get('sku')
                # existing_product = Product.objects.get(sku= sku)
                # if existing_product:
                #     existing_product.price_englishelm = variant.get('price')
                #     existing_product.save()
                #     print('update the price')
                    
                # else:
                skus = variant.get('sku').split('-')
                for sku in skus:
                    product = Product.objects.get(sku= sku)
                    if product:    
                        product.price_englishelm = variant.get('price')
                        product.save()
                        
            except Product.DoesNotExist:
                pass
        return ''

class Stopbedrooms(object):
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
        try:
            existing_product = Product.objects.get(sku= item.get('sku'))
            if existing_product:
                existing_product.price_1stopbedrooms = item.get('price').replace("$", "")
                existing_product.url_1stopbedrooms = item.get('link')
                existing_product.save()
                print('found n save')
                    
        except Product.DoesNotExist:
            pass
            
        return ''

