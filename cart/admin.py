from django.contrib import admin
from cart.models import Order, OrderItem
from datetime import datetime
from django.utils.html import format_html


class OrdersAdmin(admin.ModelAdmin):
    exclude = ('created',)
    list_display = ('e_customer', 'e_total', 'e_status')
    list_filter = ('created',)
    search_fields = ('customer__icontains',)

    @admin.display(description="Khách hàng")
    def e_customer(self, obj):
        return f'{obj.customer}'
    
    @admin.display(description="Tổng giá trị đơn hàng")
    def e_total(self, obj):
        return '{:20,.2f}'.format(int(obj.total))
    
    @admin.display(description="Trạng thái")
    def e_status(self, obj):
        return 'Đã giao' if obj.status else 'Chưa giao'
    
def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())

change_public_day.shoer_description = 'Change public day'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('e_order', 'e_product', 'e_price', 'e_quantity', 'e_discount', 'e_total_price')
    list_filter = ('order',)
    search_fields = ('name__icontains',)

    @admin.display(description="Đơn hàng")
    def e_order(self, obj):
        return f'{obj.order}'
    
    @admin.display(description="Tên sản phẩm")
    def e_product(self, obj):
        return f'{obj.product}'
    
    @admin.display(description="Giá thành")
    def e_price(self, obj):
        return '{:20,.2f}'.format(int(obj.price))
    
    @admin.display(description="Số lượng")
    def e_quantity(self, obj):
        return f'{obj.quantity}'
    
    @admin.display(description="Giảm giá")
    def e_discount(self, obj):
        return f'{obj.discount}'
    
    @admin.display(description="Tổng giá tiền")
    def e_total_price(self, obj):
        return '{:20,.2f}'.format(int(obj.total_price))


# Register your models here.
admin.site.register(Order, OrdersAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
