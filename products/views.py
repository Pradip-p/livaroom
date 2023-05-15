from django.shortcuts import render, redirect
from .models import  Variant, Product
from .pagination import set_pagination
from django.contrib.auth.decorators import login_required

# Create your views here.
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