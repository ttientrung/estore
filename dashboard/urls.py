from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'dashboard'
urlpatterns = [
    path('dashboard/', views.dashboard_with_pivot, name= 'dashboard'),
    path('pivot-data/', views.pivot_data, name= 'pivot_data'),
]

