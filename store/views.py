from django.shortcuts import render, redirect, reverse
from django.conf import settings
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import FormContact
from django.db.models import Q
from .utils import *
from cart.cart import Cart
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer
from urllib.parse import urlencode
from django.conf import settings
import feedparser
from cart.views import add2cart
import pandas as pd
import os
import re

# Create your views here.
brands = Brand.objects.all()
products_per_page = 9

def index(request):
    cart = Cart(request)
    slider = Slider.objects.all()
    family_product = SubCategory.objects.filter(category_id = 1).values('id')
    family_product = Product.objects.filter(subcategory_id__in = family_product).order_by('-public_day')
    kitchen_product = SubCategory.objects.filter(category_id = 2).values('id')
    kitchen_product = Product.objects.filter(subcategory_id__in = kitchen_product).order_by('-public_day')
    context = {'slider': slider, 'brands': brands, 'family_product': family_product[:20],
               'kitchen_product': kitchen_product[:20], 'cart': cart}
    return render(request, 'store/index.html', context)

def test(request):
    slider = Slider.objects.all()
    family_product = SubCategory.objects.filter(category_id = 1).values('id')
    family_product = Product.objects.filter(subcategory_id__in = family_product).order_by('-public_day')
    kitchen_product = SubCategory.objects.filter(category_id = 2).values('id')
    kitchen_product = Product.objects.filter(subcategory_id__in = kitchen_product).order_by('-public_day')
    context = {'slider': slider, 'brands': brands, 'family_product': family_product[:20], 'kitchen_product': kitchen_product[:20]}
    response = render(request, 'store/index.html', context)

    count = 0
    if request.COOKIES.get('access_count'):
        count = int(request.COOKIES.get('access_count'))

    if count == 10:
        response.delete_cookie('access_count')

    response.set_cookie('access_count', count + 1)

    return response

def products(request, pk):
    cart = Cart(request)
    subcategories = SubCategory.objects.all().order_by('name')
    if pk == 0:
        products = Product.objects.all().order_by("-public_day")
        subcategory = f'Tất cả sản phẩm {len(products)}'
    else:
        products = Product.objects.filter(subcategory_id = pk).order_by('name')
        subcategory = SubCategory.objects.get(pk=pk)

    price_range = ''
    search_query= ''
    if request.GET.get('price'):
        price_range, search_query, products, subcategory = filter_by_price(request, pk)
    products_pager, custom_range = paginate(request, products, products_per_page)

    context = {'products': products, 'subcategories': subcategories, 'subcategory': subcategory,
               'products_pager': products_pager, 'custom_range': custom_range, 'brands': brands,
               'cart': cart, 'price_range': price_range, 'search_query': search_query}
    return render(request, 'store/product-list.html', context)

def product(request, pk):
    
    # Update viewed
    product = Product.objects.get(pk=pk)
    product.viewed += 1
    product.save()

    # Add to cart
    quantity = 1
    if request.POST.get('btnAdd2Cart'):
        quantity = int(request.POST.get('quantity'))
        add2cart(request, pk, quantity)

    cart = Cart(request)

    # Relate product
    relate_products = Product.objects.filter(subcategory_id = product.subcategory_id).exclude(pk=pk).order_by('-public_day')[:20]
    subcategories = SubCategory.objects.all().order_by('name')

    # Hiển thị sản phẩm thường được mua kèm
    rules = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'store\\analysis\\rules.csv'), index_col=0)
    lst = rules.values.tolist()
    list_rules = []
    for item in lst:
        if str(pk) in re.findall(r'\d+[, \d+]*', item[0])[0].split(','):
            list_rules = re.findall(r'\d+[, \d+]*', item[1])[0].split(',')
    recommended_products = []
    for i in list_rules:
        recommended_products.append(Product.objects.get(pk=int(i)))

    context = {'product': product, 'relate_products': relate_products,
               'subcategories': subcategories, 'cart': cart, 'brands': brands,
               'quantity': quantity, 'recommended_products': recommended_products}
    return render(request, 'store/product-detail.html', context)

def contact(request):
    cart = Cart(request)
    form = FormContact()
    if request.method == "POST":
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.phone_number = form.cleaned_data['phone_number']
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()
            return redirect('store:contact')
    else:
        form = FormContact()
    context = {'form': form, 'cart': cart}
    return render(request, 'store/contact.html', context)

def search(request):
    cart = Cart(request)
    search_query = ""
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query').strip()
    search_result = search_func(search_query)
    if request.GET.get('price'):
        price_range = request.GET.get('price')
        search_query = request.GET.get('search_query').strip()
        base_url = reverse('store:category', kwargs={'pk': 0})
        query_string = urlencode({'price': price_range, 'search_query': search_query})
        url = f'{base_url}?{query_string}'
        return redirect(url)

    total = len(search_result)
    search_result, custom_range = paginate(request, search_result, products_per_page)
    subcategories = SubCategory.objects.all().order_by('name')
    context = {'search_result': search_result, 'search_query': search_query, 'subcategories': subcategories,
               'custom_range': custom_range, 'total': total, 'brands': brands, 'cart': cart}
    return render(request, 'store/search-result.html', context)

def rss(request):
    cart = Cart(request)
    newfeed = feedparser.parse("http://feeds.feedburner.com/bedtimeshortstories/LYCF")
    entries = newfeed.entries
    '''
    dict_keys(['title', 'title_detail', 'links', 'link', 'authors', 'author', 'author_detail', 'published', 'published_parsed', 'tags', 'id', 'guidislink', 'summary', 'summary_detail', 'content'])
    '''
    for entry in entries:
        print(entry['title'])
    context = {'cart' : cart}
    return render(request, 'store/contact.html', context)

# REST API cách 1: Websevice trực tiếp
def products_service(request):
    products = Product.objects.all()
    list_products = list(products.values('name', 'price', 'image'))
    return JsonResponse(list_products, safe=False)


# REST API cách 2: Websevice django rest framework
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-public_day')
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
