from django.db import models
from django.utils.text import slugify

# Create your models here.
class EnglishemlVendor(models.Model):
    product_id = models.CharField(max_length=200)
    type = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate slug from name if it is not already set
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

class EnglisemProduct(models.Model):
    variant_id = models.CharField(max_length=200)
    vendor = models.ForeignKey(EnglishemlVendor, on_delete=models.CASCADE, related_name='englishelm_product')
    public_title = models.CharField(max_length=200,null=True, blank=True)
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200)
    price = models.CharField(max_length=200)

    def __str__(self):
        return self.title