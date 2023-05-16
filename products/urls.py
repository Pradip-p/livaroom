from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboard'),
    # path('<int:pk>/', views.news_detail, name='news_detail'),  # Front News Details Page
    path('update/', views.update_view, name='update_view'),
    ####data visualization
    path('panel/', views.home, name='home'),
    path('search-product/', views.search_product, name="search-product")
    # path('bar-chart/', views.bar_chart, name='bar-chart'),
]