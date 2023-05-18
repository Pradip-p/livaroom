from django.shortcuts import render, redirect
from .models import  Variant, Product
from .pagination import set_pagination
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
import shopify
from shopify import PaginatedIterator

# Create your views here.
from django.http import FileResponse
from django.urls import reverse
from django.utils.encoding import smart_str
import os
from django.http import FileResponse
from django.utils.encoding import smart_str
from pathlib import Path

def download_export_csv(request):
    file_path = Path(__file__).resolve().parent.parent.parent / 'data' / 'export.csv'

    with open(file_path, 'r') as file:
        file_content = file.read()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    response.write(smart_str(file_content))

    return response


# def download_export_csv(request):
#     # Assuming the "export.csv" file is located in the base directory of your Django project
#     file_path = 'export.csv'
#      # Assuming the "export.csv" file is located in the "data" folder outside the Django project
#     # file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'export.csv')
#     # file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__)),'data/export.csv'))
#     file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'export.csv')
#     # Open the file in binary mode
#     file = open(file_path, 'rb')
#     # Read the file content
#     file_content = file.read()
#     # Close the file
#     file.close()

#     # Create a FileResponse object with the file content
#     response = FileResponse(file_content)
#     # Set the appropriate content type (CSV file)
#     response['Content-Type'] = 'text/csv'
#     # Set the Content-Disposition header to force the browser to download the file
#     response['Content-Disposition'] = 'attachment; filename="{0}"'.format(smart_str(file_path))
#     return response








@login_required(login_url='/')
def update_product_price(request):
    if request.method == "POST":
        prices = request.POST.getlist('prices[]')
        # Update the value in the database or perform any other operations
        API_KEY = "2b4e323d3129443363269802ebca49df"
        API_ACCESS_TOKEN = "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"

        SHOP_NAME = 'livaroom'

        shop_url = f"https://{API_KEY}:{API_ACCESS_TOKEN}@{SHOP_NAME}.myshopify.com/admin/api/2023-01"
        shopify.ShopifyResource.set_site(shop_url)
        shop = shopify.Shop.current()
        #now i want to update the prices of each prodcuts
        # variant_sku = 'AR-9511'
        for price in prices:
            variant_sku = 'EEI-5805-CHE-WHI-WHI'
            variant = Product.objects.get(sku=variant_sku)
            if variant:
                product_id = variant.product_id
                variant_id = variant.variant_id
                # Find the product variant based on SKU on Livaroom API(site)..
                # product = shopify.Product(dict(id=product_id))
                # variant = shopify.Variant(dict(id=variant_id, price=55.04)) #55.04
                # product.add_variant(variant) #it does not mean add new varinat it update the existing price of variant.
                # product.save()
                # messages.success(request,'Price {} updated successfully.'.format(optimize_price))
        return JsonResponse({'message': 'Price updated successfully.'}, status=200,)

    return JsonResponse({'message':'invalid request.'}, status=500)


@login_required(login_url='/')
def update_view(request):
    if request.method == 'POST':
        optimize_price = request.POST.get('optimize_price')
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
        variant = Product.objects.get(sku=variant_sku)
        if variant:
            product_id = variant.product_id
            variant_id = variant.variant_id
            # Find the product variant based on SKU on Livaroom API(site)..
            product = shopify.Product(dict(id=product_id))
            variant = shopify.Variant(dict(id=variant_id, price=55.04)) #55.04
            product.add_variant(variant) #it does not mean add new varinat it update the existing price of variant.
            product.save()
            # messages.success(request,'Price {} updated successfully.'.format(optimize_price))
            return JsonResponse({'message': 'Price {} updated successfully.'.format(optimize_price)}, status=200, safe=False)

        else:
            # messages.errors(request, 'Varint:{} Not found'.format(variant_sku))
            return JsonResponse({'success': True, 'message': 'SKU Not Found.'}, status=500)
        

@login_required(login_url='/')
def search_product(request):
    if request.method == 'GET':

        sku = request.GET.get('sku')
        if sku:
            try:
                variants = Product.objects.filter(sku__icontains=sku).distinct()
                context = {'variants':variants, 'message':'show the products based on price avaiable'}
                return render(request, 'back/product_table.html', context)
            except ValueError:
                return render(request, "back/product_table.html", {"message":"please, select the country."})
        else:
            variants = [variant for variant in Product.objects.all().order_by('-id') if variant.price_livaroom]
            variants = set_pagination(request, variants)
            context = {
               'variants':variants,
               }
            return render(request, "back/product_table.html", context)


@login_required(login_url='/')
def dashboard(request):
    variants = Product.objects.all().order_by('-id')
    for variant in variants:
        if variant.price_livaroom:
            print('')
    # variants_data = Variant.objects.exclude(price_livaroom__exact='').order_by('-id')
    # cat = Category.objects.all()
    # print(variants_data)
    variants = set_pagination(request, variants)

    return render(request, 'front/home.html',{
        'variants':variants,
        # 'cat':cat
    })

@login_required(login_url='/')
def home(request):
    # #set the pagination on products li
    variants = [variant for variant in Product.objects.all().order_by('-id') if variant.price_englishelm]
    # variants = Product.objects.all().order_by('-id')
    variants = set_pagination(request, variants)
    context = {
               'variants':variants,
               }
    return render(request, 'back/home.html', context)