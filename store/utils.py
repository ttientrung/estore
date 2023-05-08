from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate(request, products, result):
    page = request.GET.get('page')
    paginator = Paginator(products, result)

    try:
        products_pager = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        products_pager = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        products_pager = paginator.page(page)

    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1

    righIndex = (int(page) + 3)
    if righIndex > paginator.num_pages:
        righIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, righIndex)
    return products_pager, custom_range