from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Min, Avg
from django.db.models import Q

# Create your models here.
# class Category(models.Model):
#     name = models.CharField(max_length=150, unique=True)
#     slug = models.SlugField(max_length=50)


#     def save(self, *args, **kwargs):
#         # Generate slug from name if it is not already set
#         if not self.slug:
#             self.slug = slugify(self.name)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name


# class SubCategory(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_category')
#     name = models.CharField(max_length=150, unique=True)
#     slug = models.SlugField(max_length=50)

#     def save(self, *args, **kwargs):
#         # Generate slug from name if it is not already set
#         if not self.slug:
#             self.slug = slugify(self.name)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.name
        
class Product(models.Model):
    category_name = models.CharField(max_length=200, blank=True)
    product_id = models.CharField(max_length=200)
    variant_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    sku = models.CharField(max_length=200,unique=True)
    handle = models.CharField(max_length=200)
    price_englishelm = models.CharField(max_length=200, blank=True)
    price_livaroom = models.CharField(max_length=200, blank=True)
    barcode = models.CharField(max_length=200)
    featured_image = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def product_url(self):
        # if not isinstance(self.handle, str):
        #     raise TypeError("Product handle must be a string")
        return f'https://livaroom.com/products/{self.handle}'

    def optimize_price(self):
        if self.price_englishelm:
            return float(self.price_englishelm)/100
        else:
            return 'NA'
    
    @classmethod
    def get_total_count(cls):
        return cls.objects.count()

    @classmethod
    def matching_product_count(cls):
        count = sum(1 for obj in cls.objects.all() if obj.price_englishelm and obj.price_livaroom)
        return count