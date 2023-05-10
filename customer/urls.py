from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'customer'
urlpatterns = [
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('my-account/', views.my_account, name= 'my-account'),
    path('reports/<int:pk>/', views.report_export, name= 'reports'),
]