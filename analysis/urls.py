from django.contrib import admin
from django.urls import path, re_path, include
from . import views

app_name = 'analysis'
urlpatterns = [
    path('analysis', views.analysis, name= 'analysis'),
    path('chart', views.chart, name= 'chart'),
]