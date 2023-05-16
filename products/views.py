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

def update_view(request):
    if request.method == 'POST':
        optimize_price = request.POST.get('optimize_price')
        # Update the value in the database or perform any other operations
        API_KEY = "2b4e323d3129443363269802ebca49df"
        API_SECRET_KEY = '60d668593ffa6e9a65d3e02301c37d0d'
        API_ACCESS_TOKEN = "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"
        api_version = "2023-01"  # Set your desired API version

        SHOP_NAME = 'livaroom'

        shop_url = f"https://{API_KEY}:{API_ACCESS_TOKEN}@{SHOP_NAME}.myshopify.com/admin/api/2023-01"
        shopify.ShopifyResource.set_site(shop_url)
        shop = shopify.Shop.current()
        #now i want to update the prices of each prodcuts
        variant_sku = 'AR-9511	'

        # Find the product variant based on SKU
        # variant = shopify.Variant.find_one(sku=variant_sku)

        product = shopify.Product(dict(id=8116163510579))
        variant = shopify.Variant(dict(id=44402183471411, price=114999))
        # product.add_variant(variant)
        # product.save()

        if variant:
            print(variant)
            # for i in variant:
                # print(i.sku)
            # print(variant)
            # Update the price of the variant
            # variant.price = 'new_price'  # Replace 'new_price' with the desired price
            # variant.save()
            
            messages.success(request, 'Price updated successfully for SKU: {}'.format(variant_sku))
            return JsonResponse({'success': True, 'message': 'Price updated successfully.'})
        else:
            messages.error(request, 'Variant with SKU {} not found.'.format(variant_sku))
            return JsonResponse({'success': False, 'message': 'Variant not found.'})
        

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
    # variants = [variant for variant in Variant.objects.all().order_by('-id') if variant.price_livaroom]
    variants = Product.objects.all().order_by('-id')
    variants = set_pagination(request, variants)
    context = {
               'variants':variants,
               }
    return render(request, 'back/home.html', context)