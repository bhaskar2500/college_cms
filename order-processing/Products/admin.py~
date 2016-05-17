from django.contrib import admin
from Products.models import *
from import_export import resources
from import_export.admin import *

class BaseProductResource(resources.ModelResource):
    class Meta:
        model = BaseProduct

class BaseProductAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = BaseProductResource
    list_display = (
        'base_product_id',
        'title',
        'created_date',
        'modified_date',
        'brand_id'
    )
    search_fields = ('base_product_id', 'title')
    list_filter = ('created_date', 'modified_date')
admin.site.register(BaseProduct,BaseProductAdmin)

class SubscribedProductResource(resources.ModelResource):
    class Meta:
        model = SubscribedProduct

class SubscribedProductAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
        'base_product_id',
        'subscribed_product_id',
        #'title',
        'sku',
        #'color',
        #'moq',
        #'modified_date',
        #'store',
    )
    search_fields = ('sku','subscribed_product_id', 'base_product__base_product_id')
    list_filter = ('created_date', 'modified_date')
admin.site.register(SubscribedProduct,SubscribedProductAdmin)
