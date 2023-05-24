from django.shortcuts import render
from .models import Product
from .pagination import set_pagination
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import shopify
import json
from django.db.models import Q
from englishelm.models import EnglisemProduct, EnglishemlVendor

@login_required(login_url='/')
def vendor_view(request,slug):
    variants = [variant for variant in Product.objects.filter(vendor__slug = slug).distinct() if variant.price_englishelm]
    variants = set_pagination(request, variants)
    context = {
            'variants':variants,
            }
    return render(request, "back/home.html", context)

@login_required(login_url='/')
def category_view(request, slug):
    # Logic for the category view goes here
    # You can access the 'slug' parameter in this function
    variants = [variant for variant in Product.objects.filter(category__slug=slug).distinct() if variant.price_englishelm]
    variants = set_pagination(request, variants)
    context = {
            'variants':variants,
            }
    return render(request, "back/home.html", context)


@login_required(login_url='/')
def update_product_price(request):
    if request.method == "POST":
        prices_json = request.POST.get('prices')
        prices = json.loads(prices_json)
        prices = {key: value for key, value in prices.items() if value != 'NA'}
        # Update the value in the database or perform any other operations
        API_KEY = "2b4e323d3129443363269802ebca49df"
        API_ACCESS_TOKEN = "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"
        SHOP_NAME = 'livaroom'
        shop_url = f"https://{API_KEY}:{API_ACCESS_TOKEN}@{SHOP_NAME}.myshopify.com/admin/api/2023-01"
        shopify.ShopifyResource.set_site(shop_url)
        shop = shopify.Shop.current()
        # now i want to update the prices of each prodcuts
        # variant_sku = 'AR-9511'
        if prices:
            update_price = []
            for sku, price in prices.items():
            #     variant_sku = 'EEI-5805-CHE-WHI-WHI'
                variant = Product.objects.get(sku=sku)
                if variant:
                    product_id = variant.product_id
                    variant_id = variant.variant_id
                    # Find the product variant based on SKU on Livaroom API(site)..
                    product = shopify.Product(dict(id=product_id))
                    # variant = shopify.Variant(dict(id=variant_id, price=price)) #55.04
                    # product.add_variant(variant) #it does not mean add new varinat it update the existing price of variant.
                    # product.save()
                    update_price.append(price)
            return JsonResponse({'message': 'Price {} updated successfully.'.format(','.join(update_price))}, status=200,)
        return JsonResponse({'message': 'Please set a valid price. "NA" is not a valid price for the product.'}, status=500)
    return JsonResponse({'message':'invalid request.'}, status=500)


@login_required(login_url='/')
def update_view(request):
    if request.method == 'POST':
        sku = request.POST.get('sku')
        price = request.POST.get('price')
        if not sku or not price or price == 'NA' or price.strip() == '':
            return JsonResponse({'message': 'Invalid or Empty Price Found.'}, status=500)
        
        # Update the value in the database or perform any other operations
        API_KEY = "2b4e323d3129443363269802ebca49df"
        API_ACCESS_TOKEN = "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"

        SHOP_NAME = 'livaroom'

        shop_url = f"https://{API_KEY}:{API_ACCESS_TOKEN}@{SHOP_NAME}.myshopify.com/admin/api/2023-01"
        shopify.ShopifyResource.set_site(shop_url)
        shop = shopify.Shop.current()
        #now i want to update the prices of each prodcuts
        # variant_sku = 'AR-9511'
        variant_sku = 'EEI-5805-CHE-WHI-WHI'
        #let's check we found the varinat our database
        variant = Product.objects.get(sku=sku)
        if variant:
            product_id = variant.product_id
            variant_id = variant.variant_id
            # Find the product variant based on SKU on Livaroom API(site)..
            product = shopify.Product(dict(id=product_id))
            # variant = shopify.Variant(dict(id=variant_id, price=price)) #55.04
            # product.add_variant(variant) #it does not mean add new varinat it update the existing price of variant.
            # product.save()
            return JsonResponse({'message': 'Price {} updated successfully.'.format(price)}, status=200, safe=False)
        else:
            return JsonResponse({'message': 'SKU Not Found.'}, status=500)
    # return JsonResponse({'message': 'Price {} updated successfully.'.format(price)}, status=200, safe=False)
        

@login_required(login_url='/')
def search_product(request):
    """
    Search for products based on the SKU parameter in the request and return the corresponding results.

    Args:
    request: The HTTP request object.

    Returns:
    If the request method is 'GET', the function searches for products based on the SKU parameter. If the SKU parameter is provided, it filters the Product objects based on the SKU (case-insensitive) and returns the variants along with a message indicating to show the products based on price availability. If the SKU parameter is not provided, it retrieves all Product objects, orders them by descending ID, filters out variants with no price_livaroom value, paginates the results using the set_pagination function, and returns the paginated variants.

    Note:
    - This function assumes the use of Django's render function to render the 'back/product_table.html' template.
    - The function relies on the set_pagination function to perform pagination for the results.
    - The function assumes the existence of a Product model with the necessary fields (e.g., sku, price_livaroom) in the Django project.
    - If an error occurs during the SKU filtering process, a message is rendered indicating the need to select a country.
    """
    if request.method == 'GET':
        sku = request.GET.get('sku')
        if sku:
            try:
                # variants = Product.objects.filter(sku__icontains=sku).distinct()
                variants = [variant for variant in Product.objects.filter(sku__icontains=sku).distinct() if variant.price_englishelm]
                variants = set_pagination(request, variants)
                context = {'variants':variants, 'message':'show the products based on price avaiable'}
                return render(request, 'back/product_table.html', context)
            except ValueError:
                return render(request, "back/product_table.html", {"message":"please, select the country."})
        else:
            variants = [variant for variant in Product.objects.all().order_by('-id') if variant.price_englishelm]
            variants = set_pagination(request, variants)
            context = {
               'variants':variants,
               }
            return render(request, "back/product_table.html", context)
        

@login_required(login_url='/')
def home(request):
    """
    Render the home page view.

    This view requires authentication, redirecting to the '/' URL if the user is not logged in.

    The view retrieves a list of product variants, orders them by descending ID, filters out variants without an 'price_englishelm' value,
    paginates the results using the set_pagination function, and renders the 'back/home.html' template with the paginated variants.

    Args:
        request: The HTTP request object.

    Returns:
        The rendered 'back/home.html' template with the paginated variants in the context.

    Note:
        - This view assumes the use of Django's render function to render templates.
        - The view assumes the existence of a 'Product' model with the necessary fields.
        - The 'set_pagination' function is used to perform pagination for the product variants.
        - The 'back/home.html' template is expected to exist and contain the necessary markup for displaying the product variants.
    """

    # eng_elm = EnglisemProduct.objects.all()
    # liva_room = Product.objects.all()

    # matching_skus = EnglisemProduct.objects.values_list('sku', flat=True)

    # updated_matching_skus = []
    # for sku in matching_skus:
    #     if "-" in sku:
    #         split_sku = sku.split("-")[0]
    #         updated_matching_skus.append(split_sku)
    #     else:
    #         updated_matching_skus.append(sku)

    # print(updated_matching_skus)

    # matching_products = Product.objects.filter(Q(sku__in=matching_skus))

    variants = [variant for variant in Product.objects.all().order_by('-id') if variant.price_englishelm]
    # variants = Product.objects.all().order_by('-id')
    variants = set_pagination(request, variants)
    context = {
               'variants':variants,
               }
    return render(request, 'back/home.html', context)