from django.db import models
from django.db import connection, connections

class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_code = models.CharField(max_length=255, blank=True)
    store_name = models.CharField(max_length=255, blank=True, verbose_name='Store Name')
    store_details = models.TextField(blank=True)
    store_logo = models.CharField(max_length=255, blank=True)
    seller_name = models.CharField(max_length=255, blank=True, verbose_name='Vendor Name')
    business_address = models.CharField(max_length=300, blank=True, verbose_name='Address')
    business_address_country = models.CharField(max_length=100, blank=True)
    business_address_state = models.CharField(max_length=100, blank=True, verbose_name='State')
    business_address_city = models.CharField(max_length=100, blank=True, verbose_name='City')
    business_address_pincode = models.CharField(max_length=100, blank=True, verbose_name='Pincode')
    mobile_numbers = models.CharField(max_length=100, blank=True, verbose_name='Mobile')
    telephone_numbers = models.CharField(max_length=100, blank=True)
    visible = models.IntegerField(blank=True, null=True, default=0)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)
    customer_value = models.DecimalField(max_digits=12, decimal_places=4, blank=True, null=True, default=0.0)
    chat_id = models.CharField(max_length=45, blank=True)
    email = models.CharField(max_length=255, blank=True)
    tin = models.CharField(max_length=255, blank=True)
    pan = models.CharField(max_length=255, blank=True)
    contact_persion_name = models.CharField(max_length=255, blank=True)
    con_per_mobile = models.CharField(max_length=255, blank=True)
    con_per_email = models.CharField(max_length=255, blank=True, verbose_name='Vendor Email')
    bank_name = models.CharField(max_length=255, blank=True)
    ac_number = models.CharField(max_length=255, blank=True)
    branch_code = models.CharField(max_length=255, blank=True)
    ifsc_code = models.CharField(max_length=255, blank=True)
    rtgs_code = models.CharField(max_length=255, blank=True)
    status = models.IntegerField(blank=True, null=True, default=0)
    vtiger_status = models.IntegerField(blank=True, null=True, default=0)
    vtiger_accountid = models.IntegerField(blank=True, null=True, default=0)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True, default=0)
    tagline = models.CharField(max_length=256, blank=True)
    is_tagline = models.IntegerField(blank=True, null=True, default=0)
    store_api_key = models.CharField(max_length=100,blank=True, null=True, default="")
    store_api_password = models.CharField(max_length=100, blank=True, null=True, default="")
    redirect_url = models.TextField(blank=True, default="")
    seller_mailer_flag = models.IntegerField(blank=True, null=True, default=0)
    buyer_mailer_flag = models.IntegerField(blank=True, null=True, default=0)
    channel_name = models.CharField(max_length=255, blank=True, null=True, default="")
    channel_id = models.CharField(max_length=255, blank=True, null=True, default="")
    order_prefix = models.CharField(max_length=11, blank=True, null=True, default="")
    is_active_valid = models.IntegerField(blank=True, null=True, default=0)
    store_shipping_charge = models.IntegerField(blank=True, null=True, default=0)
    store_tax_per = models.FloatField(blank=True, null=True, default=0)

    class Meta:
        managed = False
        db_table = 'store'

    def __unicode__(self):
        return self.seller_name + ' - (ID: ' + str(self.store_id) + ')'

    def save(self, *args, **kwargs):
        super(Store, self).save(*args, **kwargs)

        new_store = self.__dict__
        del(new_store['_state'])
        sync_store_with_production(new_store)

def sync_store_with_production(data_dict):
    keys = data_dict.keys()
    values = [str(c) for c in data_dict.values()]
    update_str = [ str(k) + ' = "' + str(data_dict[k]) + '"' for k in keys]
    query = 'INSERT INTO store (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s'%\
        (','.join(keys), '"' + '","'.join(values) + '"', ','.join(update_str))
    cursor = connections['test_prod_stack2'].cursor()
    try:
        cursor.execute(query)
    except Exception, e:
        print 'Error while syncing data with production server: ', str(e)

class StoreShippingCharge(models.Model):
    store = models.ForeignKey(Store, null=True, db_column='store_id')
    price = models.IntegerField()
    shipping_charge = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'store_shipping_charge'

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

class StorePriceMapping(models.Model):
    base_product = models.ForeignKey('Products.BaseProduct', blank=True, null=True)
    subscribed_product = models.ForeignKey('Products.SubscribedProduct', blank=True, null=True)
    store_id = models.IntegerField()
    publish = models.IntegerField()
    # new columns
    region_id = models.IntegerField(default=0)
    price_type = models.CharField(max_length=255, blank=True, null=True)
    store_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    markup = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    store_offer_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    moq_retail = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    moq_incremental_retail = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    moq_enterprise = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    moq_increment_enterprise = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    dispatch_location = models.TextField(null=True, blank=True)
    vat = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    shipping_charge = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    stock_status = models.IntegerField(default=0)
    price_validity = models.DateTimeField(null=True, blank=True)
    shipment_mode = models.CharField(max_length=255, blank=True, null=True)
    is_cancelable = models.BooleanField(default=False)
    is_cod = models.BooleanField(default=False)
    is_returnable = models.BooleanField(default=False)
    processing_time = models.IntegerField(default=7)
    conforming_standard = models.CharField(max_length=255, blank=True, null=True)
    warranty = models.TextField(null=True, blank=True)
    item_buying_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'store_price_mapping'
