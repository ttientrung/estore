from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from cart.cart import Cart
from django.forms.models import model_to_dict
from cart.models import Order, OrderItem
from store.models import Product
from django.conf import settings
from customer.libs import *
import base64
import pdfkit
from django.template.loader import render_to_string

salt = '123'

# Create your views here.
def login(request):
    if 's_customer' in request.session:
        return redirect('store:index')

    # Lấy thông tin tỉnh/tp, quận/huyện, phường/xã
    du_lieu = read_json_internet('http://api.laptrinhpython.net/vietnam')

    # Tỉnh/TP
    list_provinces = []
    str_districts = []
    str_wards = []
    list_districts_2 = []
    for province in du_lieu:
        list_provinces.append(province['name'])
        # Quận/Huyện
        list_districts_1 = []
        for dictrict in province['districts']:
            d = dictrict['prefix'] + ' ' + dictrict['name']
            list_districts_1.append(d)
            list_districts_2.append(d)
            # Phường/Xã
            list_wards = []
            for ward in dictrict['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                list_wards.append(w)
            else:
                str_wards.append('|'.join(list_wards))
        else:
            str_districts.append('|'.join(list_districts_1))

    result = ""
    form = FormDangKy()
    if request.POST.get('btnRegister'):
        form = FormDangKy(request.POST, Customer)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                hasher = PBKDF2PasswordHasher()
                request.POST._mutable = True
                post = form.save(commit=False)
                post.first_name = form.cleaned_data['first_name']
                post.last_name = form.cleaned_data['last_name']
                post.email = form.cleaned_data['email']
                post.password = hasher.encode(form.cleaned_data['password'], salt)
                post.confirm_password = form.cleaned_data['confirm_password']
                post.phone = form.cleaned_data['phone']
                post.address = form.cleaned_data['address'] + ', ' + form.cleaned_data['ward'] + ', ' + form.cleaned_data['district'] + ', ' + form.cleaned_data['province']
                post.save()
                result = '''
                <div class="alert alert-success" role="alert">
                    Successful create your account!
                </div>
                '''
                # return redirect('customer:login')
            else:
                result = '''
                <div class="alert alert-danger" role="alert">
                    Please check the password!
                </div>
                '''
        else:
            result = '''
                <div class="alert alert-danger" role="alert">
                    False to create your account! Please check again!
                </div>
                '''
    else:
        form = FormDangKy()
        
    login_result = ''
    if request.POST.get('btnlogin'):

        hasher = PBKDF2PasswordHasher()

        email = request.POST.get('email')
        password = hasher.encode(request.POST.get('password'), salt)

        customer = Customer.objects.filter(email=email, password=password)
    
        if customer.count() > 0:
            dict_customer = customer.values()[0]
            request.session['s_customer'] = dict_customer
            return redirect('store:index')
        else:
            login_result = '''
                <div class="alert alert-danger" role="alert">
                    Login fail!
                </div>
                '''
    context = {'form': form, 'result': result, 'login_result': login_result,
        'provinces': tuple(list_provinces),
        'str_districts': tuple(str_districts),
        'str_wards': tuple(str_wards),
        'list_districts': list_districts_2}
    return render(request, 'store/login.html', context)

def logout(request):
    # if request.session.get('s_customer'):
    #     del request.session['s_customer']
    if 's_customer' in request.session:
        del request.session['s_customer']
    return redirect('customer:login')

def my_account(request):
    cart = Cart(request)
    result = ""
    result_change = ""
    customer = Customer.objects.get(pk=request.session.get('s_customer')['id'])
    form = UpdateForm(instance=customer)
    pass_form = PassChangeForm(instance=customer)

    if 's_customer' not in request.session:
        return redirect('customer:login')
    
    if request.POST.get('btnUpdate'):
        form = UpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            dict_customer = model_to_dict(customer)
            request.session['s_customer'] = dict_customer
            result = '''
                <div class="alert alert-success" role="alert">
                    Successful update your account!
                </div>
                '''
            # return redirect('customer:my-account')
        else:
            result = '''
                <div class="alert alert-danger" role="alert">
                    Please check your information!
                </div>
            '''
            print(form.errors.as_data())

    if request.POST.get('btnChangePass'):
        pass_form = PassChangeForm(request.POST, instance=customer)
        hasher = PBKDF2PasswordHasher()
        if pass_form.is_valid():
            if request.session.get('s_customer')['password'] == hasher.encode(request.POST.get('curr_password'), salt):
                if pass_form.cleaned_data['password'] == pass_form.cleaned_data['confirm_password']:
                    request.POST._mutable = True
                    post = pass_form.save(commit=False)
                    post.password = hasher.encode(pass_form.cleaned_data['password'], salt)
                    post.save()
                    dict_customer = model_to_dict(customer)
                    request.session['s_customer'] = dict_customer
                    result_change = '''
                        <div class="alert alert-success" role="alert">
                            Successful change your account password!
                        </div>
                        '''
                else:
                    result_change = '''
                        <div class="alert alert-danger" role="alert">
                            Password are not match!
                        </div>
                        '''
            else:
                result_change = '''
                        <div class="alert alert-danger" role="alert">
                            Wrong password!
                        </div>
                        '''
            # return redirect('customer:my-account')
        else:
            result_change = '''
                <div class="alert alert-danger" role="alert">
                    Please check your information!
                </div>
            '''
            print(form.errors.as_data())

    orders = Order.objects.filter(customer=request.session['s_customer']['id'])
    dict_orders = {}
    for order in orders:
        order_items = list(OrderItem.objects.filter(order=order.pk).values())
        for order_item in order_items:
            product = Product.objects.get(pk=order_item['product_id'])
            order_item['product_name'] = product.name
            order_item['product_image'] = product.image
            order_item['total'] = order.total
        else:
            dict_order_items = {
                order.pk: order_items
            }
            dict_orders.update(dict_order_items)
    context = {'cart': cart, 'form': form, 'result': result, 'pass_form': pass_form, 'result_change': result_change, 'dict_orders': dict_orders, 'orders': orders}
    return render(request, 'store/my-account.html', context)

def report_export(request, pk):
    if 's_customer' not in request.session:
        return redirect('customer:login')
    customer = request.session.get('s_customer')
    order = Order.objects.get(pk=pk, customer = customer['id'])
    order_items = list(OrderItem.objects.filter(order = pk).values())
    for item in order_items:
        product = Product.objects.get(pk=item['product_id'])
        item['product_name'] = product.name
        with open(settings.MEDIA_ROOT + str(product.image), 'rb') as img_file:
            image_string = base64.b64encode(img_file.read())
        item['product_image'] = image_string.decode('utf-8')
        item['total'] = order.total
    context = {'order_date': order.created.strftime('%d-%m-%Y %H:%M:%S'), 'order_items': order_items, 'customer': customer, 'pk': pk}
    # response = render(request, 'customer/report_order.html', context)
    response = render_to_string('customer/report_order.html', context)

    # export to pdf
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    filename = f'DH{order.pk}.pdf'
    folder_report = settings.MEDIA_ROOT + 'store/reports/'
    path_to_report = folder_report + filename
    pdfkit.from_string(response, path_to_report, configuration=config)
    return redirect('/media/store/reports/' + filename)