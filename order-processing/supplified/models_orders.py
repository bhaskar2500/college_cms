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

class CompanyInfo(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500, blank=True)
    website = models.CharField(max_length=200, blank=True)
    tin = models.CharField(max_length=100, blank=True)
    pan = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'company_info'

class Contact(models.Model):
    icontactid = models.IntegerField(db_column='iContactId', primary_key=True)  # Field name made lowercase.
    vcontname = models.CharField(db_column='vContName', max_length=255)  # Field name made lowercase.
    vcontemail = models.CharField(db_column='vContEmail', max_length=100)  # Field name made lowercase.
    vcontmob = models.CharField(db_column='vContMob', max_length=20)  # Field name made lowercase.
    vcontmess = models.TextField(db_column='vContMess')  # Field name made lowercase.
    adate = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'

class CouponUserMapping(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.CharField(max_length=55, blank=True)
    code = models.CharField(max_length=20, blank=True)
    coupon_id = models.IntegerField(blank=True, null=True)
    applied_on = models.DateTimeField()
    discount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupon_user_mapping'

class Dberror(models.Model):
    error_id = models.BigIntegerField(primary_key=True)
    error_code = models.CharField(max_length=255, blank=True)
    error_message = models.CharField(max_length=255, blank=True)
    error_query = models.TextField(blank=True)
    error_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dberror'

class Login(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    login_via_google = models.CharField(max_length=1)
    google_id = models.CharField(max_length=255, blank=True)
    login_via_facebook = models.CharField(max_length=1)
    facebook_id = models.CharField(max_length=255, blank=True)
    registered_at = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    usertype = models.CharField(max_length=50)
    company = models.CharField(max_length=255)
    vcode = models.CharField(db_column='vCode', max_length=50)  # Field name made lowercase.
    ustatus = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'login'

    def __unicode__(self):
        return self.name

class LoginVerify(models.Model):
    phone = models.CharField(max_length=50)
    vcode = models.CharField(max_length=50)
    adate = models.DateTimeField(db_column='aDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_verify'

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
    base_product_id = models.IntegerField()
    variant_id = models.IntegerField()
    product_qty = models.IntegerField()
    unit_price = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    ip_address = models.CharField(max_length=255)
    title = models.CharField(max_length=500, blank=True)
    vat = models.CharField(max_length=15, blank=True)
    thumb_url = models.TextField(blank=True)
    moq = models.IntegerField(blank=True, null=True)

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

class OrderHeader(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_number = models.CharField(max_length=255)
    user = models.ForeignKey(Login)
    created_date = models.DateTimeField(blank=True, null=True)
    payment_method = models.CharField(max_length=16, blank=True)
    payment_status = models.CharField(max_length=12, blank=True)
    billing_name = models.CharField(max_length=255, blank=True)
    billing_phone = models.CharField(max_length=15, blank=True)
    billing_email = models.CharField(max_length=256, blank=True)
    billing_address = models.TextField(blank=True)
    billing_state = models.CharField(max_length=100, blank=True)
    billing_city = models.CharField(max_length=100, blank=True)
    billing_pincode = models.CharField(max_length=11, blank=True)
    shipping_name = models.CharField(max_length=256, blank=True)
    shipping_phone = models.CharField(max_length=15, blank=True)
    shipping_email = models.CharField(max_length=256, blank=True)
    shipping_address = models.TextField(blank=True)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_pincode = models.CharField(max_length=11, blank=True)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_payable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coupon_code = models.CharField(max_length=20, blank=True)
    payment_ref_id = models.CharField(max_length=30, blank=True)
    payment_gateway_name = models.CharField(max_length=100, blank=True)
    payment_type = models.CharField(max_length=100, blank=True)
    payment_source = models.CharField(max_length=15, blank=True)
    order_source = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    bank_transaction_id = models.CharField(max_length=50, blank=True)
    transaction_time = models.DateTimeField(blank=True, null=True)
    payment_mod = models.CharField(max_length=50, blank=True)
    bankname = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=9, blank=True)
    cron_processed_flag = models.CharField(max_length=1, blank=True)
    source_url = models.TextField(blank=True)
    source_type = models.CharField(max_length=100, blank=True)
    source_id = models.IntegerField(blank=True, null=True)
    source_name = models.CharField(max_length=254, blank=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    buyer_shipping_cost = models.IntegerField(blank=True, null=True)
    order_type = models.CharField(max_length=150, blank=True)
    utm_source = models.CharField(max_length=255, blank=True)
    coupon_discount = models.IntegerField(blank=True, null=True)
    coupon_is_valid = models.CharField(max_length=20, blank=True)
    user_phone_no = models.CharField(max_length=15, blank=True)
    user_email = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'order_header'

class OrderInvoice(models.Model):
    order_number = models.CharField(max_length=255)
    invoicenumber = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_invoice'

class OrderLine(models.Model):
    order_id = models.IntegerField()
    subscribed_product_id = models.IntegerField()
    base_product_id = models.IntegerField()
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=150, blank=True)
    store_email = models.CharField(max_length=150, blank=True)
    store_front_id = models.IntegerField(blank=True, null=True)
    store_front_name = models.CharField(max_length=250, blank=True)
    seller_name = models.CharField(max_length=150, blank=True)
    seller_phone = models.CharField(max_length=150, blank=True)
    seller_address = models.TextField(blank=True)
    seller_state = models.CharField(max_length=150, blank=True)
    seller_city = models.CharField(max_length=150, blank=True)
    colour = models.CharField(max_length=30, blank=True)
    size = models.CharField(max_length=10, blank=True)
    product_name = models.CharField(max_length=256, blank=True)
    product_qty = models.IntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    shipping_charges = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=24)
    delivery_request_id = models.CharField(max_length=255)
    delivery_tracking_number = models.CharField(max_length=255)
    product_title = models.CharField(max_length=500, blank=True)
    vatrate = models.CharField(max_length=10, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_vat = models.CharField(max_length=20, blank=True)

    class Meta:
        managed = False
        db_table = 'order_line'

class OrderLogs(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    inputs = models.TextField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_logs'

class PgTransactions(models.Model):
    order_id = models.IntegerField()
    order_no = models.CharField(max_length=50, blank=True)
    pg_request = models.TextField(blank=True)
    pg_response = models.TextField(blank=True)
    status = models.CharField(max_length=50, blank=True)
    reason = models.CharField(max_length=250, blank=True)
    added_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'pg_transactions'

class Pincodes(models.Model):
    pincode = models.CharField(max_length=25)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'pincodes'

class ProductAttributeMapping(models.Model):
    base_product_id = models.IntegerField()
    attribute_id = models.IntegerField()
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'product_attribute_mapping'

class ProductCategoryMapping(models.Model):
    base_product_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_category_mapping'

class ProductFrontendMapping(models.Model):
    subscribed_product_id = models.IntegerField()
    store_front_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_frontend_mapping'

class ProductTaxMasterMapping(models.Model):
    base_product_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_tax_master_mapping'

class Promocode(models.Model):
    code = models.CharField(max_length=20, blank=True)
    min_cart_total = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    expiry_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'promocode'

class Responsibilities(models.Model):
    user_id = models.IntegerField()
    admin_func_id = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'responsibilities'

class Reviews(models.Model):
    name = models.CharField(max_length=100, blank=True)
    title_of_review = models.TextField(blank=True)
    review = models.TextField()
    status = models.IntegerField()
    ip_address = models.TextField(blank=True)
    submited_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'

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

class Store(models.Model):
    store_id = models.IntegerField(primary_key=True)
    store_code = models.CharField(max_length=255, blank=True)
    store_name = models.CharField(max_length=255, blank=True)
    store_details = models.TextField(blank=True)
    store_logo = models.CharField(max_length=255, blank=True)
    seller_name = models.CharField(max_length=255, blank=True)
    business_address = models.CharField(max_length=300, blank=True)
    business_address_country = models.CharField(max_length=100, blank=True)
    business_address_state = models.CharField(max_length=100, blank=True)
    business_address_city = models.CharField(max_length=100, blank=True)
    business_address_pincode = models.CharField(max_length=100, blank=True)
    mobile_numbers = models.CharField(max_length=100, blank=True)
    telephone_numbers = models.CharField(max_length=100, blank=True)
    visible = models.IntegerField()
    meta_title = models.CharField(max_length=150, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)
    customer_value = models.DecimalField(max_digits=12, decimal_places=4)
    chat_id = models.CharField(max_length=45, blank=True)
    email = models.CharField(max_length=255, blank=True)
    tin = models.CharField(max_length=255, blank=True)
    pan = models.CharField(max_length=255, blank=True)
    contact_persion_name = models.CharField(max_length=255, blank=True)
    con_per_mobile = models.CharField(max_length=255, blank=True)
    con_per_email = models.CharField(max_length=255, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    ac_number = models.CharField(max_length=255, blank=True)
    branch_code = models.CharField(max_length=255, blank=True)
    ifsc_code = models.CharField(max_length=255, blank=True)
    rtgs_code = models.CharField(max_length=255, blank=True)
    status = models.IntegerField()
    vtiger_status = models.IntegerField()
    vtiger_accountid = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    tagline = models.CharField(max_length=256, blank=True)
    is_tagline = models.IntegerField()
    store_api_key = models.CharField(max_length=100)
    store_api_password = models.CharField(max_length=100)
    redirect_url = models.TextField(blank=True)
    seller_mailer_flag = models.IntegerField()
    buyer_mailer_flag = models.IntegerField()
    channel_name = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
    order_prefix = models.CharField(max_length=11)
    is_active_valid = models.IntegerField()
    store_shipping_charge = models.IntegerField()
    store_tax_per = models.FloatField()

    class Meta:
        managed = False
        db_table = 'store'

class StoreFront(models.Model):
    store_front_id = models.IntegerField()
    store_front_name = models.CharField(max_length=255, blank=True)
    store_front_api_key = models.CharField(max_length=100, blank=True)
    store_front_api_password = models.CharField(max_length=100, blank=True)
    store_front_api_token = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField()
    parent_id = models.IntegerField()
    tagline = models.CharField(max_length=255)
    is_tagline = models.IntegerField()
    redirect_url = models.TextField(blank=True)
    seller_mailer_flag = models.IntegerField()
    buyer_mailer_flag = models.IntegerField()
    vendor_coupon_prefix = models.CharField(max_length=10)
    order_prefix = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'store_front'

class StoreShippingCharge(models.Model):
    store_id = models.IntegerField()
    price = models.IntegerField()
    shipping_charge = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'store_shipping_charge'

class StorefrontFbpageMapping(models.Model):
    store_front_id = models.IntegerField()
    page_id = models.CharField(max_length=40)
    page_name = models.CharField(max_length=255, blank=True)
    access_token = models.TextField(blank=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modify_on = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'storefront_fbpage_mapping'

class SubscribedProduct(models.Model):
    subscribed_product_id = models.IntegerField(primary_key=True)
    base_product_id = models.IntegerField()
    store_id = models.IntegerField()
    unit_rate = models.DecimalField(max_digits=12, decimal_places=4)
    store_price = models.DecimalField(max_digits=12, decimal_places=4)
    secondary_store_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    store_offer_price = models.DecimalField(max_digits=12, decimal_places=4)
    weight = models.CharField(max_length=100, blank=True)
    length = models.CharField(max_length=100, blank=True)
    width = models.CharField(max_length=100, blank=True)
    height = models.CharField(max_length=100, blank=True)
    warranty = models.CharField(max_length=100, blank=True)
    prompt = models.IntegerField(blank=True, null=True)
    prompt_key = models.CharField(max_length=100, blank=True)
    status = models.IntegerField()
    checkout_url = models.CharField(max_length=2083, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField()
    is_deleted = models.IntegerField()
    sku = models.CharField(max_length=128)
    quantity = models.IntegerField()
    is_cod = models.IntegerField()
    subscribe_shipping_charge = models.IntegerField()
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=255)
    variant_on = models.CharField(max_length=100)
    views = models.IntegerField(blank=True, null=True)
    totorders = models.IntegerField(blank=True, null=True)
    moq = models.IntegerField(blank=True, null=True)
    vat = models.IntegerField(blank=True, null=True)
    thumb_url = models.TextField(blank=True)
    title = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 'subscribed_product'

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

class UserAddress(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True)
    phone_no = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    landmark = models.CharField(max_length=500, blank=True)
    state = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=200, blank=True)

    class Meta:
        managed = False
        db_table = 'user_address'
