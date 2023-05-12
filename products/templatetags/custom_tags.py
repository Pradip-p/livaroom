# from django import template
# from django.db.models import Avg, Min
# from ..models import Product

# register = template.Library()

# @register.simple_tag
# def optimal_price(product_id):
#     lowest_price = Product.objects.filter(product_id=product_id).aggregate(Min('price'))['price__min']
#     avg_price = Product.objects.filter(product_id=product_id).aggregate(Avg('price'))['price__avg']
#     cost = 10  # replace with your actual cost of producing the product
#     profit_margin = 0.2
#     target_margin = cost * (1 + profit_margin)
#     demand_score = 0.8
#     optimal_price = max(lowest_price, avg_price * demand_score, target_margin)
#     return optimal_price
