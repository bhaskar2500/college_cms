# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class ProductsAttributes(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products_attributes'


class ProductsCategoryattributesmapping(models.Model):
    category_id = models.IntegerField(blank=True, null=True)
    attribute_id = models.IntegerField(blank=True, null=True)
    value_constraint = models.TextField(blank=True, null=True)
    attr_type = models.CharField(max_length=255, blank=True, null=True)
    is_mandatory = models.IntegerField()
    is_spec = models.IntegerField()
    is_varing = models.IntegerField()
    is_filter = models.IntegerField()
    is_dropdown = models.IntegerField()
    sequence = models.IntegerField(blank=True, null=True)
    for_base = models.IntegerField()
    for_subscribed = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Products_categoryattributesmapping'
        unique_together = (('category_id', 'attribute_id'),)


class ProductsProductcategoryattributesmapping(models.Model):
    subscribed_product_id = models.IntegerField(blank=True, null=True)
    subscribed_ref_id = models.CharField(max_length=20, blank=True, null=True)
    category_attribute_id = models.IntegerField(blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)
    int_value = models.IntegerField(blank=True, null=True)
    decimal_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products_productcategoryattributesmapping'
        unique_together = (('subscribed_product_id', 'category_attribute_id'),)


class ProductsProductcategoryattributesmappingfilters(models.Model):
    base_product_id = models.IntegerField(blank=True, null=True)
    subscribed_product_id = models.IntegerField(blank=True, null=True)
    subscribed_ref_id = models.CharField(max_length=20, blank=True, null=True)
    category_attribute_id = models.IntegerField(blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)
    int_value = models.IntegerField(blank=True, null=True)
    decimal_value = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products_productcategoryattributesmappingfilters'
        unique_together = (('base_product_id', 'subscribed_product_id', 'category_attribute_id'),)


class ProductsProducttaxmastermapping(models.Model):
    base_product_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Products_producttaxmastermapping'


class BaseProduct(models.Model):
    base_product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    small_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=255)
    unit_of_measurement_one = models.CharField(max_length=150)
    model_number = models.CharField(max_length=255)
    key_features = models.TextField()
    meta_title = models.CharField(max_length=150)
    meta_keyword = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=150)
    status = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    video_url = models.CharField(max_length=255)
    brand_id = models.IntegerField(blank=True, null=True)
    unit_of_measurement_two = models.CharField(max_length=150)
    is_no_follow = models.IntegerField(blank=True, null=True)
    thumb_url = models.CharField(max_length=100)
    base_ref_id = models.CharField(max_length=20, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    default_category = models.IntegerField(blank=True, null=True)
    combo_categories = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    business_unit = models.TextField(blank=True, null=True)
    sub_category = models.CharField(max_length=255, blank=True, null=True)
    sub_sub_category = models.CharField(max_length=255, blank=True, null=True)
    brand_type = models.CharField(max_length=255, blank=True, null=True)
    standard_packing_uom = models.CharField(max_length=255, blank=True, null=True)
    unit_quantity_uom = models.CharField(max_length=255, blank=True, null=True)
    purchase_price_uom = models.CharField(max_length=255, blank=True, null=True)
    installation_uom = models.CharField(max_length=255, blank=True, null=True)
    installation_with_material_uom = models.CharField(max_length=255, blank=True, null=True)
    classifications = models.CharField(max_length=255, blank=True, null=True)
    categoryids = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_product'


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
    moq_increment = models.DecimalField(max_digits=65, decimal_places=2)
    store_id = models.IntegerField()
    store_code = models.CharField(max_length=255, blank=True, null=True)
    store_name = models.CharField(max_length=300, blank=True, null=True)
    deleted_date = models.DateTimeField()
    skucode = models.CharField(db_column='SKUCode', max_length=255)  # Field name made lowercase.
    lead_time = models.IntegerField()
    install_qty = models.IntegerField()
    install_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    installation_moq = models.IntegerField(blank=True, null=True)
    installation_uom = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'history_mycart'


class Linestatus(models.Model):
    l_id = models.IntegerField(primary_key=True)
    status = models.ForeignKey('Orderstatus', blank=True, null=True)
    line_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'linestatus'


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
    is_staff = models.IntegerField()
    group_type = models.CharField(max_length=2)

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
    moq_increment = models.DecimalField(max_digits=65, decimal_places=2)
    store_id = models.IntegerField()
    store_code = models.CharField(max_length=255, blank=True, null=True)
    store_name = models.CharField(max_length=300, blank=True, null=True)
    skucode = models.CharField(db_column='SKUCode', max_length=255)  # Field name made lowercase.
    lead_time = models.IntegerField()
    install_qty = models.IntegerField()
    install_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    installation_moq = models.IntegerField(blank=True, null=True)
    installation_uom = models.CharField(max_length=255, blank=True, null=True)
    unit_of_measurement_one = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mycart'


class Newsletter(models.Model):
    email = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'newsletter'


class NewsletterSubEmailid(models.Model):
    id = models.IntegerField()
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
    payment_method = models.CharField(max_length=16, blank=True, null=True)
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
    status = models.CharField(max_length=9, blank=True, null=True)
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
    store_code = models.CharField(max_length=255, blank=True, null=True)
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
    status = models.CharField(max_length=24)
    delivery_request_id = models.CharField(max_length=255)
    delivery_tracking_number = models.CharField(max_length=255)
    product_title = models.CharField(max_length=500, blank=True, null=True)
    vatrate = models.CharField(max_length=10, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_vat = models.CharField(max_length=20, blank=True, null=True)
    skucode = models.CharField(db_column='SKUCode', max_length=255)  # Field name made lowercase.
    lead_time = models.IntegerField()
    install_unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    install_qty = models.IntegerField()
    install_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    installation_moq = models.IntegerField(blank=True, null=True)
    installation_uom = models.CharField(max_length=255, blank=True, null=True)
    unit_of_measurement_one = models.CharField(max_length=150, blank=True, null=True)
    pickup_date = models.DateTimeField(blank=True, null=True)
    remarks = models.CharField(max_length=250, blank=True, null=True)

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


class OrderlineHistory(models.Model):
    order_line_id = models.IntegerField(blank=True, null=True)
    actions = models.CharField(max_length=255, blank=True, null=True)
    change_from = models.TextField(blank=True, null=True)
    change_to = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField()
    user = models.CharField(db_column='User', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orderline_history'


class Orderstatus(models.Model):
    o_id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    status_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orderstatus'


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
    discount_type = models.IntegerField()
    is_staff = models.IntegerField()
    group_type = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'promocode'


class RegionMaster(models.Model):
    name = models.CharField(max_length=255)
    publish = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'region_master'


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
    id = models.CharField(max_length=32)
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


class StorePriceMapping(models.Model):
    base_product_id = models.IntegerField(blank=True, null=True)
    subscribed_product_id = models.IntegerField(blank=True, null=True)
    store_id = models.IntegerField()
    publish = models.IntegerField()
    region_id = models.IntegerField()
    price_type = models.CharField(max_length=255, blank=True, null=True)
    store_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    markup = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    store_offer_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    moq_retail = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    moq_incremental_retail = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    moq_enterprise = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    moq_increment_enterprise = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    dispatch_location = models.TextField(blank=True, null=True)
    vat = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    shipping_charge = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock_status = models.IntegerField()
    price_validity = models.DateTimeField(blank=True, null=True)
    shipment_mode = models.CharField(max_length=255, blank=True, null=True)
    is_cancelable = models.IntegerField()
    is_cod = models.IntegerField()
    is_returnable = models.IntegerField()
    processing_time = models.IntegerField()
    conforming_standard = models.CharField(max_length=255, blank=True, null=True)
    warranty = models.TextField(blank=True, null=True)
    item_buying_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_price_mapping'


class StoreShippingCharge(models.Model):
    id = models.IntegerField()
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


class TempProductList(models.Model):
    id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    pro_name = models.CharField(max_length=255, blank=True, null=True)
    store_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'temp_product_list'


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
