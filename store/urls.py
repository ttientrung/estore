from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name= 'index'),
    path('test', views.test, name= 'test'),
    path('category/<int:pk>/', views.products, name='category'),
    path('product/<int:pk>/', views.product, name= 'product'),
    path('contact/', views.contact, name= 'contact'),
    path('search-result/', views.search, name= 'search_result'),
    path('rss/', views.rss, name= 'rss'),
    path('products-service/', views.products_service, name= 'products-service'),
]