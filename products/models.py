from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Min, Avg

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
    
# class Product(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
#     subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='product')
#     product_id = models.CharField(max_length=200, unique=True)
#     title = models.CharField(max_length=200)
#     handle = models.CharField(max_length=200)
#     published_at = models.DateTimeField()
#     created_at = models.DateTimeField()
#     vendor = models.CharField(max_length=200)
#     product_type = models.CharField(max_length=200)
#     tags = models.CharField(max_length= 200)
#     price = models.CharField(max_length=200)
#     price_min = models.CharField(max_length=200)
#     price_max = models.CharField(max_length=200)
#     available = models.CharField(max_length=200)
#     price_varies = models.CharField(max_length=200)
#     product_url = models.CharField(max_length=200) 
#     description = models.TextField()
#     featured_image = models.ImageField(default='producsts/features/images', blank=True)
#     # make all thumbnails at most 140x140pixels

#     def __str__(self):
#         return self.title
    
    


class Variant(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant')
    title = models.CharField(max_length=200)
    sku = models.CharField(max_length=200, unique=True)
    # requires_shipping = models.CharField(max_length=200),
    # taxable = models.CharField(max_length=200),
    price_englishelm = models.CharField(max_length=200, blank=True)
    price_livaroom = models.CharField(max_length=200, blank=True)
    # inventory_management = models.CharField(max_length=200)
    barcode = models.CharField(max_length=200)



    def optimize_price(self):
        # Calculate the absolute difference between the two prices
        abs_diff = abs(float(self.price_englishelm) - float(self.price_livaroom))

        # Calculate the percentage change between the two prices
        if float(self.price_livaroom) != 0:
            percentage_change = abs_diff / float(self.price_livaroom) * 100
        else:
            percentage_change = 0

        # Calculate the related price based on the sign of the price difference
        related_price = float(self.price_englishelm)
        if float(self.price_englishelm) >= float(self.price_livaroom):
            related_price -= float(self.price_englishelm) * percentage_change / 100
        else:
            related_price += float(self.price_englishelm) * percentage_change / 100

        return related_price

    def __str__(self):
        return self.title
    
class Product(models.Model):
    category_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    sku = models.CharField(max_length=200)
    handle = models.CharField(max_length=200)
    price_englishelm = models.CharField(max_length=200, blank=True)
    price_livaroom = models.CharField(max_length=200, blank=True)
    barcode = models.CharField(max_length=200)
    featured_image = models.CharField(max_length=200)

    def __str__(self):
        return self.title
