from django.contrib import admin
from Stores.models import *
from import_export import resources
from import_export.admin import *

class StoreAdmin(admin.ModelAdmin):
    #def has_add_permission(self, request):
    #    return False

    fields =('seller_name', 'business_address', 'business_address_city', 'business_address_pincode',\
       'business_address_state', 'business_address_country', 'mobile_numbers', 'visible', 'email',\
       'tin', 'pan', 'contact_persion_name', 'con_per_mobile', 'con_per_email', 'bank_name', 'ac_number',\
       'branch_code', 'ifsc_code', 'rtgs_code', 'status', 'store_shipping_charge', 'store_tax_per')
    list_display = (
        'store_id',
        #'store_name',
        'seller_name',
        'con_per_email',
        'mobile_numbers',
        'business_address',
        'business_address_city',
        'business_address_state',
        'business_address_pincode',
    )
    search_fields = ('store_id', 'seller_name')
admin.site.register(Store,StoreAdmin)

class StoreShippingChargeAdmin(admin.ModelAdmin):
    list_display = (
        'store',
        'price',
        'shipping_charge',
    )
admin.site.register(StoreShippingCharge, StoreShippingChargeAdmin)

class StorePriceMappingResource(resources.ModelResource):
    class Meta:
        model = StorePriceMapping

class StorePriceMappingAdmin(ExportMixin, admin.ModelAdmin):
    list_display = (
	'base_product_id',
	'subscribed_product_id',
	'store_id',
	'store_price',
	'store_offer_price',
	'publish',
    )
    search_fields = ('base_product_id', 'subscribed_product_id')
    list_filter = ('store_id', 'publish')
admin.site.register(StorePriceMapping, StorePriceMappingAdmin)
