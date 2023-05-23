from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from store.models import Product
from customer.models import Customer
from .models import Order, OrderItem
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from datetime import datetime
from django.views.decorators.http import require_POST

# Create your views here.
def cart(request):
    cart = Cart(request)
    # Update cart
    if request.POST.get('btnUpDateCart'):
        cart_new = {}
        for c in cart:
            quantity_new = int(request.POST.get('quantity2' + str(c['product'].pk)))
            if quantity_new > 0:
                product_cart = {
                    str(c['product'].pk): {'quantity': quantity_new, 'price': str(c['price']), 'coupon': str(c['coupon'])}
                }
                cart_new.update(product_cart)
                # update new quantity
                c['quantity'] = quantity_new
            else:
                cart.remove(c['product'])
        else:
            request.session['cart'] = cart_new

    # print(request.session.get('cart'))
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)

@require_POST
def mua_ngay(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.POST.get('btnMuaNgay' + str(product_id)):
        quantity = int(request.POST.get('quantity' + str(product_id)))
        cart.add(product, quantity)
    return redirect('cart:cart')

@require_POST
def add2cart(request, product_id, quantity):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity)

@require_POST
def xoa_san_pham(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart')

def thanh_toan(request):
    cart = Cart(request)
    if len(cart) < 1:
        return redirect('cart:cart')
    
    ds_ma_giam_gia = [{'TTTH': 0.8}, {'LNT': 0.9}]
    ma_giam_gia = ''
    if request.POST.get('btnMaGiamGia'):
        ma_giam_gia = request.POST.get('ma_giam_gia').strip()
        giam_gia = 1
        for dict_ma_giam_gia in ds_ma_giam_gia:
            if ma_giam_gia in dict_ma_giam_gia:
                giam_gia = dict_ma_giam_gia[ma_giam_gia]
            cart_new = {}
            for c in cart:
                product_cart = {
                    str(c['product'].pk): {'quantity': c['quantity'], 'price': str(c['price']), 'coupon': str(giam_gia)}
                }
                cart_new.update(product_cart)
                # update new quantity
                c['coupon'] = giam_gia
            else:
                request.session['cart'] = cart_new
    # Đặt hàng lưu thông tin đơn hàng vào cơ sở dữ liệu
    if request.POST.get('btnDatHang'):
        khach_hang = Customer.objects.get(pk=request.session.get('s_customer')['id'])
        order = Order()
        order.customer = khach_hang
        order.total = cart.get_final_total_price()
        order.save()

        for c in cart:
            OrderItem.objects.create(order=order, product= c['product'], price=c['price'], quantity=c['quantity'], discount=c['price']*c['quantity']*(1 - c['coupon']), total_price=c['total_price'])
        
        today = datetime.now()
        subject = f'[{today.strftime("%Y%m%d%H%M%S")}] Xác nhận đặt hàng thành công'
        # message = 'Cảm ơn bạn đã đặt hàng'
        sender = settings.EMAIL_HOST_USER
        receiver_list = [khach_hang.email]

        message = '<p>Các mặt hàng đã đặt: </p>'
        message += '<ul>'
        for c in cart:
            message += f'<li>{c["product"]}</li>'
        message += '</li>'    

        msg = EmailMessage(subject, message, sender, receiver_list)
        msg.content_subtype = 'html'
        msg.send()

        # send_mail(
        #     subject,
        #     message,
        #     sender,
        #     receiver_list,
        #     fail_silently=False,
        # )
        
        # Xóa tất cả các sản phẩm ra khỏi giỏ hàng
        cart.clear()
        context = {'cart': cart}
        return render(request, 'cart/result.html', context)

    context = {'cart': cart, 'ma_giam_gia': ma_giam_gia}
    return render(request, 'store/checkout.html', context)