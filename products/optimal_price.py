from django.db.models import Min, Avg
from .models import Product

# Assuming you have already retrieved competitor data and stored it in a separate table


def calculate_optimal_price(product_id):
    # Retrieve the lowest price among competitors for the product
    lowest_price = Product.objects.filter(product_id=product_id).aggregate(Min('price'))['price__min']

    # Retrieve the average price among competitors for the product
    avg_price = Product.objects.filter(product_id=product_id).aggregate(Avg('price'))['price__avg']

    # Determine your profit margin (in this example, we'll use a 20% margin)
    cost = 10  # replace with your actual cost of producing the product
    profit_margin = 0.2
    target_margin = cost * (1 + profit_margin)

    # Determine the demand for the product (in this example, we'll use a demand score of 0.8)
    demand_score = 0.8

    # Calculate the optimal price
    optimal_price = max(lowest_price, avg_price * demand_score, target_margin)
    return optimal_price
    # # Update the product price in the database
    # product = Product.objects.get(product_id=product_id)
    # product.price = str(optimal_price)
    # product.save()

    # return optimal_price
