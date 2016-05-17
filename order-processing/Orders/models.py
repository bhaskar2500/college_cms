from __future__ import unicode_literals

from django.db import models

from Orders.configure_lines import *
from Orders.models import *
from django import forms
from django.contrib.auth.models import User


class orderstatus(models.Model):
    status=models.CharField(max_length=200,blank=True,null=True)
    status_name=models.CharField(max_length=200,blank=True,null=True)
    order_by=models.IntegerField()
    cust_sms = models.BooleanField()
    cust_email = models.BooleanField()
    temp_cust_mail=models.CharField(max_length=5000,blank=True)
    temp_seller_mail=models.CharField(max_length=5000,blank=True)
    temp_cust_sms=models.CharField(max_length=3000,blank=True)
    temp_seller_sms=models.CharField(max_length=3000,blank=True)
    seller_sms= models.BooleanField()
    seller_mail= models.BooleanField()
    class Meta:
        managed = False
        db_table = 'orderstatus'

    def __unicode__(self):
        # print self.status_name
        return str(self.status_name)
os=orderstatus.objects.using('orders').values('status','status_name')

l=[]
for v in os:
    l.append((v['status'],v['status_name']))

Order_option_choices=tuple(l) 

class CompanyInfo(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    website = models.CharField(max_length=200, blank=True, null=True)
    tin = models.CharField(max_length=100, blank=True, null=True)
    pan = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_info'


class Contact(models.Model):
    icontactid = models.AutoField(db_column='iContactId', primary_key=True)  # Field name made lowercase.
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
    session_id = models.CharField(max_length=55, blank=True, null=True)
    code = models.CharField(max_length=20, blank=True, null=True)
    coupon_id = models.IntegerField(blank=True, null=True)
    applied_on = models.DateTimeField()
    discount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupon_user_mapping'


class Dberror(models.Model):
    error_id = models.BigIntegerField(primary_key=True)
    error_code = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    error_query = models.TextField(blank=True, null=True)
    error_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dberror'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Feedback(models.Model):
    user_id = models.IntegerField()
    feedback = models.TextField()
    callback = models.CharField(max_length=255, blank=True, null=True)
    feedback_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'feedback'


class HistoryMycart(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.CharField(max_length=55, blank=True, null=True)
    cart_data = models.CharField(max_length=1111)
    base_product_id = models.IntegerField()
    variant_id = models.IntegerField()
    product_qty = models.IntegerField()
    unit_price = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    ip_address = models.CharField(max_length=255)
    title = models.CharField(max_length=500, blank=True, null=True)
    vat = models.CharField(max_length=15, blank=True, null=True)
    thumb_url = models.TextField(blank=True, null=True)
    moq = models.DecimalField(max_digits=65, decimal_places=2)
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=300, blank=True, null=True)
    deleted_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'history_mycart'


class Login(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    login_via_google = models.CharField(max_length=1)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    login_via_facebook = models.CharField(max_length=1)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    registered_at = models.DateTimeField(blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    usertype = models.CharField(max_length=50)
    company = models.CharField(max_length=255)
    vcode = models.CharField(db_column='vCode', max_length=50)  # Field name made lowercase.
    ustatus = models.CharField(max_length=50)
    auth_key = models.CharField(max_length=255, blank=True, null=True)
    is_verified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'login'


class LoginVerify(models.Model):
    phone = models.CharField(max_length=50)
    vcode = models.CharField(max_length=50)
    adate = models.DateTimeField(db_column='aDate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'login_verify'


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    media_url = models.CharField(max_length=255, blank=True, null=True)
    thumb_url = models.CharField(max_length=255, blank=True, null=True)
    media_type = models.CharField(max_length=45, blank=True, null=True)
    base_product_id = models.IntegerField()
    variant_id = models.IntegerField()
    is_default = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'media'


class Mycart(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    session_id = models.CharField(max_length=55, blank=True, null=True)
    cart_data = models.CharField(max_length=1111)
    base_product_id = models.IntegerField()
    variant_id = models.IntegerField()
    product_qty = models.IntegerField()
    unit_price = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()
    ip_address = models.CharField(max_length=255)
    title = models.CharField(max_length=500, blank=True, null=True)
    vat = models.CharField(max_length=15, blank=True, null=True)
    thumb_url = models.TextField(blank=True, null=True)
    moq = models.DecimalField(max_digits=65, decimal_places=2)
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mycart'


class Newsletter(models.Model):
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'newsletter'


class NewsletterSubEmailid(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    modified_date = models.DateTimeField()
    status = models.IntegerField()
    ip = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'newsletter_sub_emailid'


class OrderHeader(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_number = models.CharField(max_length=255)
    user_id = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    payment_method = models.CharField   (max_length=16, blank=True, null=True)
    payment_status = models.CharField(max_length=12, blank=True, null=True)
    billing_name = models.CharField(max_length=255, blank=True, null=True)
    billing_phone = models.CharField(max_length=15, blank=True, null=True)
    billing_email = models.CharField(max_length=256, blank=True, null=True)
    billing_address = models.TextField(blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_pincode = models.CharField(max_length=11, blank=True, null=True)
    shipping_name = models.CharField(max_length=256, blank=True, null=True)
    shipping_phone = models.CharField(max_length=15, blank=True, null=True)
    shipping_email = models.CharField(max_length=256, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_pincode = models.CharField(max_length=11, blank=True, null=True)
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_payable_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_paid_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_amt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    payment_ref_id = models.CharField(max_length=30, blank=True, null=True)
    payment_gateway_name = models.CharField(max_length=100, blank=True, null=True)
    payment_type = models.CharField(max_length=100, blank=True, null=True)
    payment_source = models.CharField(max_length=15, blank=True, null=True)
    order_source = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    bank_transaction_id = models.CharField(max_length=50, blank=True, null=True)
    transaction_time = models.DateTimeField(blank=True, null=True)
    payment_mod = models.CharField(max_length=50, blank=True, null=True)
    bankname = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=9, blank=True, null=True, choices=Order_option_choices)
    cron_processed_flag = models.CharField(max_length=1, blank=True, null=True)
    source_url = models.TextField(blank=True, null=True)
    source_type = models.CharField(max_length=100, blank=True, null=True)
    source_id = models.IntegerField(blank=True, null=True)
    source_name = models.CharField(max_length=254, blank=True, null=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    buyer_shipping_cost = models.IntegerField(blank=True, null=True)
    order_type = models.CharField(max_length=150, blank=True, null=True)
    utm_source = models.CharField(max_length=255, blank=True, null=True)
    coupon_discount = models.IntegerField(blank=True, null=True)
    coupon_is_valid = models.CharField(max_length=20, blank=True, null=True)
    user_phone_no = models.CharField(max_length=15, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_header'
    def __unicode__(self):
        return str(self.order_id)

class OrderInvoice(models.Model):
    order_number = models.CharField(max_length=255)
    invoicenumber = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'order_invoice'


class OrderLine(models.Model):
    order_line_id = models.IntegerField(primary_key=True, db_column='id')
    order= models.ForeignKey(OrderHeader)  # this is order header id
    subscribed_product_id = models.IntegerField()
    base_product_id = models.IntegerField()
    store_id = models.IntegerField()
    store_name = models.CharField(max_length=150, blank=True, null=True)
    store_email = models.CharField(max_length=150, blank=True, null=True)
    store_front_id = models.IntegerField(blank=True, null=True)
    store_front_name = models.CharField(max_length=250, blank=True, null=True)
    seller_name = models.CharField(max_length=150, blank=True, null=True)
    seller_phone = models.CharField(max_length=150, blank=True, null=True)
    seller_address = models.TextField(blank=True, null=True)
    seller_state = models.CharField(max_length=150, blank=True, null=True)
    seller_city = models.CharField(max_length=150, blank=True, null=True)
    colour = models.CharField(max_length=30, blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)
    product_name = models.CharField(max_length=256, blank=True, null=True)
    product_qty = models.IntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    shipping_charges = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20,choices=Order_option_choices)
    delivery_request_id = models.CharField(max_length=255)
    delivery_tracking_number = models.CharField(max_length=255)
    product_title = models.CharField(max_length=500, blank=True, null=True)
    vatrate = models.CharField(max_length=10, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_vat = models.CharField(max_length=20, blank=True, null=True)
    pickup_date=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    lead_time=models.CharField(null=True,blank=True,max_length=11)
    remarks=models.CharField(null=True,blank=True,max_length=11)
   

    class Meta:
        managed = False
        db_table = 'order_line'

    
 

class OrderLogs(models.Model):
    order_id = models.IntegerField(blank=True, null=True)
    inputs = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_logs'


class PgTransactions(models.Model):
    order_id = models.IntegerField()
    order_no = models.CharField(max_length=50, blank=True, null=True)
    pg_request = models.TextField(blank=True, null=True)
    pg_response = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    reason = models.CharField(max_length=250, blank=True, null=True)
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
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_attribute_mapping'


class ProductCategoryMapping(models.Model):
    base_product_id = models.IntegerField()
    category_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_category_mapping'
        unique_together = (('base_product_id', 'category_id'),)


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
    code = models.CharField(max_length=20, blank=True, null=True)
    min_cart_total = models.IntegerField(blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True)
    expiry_date = models.DateTimeField()
    msg = models.CharField(max_length=255, blank=True, null=True)

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
    name = models.CharField(max_length=100, blank=True, null=True)
    title_of_review = models.TextField(blank=True, null=True)
    review = models.TextField()
    status = models.IntegerField()
    ip_address = models.TextField(blank=True, null=True)
    submited_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'


class Sessions(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    expire = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class SolrBackLog(models.Model):
    subscribed_product_id = models.IntegerField()
    is_deleted = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'solr_back_log'


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_code = models.CharField(max_length=255, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    store_details = models.TextField(blank=True, null=True)
    store_logo = models.CharField(max_length=255, blank=True, null=True)
    seller_name = models.CharField(max_length=255, blank=True, null=True)
    business_address = models.CharField(max_length=300, blank=True, null=True)
    business_address_country = models.CharField(max_length=100, blank=True, null=True)
    business_address_state = models.CharField(max_length=100, blank=True, null=True)
    business_address_city = models.CharField(max_length=100, blank=True, null=True)
    business_address_pincode = models.CharField(max_length=100, blank=True, null=True)
    mobile_numbers = models.CharField(max_length=100, blank=True, null=True)
    telephone_numbers = models.CharField(max_length=100, blank=True, null=True)
    visible = models.SmallIntegerField()
    meta_title = models.CharField(max_length=150, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.CharField(max_length=150, blank=True, null=True)
    customer_value = models.DecimalField(max_digits=12, decimal_places=4)
    chat_id = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    tin = models.CharField(max_length=255, blank=True, null=True)
    pan = models.CharField(max_length=255, blank=True, null=True)
    contact_persion_name = models.CharField(max_length=255, blank=True, null=True)
    con_per_mobile = models.CharField(max_length=255, blank=True, null=True)
    con_per_email = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    ac_number = models.CharField(max_length=255, blank=True, null=True)
    branch_code = models.CharField(max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=255, blank=True, null=True)
    rtgs_code = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField()
    vtiger_status = models.IntegerField()
    vtiger_accountid = models.IntegerField()
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.SmallIntegerField()
    tagline = models.CharField(max_length=256, blank=True, null=True)
    is_tagline = models.IntegerField()
    store_api_key = models.CharField(max_length=100)
    store_api_password = models.CharField(max_length=100)
    redirect_url = models.TextField(blank=True, null=True)
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
    store_front_name = models.CharField(max_length=255, blank=True, null=True)
    store_front_api_key = models.CharField(max_length=100, blank=True, null=True)
    store_front_api_password = models.CharField(max_length=100, blank=True, null=True)
    store_front_api_token = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.SmallIntegerField()
    parent_id = models.IntegerField()
    tagline = models.CharField(max_length=255)
    is_tagline = models.IntegerField()
    redirect_url = models.TextField(blank=True, null=True)
    seller_mailer_flag = models.IntegerField()
    buyer_mailer_flag = models.IntegerField()
    vendor_coupon_prefix = models.CharField(max_length=10)
    order_prefix = models.CharField(max_length=11)

    class Meta:
        managed = False
        db_table = 'store_front'


class StoreShippingCharge(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField()
    price = models.IntegerField()
    shipping_charge = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'store_shipping_charge'


class StorefrontFbpageMapping(models.Model):
    store_front_id = models.IntegerField()
    page_id = models.CharField(max_length=40)
    page_name = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    modify_on = models.DateTimeField(blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storefront_fbpage_mapping'


class SubscribedProduct(models.Model):
    subscribed_product_id = models.AutoField(primary_key=True)
    base_product_id = models.IntegerField()
    store_id = models.IntegerField()
    unit_rate = models.DecimalField(max_digits=12, decimal_places=4)
    store_price = models.DecimalField(max_digits=12, decimal_places=4)
    secondary_store_price = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True)
    store_offer_price = models.DecimalField(max_digits=12, decimal_places=4)
    weight = models.CharField(max_length=100, blank=True, null=True)
    length = models.CharField(max_length=100, blank=True, null=True)
    width = models.CharField(max_length=100, blank=True, null=True)
    height = models.CharField(max_length=100, blank=True, null=True)
    warranty = models.CharField(max_length=100, blank=True, null=True)
    prompt = models.SmallIntegerField(blank=True, null=True)
    prompt_key = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField()
    checkout_url = models.CharField(max_length=2083, blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField()
    is_deleted = models.SmallIntegerField()
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
    thumb_url = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)

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
    is_deleted = models.SmallIntegerField()
    is_mega_category = models.SmallIntegerField()
    category_shipping_charge = models.IntegerField()
    status = models.IntegerField()
    cat_tax_per = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'tax_master'


class UserAddress(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    addedon = models.DateTimeField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    landmark = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_address'



class  OrderLine_History(models.Model):
    created_date=models.DateTimeField(blank=False,null=False)
    order_line_id=models.IntegerField(blank=True,null=True)
    actions=models.CharField(max_length=255,blank=True,null=True)  
    change_from =models.TextField(blank=True,null=True)
    change_to=models.TextField(blank=True,null=True)  
    User=models.CharField(max_length=200,blank=True,null=True)

    class Meta:
        managed = False
        db_table = 'orderline_history'



class linestatus(models.Model):
    line_name=models.CharField(max_length=200,blank=True,null=True)
    order_status=models.ForeignKey('orderstatus',null=True,blank=True,db_column='order_status')
    # rank=models.ForeignKey('orderstatus',related_name='order_by',null=True,blank=True)

    class Meta:
        managed = False
        db_table = 'linestatus'
