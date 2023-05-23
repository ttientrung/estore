from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'cart'
urlpatterns = [
    path('cart/', views.cart, name= 'cart'),
    path('mua_ngay/<int:product_id>', views.mua_ngay, name= 'mua_ngay'),
    path('xoa_san_pham/<int:product_id>', views.xoa_san_pham, name= 'xoa_san_pham'),
    path('thanh_toan/', views.thanh_toan, name= 'thanh_toan'),
    path('add2cart/', views.add2cart, name= 'add2cart'),
]