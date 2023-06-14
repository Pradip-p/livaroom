from django.db import models
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=50)


    def save(self, *args, **kwargs):
        # Generate slug from name if it is not already set
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate slug from name if it is not already set
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)




class Product(models.Model):
    """
    Represents a product.

    Fields:
        product_id (CharField): The product ID (maximum length: 200 characters).
        variant_id (CharField): The variant ID (maximum length: 200 characters).
        title (CharField): The title of the product (maximum length: 200 characters).
        sku (CharField): The SKU (Stock Keeping Unit) of the product (maximum length: 200 characters, must be unique).
        handle (CharField): The handle of the product (maximum length: 200 characters).
        price_englishelm (CharField): The price in the English Elm currency (maximum length: 200 characters, blank allowed).
        price_livaroom (CharField): The price in the Livaroom currency (maximum length: 200 characters, blank allowed).
        barcode (CharField): The barcode of the product (maximum length: 200 characters).
        featured_image (CharField): The URL of the featured image of the product (maximum length: 200 characters, blank allowed).
    """
     
    product_id = models.CharField(max_length=200)
    variant_id = models.CharField(max_length=200)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='product')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    title = models.CharField(max_length=200)
    sku = models.CharField(max_length=200,unique=True)
    handle = models.CharField(max_length=200)
    price_englishelm = models.CharField(max_length=200, blank=True)
    price_livaroom = models.CharField(max_length=200, blank=True)
    price_coleman = models.CharField(max_length=200, null=True, blank=True)
    barcode = models.CharField(max_length=200)
    featured_image = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def product_url(self):
        return f'https://livaroom.com/products/{self.handle}'

    def optimize_price(self):
        if self.price_englishelm:
            return float(self.price_englishelm)/100
        else:
            return 'NA'
    
    @classmethod
    def get_total_count(cls):
        """
        Get the total count of objects in the class.

        Returns:
        The total count of objects in the class.

        Note:
        - This function is a class method, meaning it can be called on the class itself (cls) rather than an instance of the class.
        - It assumes the existence of a class with objects.
        - The function uses Django's count() method on the class's objects manager (cls.objects) to retrieve the total count of objects in the class.
        """
        return cls.objects.count()

    @classmethod
    def matching_product_count(cls):
        """
        Calculate the count of objects in the class that have both 'price_englishelm' and 'price_livaroom' attributes.

        Returns:
        The count of objects in the class that have values for both 'price_englishelm' and 'price_livaroom' attributes.

        Note:
        - This function is a class method, meaning it can be called on the class itself (cls) rather than an instance of the class.
        - It assumes the existence of a class with objects that have 'price_englishelm' and 'price_livaroom' attributes.
        - The function uses a generator expression to iterate over all objects in the class and count those that meet the condition (have values for both 'price_englishelm' and 'price_livaroom').
        """
        count = sum(1 for obj in cls.objects.all() if obj.price_englishelm and obj.price_livaroom)
        return count
# {'id': 7566535786663, 'gid': 'gid://shopify/Product/7566535786663', 'vendor': 'TOV Furniture', 'type': 'Ottomans and Trunks', 'variants': [{'id': 43105494433959, 'price': 11697, 'name': '"Wasn\'t Me" Storage Ottoman - Chocolate Brown / Long', 'public_title': 'Chocolate Brown / Long', 'sku': 'TOV-OC68598'}, {'id': 43105494532263, 'price': 8297, 'name': '"Wasn\'t Me" Storage Ottoman - Chocolate Brown / Round', 'public_title': 'Chocolate Brown / Round', 'sku': 'TOV-OC68597'}, {'id': 43105494565031, 'price': 11697, 'name': '"Wasn\'t Me" Storage Ottoman - Olive Green / Long', 'public_title': 'Olive Green / Long', 'sku': 'TOV-OC68600'}, {'id': 43105494696103, 'price': 8297, 'name': '"Wasn\'t Me" Storage Ottoman - Olive Green / Round', 'public_title': 'Olive Green / Round', 'sku': 'TOV-OC68599'}]}