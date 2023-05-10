from .models import *
from django.db.models import Q
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

def search_func(search_query):
    search_result = Product.objects.distinct().filter(
        Q(name__icontains = search_query)|
        Q(content__icontains = search_query)|
        Q(subcategory__name__icontains = search_query)
    ).order_by('-public_day')
    return search_result

def filter_by_price(request, pk):
    price_range = request.GET.get('price')
    b_price, t_price = price_range.split('-')
    search_query = request.GET.get('search_query').strip()
    '''
    __lte: less than or equal
    __gte: greater than or equal
    __lt: less than
    __gt: greater than
    '''
    if pk == 0:
        if t_price == '':
            products = Product.objects.filter(price__gt=b_price).order_by('-public_day')
            if search_query:
                products = Product.objects.distinct().filter(
                    Q(price__gt=b_price)&
                    (Q(name__icontains=search_query)|
                    Q(content__icontains = search_query)|
                    Q(subcategory__name__icontains = search_query))).order_by('-public_day')
        else:
            products = Product.objects.filter(price__lt=t_price, price__gt=b_price).order_by('-public_day')
            if search_query:
                products = Product.objects.distinct().filter(
                    (Q(price__lt=t_price)&
                    Q(price__gt=b_price))&   
                    (Q(name__icontains=search_query)|
                    Q(content__icontains = search_query)|
                    Q(subcategory__name__icontains = search_query))).order_by('-public_day')
    else:
        if t_price == '':
            products = Product.objects.filter(subcategory = pk, price__gt=b_price).order_by('-public_day')
            if search_query:
                products = Product.objects.distinct().filter(
                    (Q(subcategory = pk)&
                    Q(price__gt=b_price))&
                    (Q(name__icontains=search_query)|
                    Q(content__icontains = search_query)|
                    Q(subcategory__name__icontains = search_query))
                ).order_by('-public_day')
        else:
            products = Product.objects.filter(subcategory = pk, price__lt=t_price, price__gt=b_price).order_by('-public_day')
            if search_query:
                products = Product.objects.filter(
                    (Q(subcategory = pk)&
                    Q(price__gt=b_price)&
                    Q(price__lt=t_price))&
                    (Q(name__icontains=search_query)|
                    Q(content__icontains = search_query)|
                    Q(subcategory__name__icontains = search_query))).order_by('-public_day')
    subcategory = f'Tìm thấy {len(products)} sản phẩm với giá {price_range}'

    return price_range, search_query, products, subcategory