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
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from subprocess import call
from settings import BASE_PATH
from subprocess import call
import os
import subprocess
from settings import ENVIRONMENT_VAR, CUR_ENV
from django.utils.safestring import mark_safe

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    spli_category_id = models.IntegerField(null=True,blank=True, default=0)
    category_name = models.CharField(max_length=255)
    parent_category_id = models.ForeignKey("Category.Category",db_column="parent_category_id", null=True)
    level = models.IntegerField()
    path = models.CharField(max_length=255)
    created_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.IntegerField(default=0)
    is_mega_category = models.IntegerField(default=0)
    category_shipping_charge = models.IntegerField(default=0)
    status = models.IntegerField()
    cat_tax_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    cat_banner_img = models.CharField(max_length=255, null=True, blank=True, default='')
    cat_pro_img = models.ImageField(upload_to='static/catproductimages', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'

    def __unicode__(self):
        return self.category_name

    def image_tag(self):
        if self.cat_pro_img:
	        return mark_safe('<img src="http://www.supplified.com/admin/catproductimages/%s" />'%self.cat_pro_img)
        else:
            return ""
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        tcat_pro_img = str(self.cat_pro_img).split('/')[-1]
        self.cat_pro_img = tcat_pro_img
        # updating slug
        self.slug = '/online-buy/' + (self.category_name.replace(' ','-')) + '/' + self.category_id
        super(Category, self).save(*args, **kwargs)
        onoff_base_product_status(self.category_id, self.status, 'prod_stack2')
        move_image(tcat_pro_img)

        sync_categ = self.__dict__
        del(sync_categ['_state'])
        sync_store_with_testing(sync_categ)

def sync_store_with_testing(data_dict):
    keys = data_dict.keys()
    values = [str(c) for c in data_dict.values()]
    update_str = [ str(k) + ' = "' + str(data_dict[k]) + '"' for k in keys]
    query = 'INSERT INTO category (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s'%\
        (','.join(keys), '"' + '","'.join(values) + '"', ','.join(update_str))
    cursor = connections['test_prod_stack2'].cursor()
    try:
        cursor.execute(query)
        onoff_base_product_status(data_dict['category_id'], data_dict['status'], 'test_prod_stack2')
    except Exception, e:
        print 'Error while syncing data with production server: ', str(e)
    subprocess.call(["sudo", "service", "memcached", "restart"], shell=True)

def onoff_base_product_status(category_id, status, database):
    from Products.models import BaseProduct, ProductCategoryMapping
    PCM = ProductCategoryMapping.objects.using(database).filter(category_id=category_id)
    if PCM:
       base_ids = map(lambda x: x.base_product_id, PCM)
       BaseProduct.objects.using(database).filter(base_product_id__in = base_ids).update(status=status)

def move_image(cat_pro_img):
  try:
     directory = os.getcwd() +'/static/catproductimages'
     if not os.path.exists(directory):
        os.makedirs(directory)
     file_path = directory + '/' + str(cat_pro_img)
     CUR_ENV = 'production'
     print 'cp '+ directory + '/' + str(cat_pro_img) + ' /www/public_html/admin/catproductimages/'
     subprocess.call(["scp","-i",ENVIRONMENT_VAR[CUR_ENV]['pem'], file_path, "ubuntu@%s:/www/public_html/admin/catproductimages/"%(ENVIRONMENT_VAR[CUR_ENV]['dns'])])
     subprocess.call(['cp '+ directory + '/' + str(cat_pro_img) + ' /www/public_html/admin/catproductimages/'], shell=True)
  except Exception, e:
     print str(e)
