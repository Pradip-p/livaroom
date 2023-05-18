from django.urls import path
from . import views

urlpatterns = [
    #this url is used for single product variant prices.
    path('update/', views.update_view, name='update_view'),
    #this url is used for update the multiple product variant prices
    path('update-product-price/', views.update_product_price, name='update_product_price'),
    #this is url of dashboard
    path('panel/', views.home, name='home'),
    #this url is used for search the variant using sku.
    path('search-product/', views.search_product, name="search-product"),
    #this url will be remove soon.
    path('download-export-csv/', views.download_export_csv, name='download_export_csv'),
]