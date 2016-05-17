# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class MasterImportUpload(models.Model):
    file_name = models.CharField(max_length=500)
    ref_text = models.CharField(max_length=500, null=True, blank=True)
    process_name = models.CharField(max_length=300)
    process_type = models.CharField(max_length=50)
    uploaded_on = models.DateTimeField(null=True, blank=True)
    applied_on = models.DateTimeField(null=True, blank=True)
    query = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    applied = models.BooleanField(default=False, verbose_name="Applied on Testing")
    applied_on_production = models.BooleanField(default=False)
    applied_on_production_time = models.DateTimeField(null=True, blank=True)
    discarded_on = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User)
    file_path = models.FileField(null=True, blank=True, upload_to='/static/uploads')
    download_query = models.TextField(null=True, blank=True)
    sql_error = models.TextField(null=True, blank=True, default='[]')
    sync_query = models.TextField(null=True, blank=True, verbose_name="Sync Sql Query (Production)")
    sync_errors = models.TextField(null=True, blank=True, default='[]')
    master_category_id = models.IntegerField(null=True, blank=True)

class AdminFunctions(models.Model):
    title = models.CharField(max_length=255)
    action_name = models.CharField(max_length=255, blank=True)
    controller_name = models.CharField(max_length=255, blank=True)
    parent_id = models.IntegerField()
    is_menu = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin_functions'

class AdminUser(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    status = models.IntegerField()
    auth_key = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField()
    last_login = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'admin_user'

class Attribute(models.Model):
    attribute_id = models.IntegerField()
    attribute_type = models.CharField(max_length=45, blank=True)
    attribute_code = models.CharField(max_length=45, blank=True)
    attribute_name = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    is_searchable = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'attribute'

class Banners(models.Model):
    cat_id = models.IntegerField()
    type = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    status = models.IntegerField()
    link = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'banners'

class CartValue(models.Model):
    session_id = models.CharField(max_length=50)
    user_id = models.IntegerField()
    product_id = models.IntegerField(blank=True, null=True)
    store_price = models.DecimalField(max_digits=20, decimal_places=0, blank=True, null=True)
    store_offer_price = models.DecimalField(max_digits=20, decimal_places=0)
    product_qty = models.IntegerField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=50, decimal_places=0)
    added_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'cart_value'

class CatSolrBackLog(models.Model):
    category_id = models.IntegerField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cat_solr_back_log'

class Category2(models.Model):
    category_id = models.IntegerField(primary_key=True)
    spli_category_id = models.IntegerField()
    category_name = models.CharField(max_length=255)
    parent_category_id = models.IntegerField()
    level = models.IntegerField()
    path = models.CharField(max_length=255)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    is_mega_category = models.IntegerField()
    category_shipping_charge = models.IntegerField()
    status = models.IntegerField()
    cat_tax_per = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'category2'

class CategoryShippingCharge(models.Model):
    cat_id = models.IntegerField()
    price = models.IntegerField()
    shipping_charge = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'category_shipping_charge'

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'

class FilterProductMapping(models.Model):
    product_id = models.IntegerField()
    filter = models.ForeignKey('Filters')
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'filter_product_mapping'

class Filters(models.Model):
    subcategory_id = models.IntegerField()
    name = models.CharField(max_length=255)
    list_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'filters'

class FinalTable(models.Model):
    orderid = models.CharField(max_length=50)
    subscribed_product_id = models.IntegerField()
    product_title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=4)
    discount = models.IntegerField()
    coupon = models.CharField(max_length=50)
    checkout_price = models.DecimalField(max_digits=12, decimal_places=4)
    storefront = models.CharField(max_length=255)
    store = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_phone = models.IntegerField()
    user_address = models.CharField(max_length=255)
    user_pincode = models.IntegerField()
    timestamp = models.DateTimeField()
    total_discount = models.FloatField()
    total_payable_amount = models.FloatField()
    total_paid_amount = models.FloatField()
    payment_method = models.CharField(max_length=15)
    sub_total = models.FloatField()
    coupon_text = models.CharField(max_length=512)
    qty = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'final_table'

class Logging(models.Model):
    log_id = models.IntegerField()
    user_id = models.CharField(max_length=255)
    entity = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    data = models.TextField()
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logging'

class Media(models.Model):
    media_id = models.IntegerField(primary_key=True)
    media_url = models.CharField(max_length=255, blank=True)
    thumb_url = models.CharField(max_length=255, blank=True)
    media_type = models.CharField(max_length=45, blank=True)
    base_product_id = models.IntegerField()
    variant_id = models.IntegerField()
    is_default = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'media'

class Mycart(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.CharField(max_length=55, blank=True)
    cart_data = models.CharField(max_length=1111)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    ip_address = models.CharField(max_length=255)
    thumb_url = models.TextField(blank=True)
    vat = models.IntegerField(blank=True, null=True)
    moq = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=500, blank=True)

    class Meta:
        managed = False
        db_table = 'mycart'

class Newsletter(models.Model):
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'newsletter'

class NewsletterSubEmailid(models.Model):
    email = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    status = models.IntegerField()
    ip = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'newsletter_sub_emailid'

class OrderInvoice(models.Model):
    order_number = models.CharField(max_length=255)
    invoicenumber = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_invoice'

class RegionMaster(models.Model):
    name = models.CharField(max_length=200, blank=True)
    publish = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'region_master'

class PincodeMaster(models.Model):
    state = models.CharField(max_length=200, blank=True)
    pincode = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    publish = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pincode_master'

class Pincodes(models.Model):
    pincode = models.CharField(max_length=25)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'pincodes'

class Responsibilities(models.Model):
    user_id = models.IntegerField()
    admin_func_id = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'responsibilities'

class Sessions(models.Model):
    expire = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'sessions'

class SolrBackLog(models.Model):
    subscribed_product_id = models.IntegerField()
    is_deleted = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'solr_back_log'

class SyncLog(models.Model):
    last_sync_date = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sync_log'

class TaxMaster(models.Model):
    category_id = models.IntegerField()
    getit_category_id = models.IntegerField()
    category_name = models.CharField(max_length=255)
    parent_category_id = models.IntegerField()
    level = models.IntegerField()
    path = models.CharField(max_length=255)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    is_mega_category = models.IntegerField()
    category_shipping_charge = models.IntegerField()
    status = models.IntegerField()
    cat_tax_per = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'tax_master'

class TempProductList(models.Model):
    name = models.TextField(blank=True)
    pro_name = models.CharField(max_length=255, blank=True)
    store_id = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_product_list'
