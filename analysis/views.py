from django.shortcuts import render
import pandas as pd
from django.conf import settings
from .utils import *

def analysis(request):
    csv_data_likes = settings.MEDIA_ROOT + 'store/analysis/data_likes.csv'
    csv_data_views = settings.MEDIA_ROOT + 'store/analysis/data_views.csv'
    likes = pd.read_csv(csv_data_likes)
    views = pd.read_csv(csv_data_views)
    df_likes_html = likes.to_html()
    df_views_html = views.to_html()
    csv_data = settings.MEDIA_ROOT + 'store/analysis/data.csv'
    df = pd.read_csv(csv_data)
    df_html = df.to_html()
    context = {'df_likes_html': df_likes_html, 'df_views_html': df_views_html, 'df_html': df_html}
    return render(request,'analysis/series_dataframe.html', context)

def chart(request):
    csv_data_wait_time = settings.MEDIA_ROOT + 'store/analysis/dataset.xlsx'
    data_second = pd.read_excel(csv_data_wait_time, sheet_name='Wait_times')
    hist = get_hist(data_second, 'seconds', 'Customer Wait Time')
    context = {'hist': hist}
    return render(request, 'analysis/chart.html', context)
# Create your views here.
