from django import template
from ..models import Product, Vendor, Category

register = template.Library()

@register.simple_tag
def get_total_product_count():
    return Product.get_total_count()

@register.simple_tag
def get_matching_product_count():
    return Product.matching_product_count()


@register.simple_tag
def get_vendor():
    return Vendor.objects.all()

@register.simple_tag
def get_categories():
    return Category.objects.all()