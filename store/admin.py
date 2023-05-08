from django.contrib import admin
from .models import *
from datetime import datetime
from django.utils.html import format_html

def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())

change_public_day.shoer_description = 'Change public day'

class ProductAdmin(admin.ModelAdmin):
    exclude = ('public_day', 'viewed')
    list_display = ('e_name', 'e_price', 'e_public_day', 'e_viewed', 'e_subcategory', 'e_image')
    list_filter = ('public_day',)
    search_fields = ('name__icontains',)
    actions = [change_public_day]

    @admin.display(description="Tên sản phẩm")
    def e_name(self, obj):
        return f'{obj.name}'
    
    @admin.display(description="Giá thành")
    def e_price(self, obj):
        return '{:20,.2f}'.format(int(obj.price))
    
    @admin.display(description="Ngày đăng")
    def e_public_day(self, obj):
        return f'{obj.public_day.strftime("%d-%m-%Y")}'
    
    @admin.display(description="Số lượt xem")
    def e_viewed(self, obj):
        return f'{obj.viewed}'
    
    @admin.display(description="Danh mục")
    def e_subcategory(self, obj):
        return f'{obj.subcategory}'
    
    @admin.display(description="Hình ảnh")
    def e_image(self, obj):
        return format_html(f'<img src="{obj.image.url}" style="width: 45px; height: 45px;"/>')

admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Slider)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)


admin.site.site_header = 'EStore Admin'
# Register your models here.
