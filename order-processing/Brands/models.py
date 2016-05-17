from django.db import models
from django.db import connection, connections

class Brand(models.Model):
    store_front_id = models.AutoField(primary_key=True)
    store_front_name = models.CharField(max_length=255, blank=True, verbose_name="Brand Name")
    store_front_api_key = models.CharField(max_length=100, blank=True)
    store_front_api_password = models.CharField(max_length=100, blank=True)
    store_front_api_token = models.CharField(max_length=100, blank=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField(default=0)
    parent_id = models.IntegerField(default=0)
    tagline = models.CharField(max_length=255)
    is_tagline = models.IntegerField(default=0)
    redirect_url = models.TextField(blank=True, verbose_name="Brand Code")
    seller_mailer_flag = models.IntegerField(default=0)
    buyer_mailer_flag = models.IntegerField(default=0)
    vendor_coupon_prefix = models.CharField(max_length=10, blank=True, null=True, default='')
    order_prefix = models.CharField(max_length=11, blank=True, null=True, default='')

    class Meta:
        managed = False
        db_table = 'brand'

    def __unicode__(self):
        return self.store_front_name

    def save(self, *args, **kwargs):
        super(Brand, self).save(*args, **kwargs)

        new_brand = self.__dict__
        del(new_brand['_state'])
        sync_brand_with_production(new_brand)

def sync_brand_with_production(data_dict):
    keys = data_dict.keys()
    values = [str(c) for c in data_dict.values()]
    update_str = [ str(k) + ' = "' + str(data_dict[k]) + '"' for k in keys]
    query = 'INSERT INTO brand (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s'%\
        (','.join(keys), '"' + '","'.join(values) + '"', ','.join(update_str))
    cursor = connections['test_prod_stack2'].cursor()
    try:
        cursor.execute(query)
    except Exception, e:
        print 'Error while syncing data with production server: ', str(e)
