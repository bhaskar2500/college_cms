from django.contrib import admin
from Brands.models import *

class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'store_front_id',
        'store_front_name',
        'redirect_url',
        'created_date'
    )
    search_fields = ('store_front_name', 'redirect_url', 'store_front_id')
    fields = ('store_front_name',)
admin.site.register(Brand, BrandAdmin)
