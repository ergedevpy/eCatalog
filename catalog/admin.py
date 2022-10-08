from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class MerchantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug', 'site', 'logo_url']
    search_fields = ['name']
    save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug', 'parent_cat', ]
    search_fields = ['name']
    save_on_top = True


class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'slug', 'site', ]
    search_fields = ['name']
    save_on_top = True


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'category', 'vendor', 'name',  'stock', 'get_photo', 'oldprice', 'price',
                    'merchant', ]
    search_fields = ['name', 'description', ]
    # list_filter = ['category', 'name', 'vendor', ]
    readonly_fields = ['get_photo', ]
    save_on_top = True

    def get_photo(self, obj):
        if obj.picture:
            return mark_safe(f'<img src="{obj.picture}" width="64">')
        return "-"

    get_photo.short_description = "Picture"


admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
