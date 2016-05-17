from django.db import models
from Stores.models import Store
from Brands.models import Brand
from Category.models import Category

class BaseProduct(models.Model):
    base_product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,blank=True, null=True)
    small_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True,null=True)
    brand = models.CharField(max_length=255, blank=True)
    unit_of_measurement_one = models.CharField(max_length=150, blank=True)
    model_number = models.CharField(max_length=255, blank=True)
    key_features = models.TextField(blank=True)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_keyword = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)
    status = models.IntegerField(blank=True, null=True, default=0)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    video_url = models.CharField(max_length=255, blank=True)
    brand_id = models.ForeignKey(Brand, db_column='brand_id', blank=True, null=True)
    unit_of_measurement_two = models.CharField(max_length=150, blank=True)
    is_no_follow = models.IntegerField(blank=True, null=True)
    thumb_url = models.ImageField(blank=True, upload_to="../../supplified-front/admin/media/product/thumbnail/150x150/5/6/")
    base_ref_id = models.CharField(null=True, blank=True, max_length=20)
    slug = models.CharField(null=True, blank=True, max_length=255)
    default_category = models.IntegerField(blank=True, null=True, default=0)
    combo_categories = models.CharField(null=True, blank=True, max_length=255, default=None)
    keywords = models.TextField(null=True, blank=True)
    # new columns according to new attributes
    business_unit = models.TextField(null=True, blank=True)
    sub_category = models.CharField(null=True, blank=True, max_length=255)
    sub_sub_category = models.CharField(null=True, blank=True, max_length=255)
    brand_type = models.CharField(null=True, blank=True, max_length=255)
    standard_packing_uom = models.CharField(null=True, blank=True, max_length=255)
    unit_quantity_uom = models.CharField(null=True, blank=True, max_length=255)
    purchase_price_uom = models.CharField(null=True, blank=True, max_length=255)
    installation_uom = models.CharField(null=True, blank=True, max_length=255)
    installation_with_material_uom = models.CharField(null=True, blank=True, max_length=255)
    classifications = models.CharField(null=True, blank=True, max_length=255)
    categoryids = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'base_product'

    def update_slug(self):
        base_ids = BaseProduct.objects.filter(Q(slug__isnull=True) | Q(default_category=0) | \
                Q(default_category__isnull=True)).values('base_product_id', 'title')
        for bid in base_ids:
            base_slug = "/buy-online/" + str(bid['title'].replace(' ','-')) + "/" + str(bid['base_product_id'])
            pcm_obj = ProductCategoryMapping.objects.filter(base_product_id=bid['base_product_id'])
            default_category_id = pcm_obj[0].category_id if pcm_obj else 0
            BaseProduct.objects.filter(base_product_id=bid['base_product_id']).update(slug=base_slug,\
                 default_category=default_category_id)
            ProductCategoryMapping.objects.filter(base_product_id=bid['base_product_id']).update(slug=base_slug)

    def __unicode__(self):
        return self.title + ' - ' + str(self.base_product_id)

class SubscribedProduct(models.Model):
    base_ref_id = models.CharField(null=True, blank=True, max_length=20)
    subscribed_ref_id = models.CharField(null=True, blank=True, max_length=20)
    subscribed_product_id = models.AutoField(primary_key=True)
    base_product = models.ForeignKey(BaseProduct, null=True)
    status = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.IntegerField(null=True, blank=True, default=0)
    sku = models.CharField(max_length=128, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    thumb_url = models.ImageField(blank=True, upload_to="../../supplified-front/admin/media/product/thumbnail/150x150/5/6/")

    standard_packing_quantity = models.CharField(null=True, blank=True, max_length=255)
    installation_price = models.DecimalField(max_digits=65, decimal_places=2, null=True, blank=True)
    installation_sow = models.TextField(null=True, blank=True)
    installation_with_material_price = models.DecimalField(max_digits=65, decimal_places=2, null=True, blank=True)
    installation_with_material_sow = models.TextField(null=True, blank=True)
    # Comma seperated category ids
    combo = models.TextField(null=True, blank=True)
    specifications = models.TextField(blank=True)

    class Meta:
        db_table = 'subscribed_product'

    def __unicode__(self):
        return str(self.base_product_id)

class ProductAttributeMapping(models.Model):
    base_product_id = models.IntegerField()
    attribute_id = models.IntegerField()
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'product_attribute_mapping'

class ProductCategoryMapping(models.Model):
    base_ref_id = models.IntegerField(null=True, blank=True)
    base_product = models.ForeignKey(BaseProduct)
    category = models.ForeignKey(Category)
    slug = models.CharField(max_length=250, blank=True)

    class Meta:
        managed = False
        db_table = 'product_category_mapping'

    def __unicode__(self):
        return self.base_product.title + ': ' + self.category.category_name

class ProductFrontendMapping(models.Model):
    subscribed_product_id = models.IntegerField()
    store_front_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'product_frontend_mapping'

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

class ProductPincodeMapping(models.Model):
    store_id = models.IntegerField()
    base_product_id = models.IntegerField()
    store_offer_price = models.DecimalField(max_digits=50, decimal_places=2, blank=True, null=True)
    subscribed_product_id = models.IntegerField(blank=True, null=True)
    store_price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    pincode = models.ForeignKey(PincodeMaster, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_pincode_mapping'

class ProductPriceMapping(models.Model):
    base_product_id = models.IntegerField(blank=True, null=True)
    subscribed_product_id = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_price_mapping'

class ProductTaxMasterMapping(models.Model):
    base_product_id = models.IntegerField()

class StoreProductMapping(models.Model):
    subscribed_product_id = models.IntegerField(blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    base_product_id = models.IntegerField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    expired_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_product_mapping'

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

class Attributes(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

ATTR_TYPE_CHOICES = (
        ('text', 'Text'),
        ('int', 'Number'),
        ('float','Decimal'),
        ('dropdown','Dropdown'),
	('date', 'Date'),
)
"""
class CategoryAttributesMappingManager(models.Manager):
    def get_queryset(self):
        return super(CategoryAttributesMapping, self).get_queryset().filter(status=True)
"""
class CategoryAttributesMapping(models.Model):
    class Meta:
        unique_together = (('category', 'attribute'),)

    category = models.ForeignKey(Category, null=True, blank=True)
    attribute = models.ForeignKey(Attributes, null=True, blank=True)
    #( list of values e.g. [0,1] for "status" attribute)
    value_constraint = models.TextField(blank=True, null=True, default="[]")
    attr_type = models.CharField(max_length=255, blank=True, null=True, choices=ATTR_TYPE_CHOICES)
    is_mandatory = models.BooleanField(default=False)
    is_spec = models.BooleanField(default=False)
    is_varing = models.BooleanField(default=False)
    is_filter = models.BooleanField(default=False)
    is_dropdown = models.BooleanField(default=False)
    sequence = models.IntegerField(blank=True, null=True)
    for_base = models.BooleanField(default=False)
    for_subscribed = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    #objects = CategoryAttributesMappingManager()

    def __unicode__(self):
        return str(self.category) + ' - ' + str(self.attribute)

class ProductCategoryAttributesMappingFilters(models.Model):
    class Meta:
        unique_together = (('base_product', 'subscribed_product', 'category_attribute'),)

    """ for filters only """
    base_product = models.ForeignKey(BaseProduct, null=True, blank=True)
    subscribed_product = models.ForeignKey(SubscribedProduct, null=True, blank=True)
    subscribed_ref_id = models.CharField(null=True, blank=True, max_length=20)
    category_attribute = models.ForeignKey(CategoryAttributesMapping, null=True, blank=True)
    text_value = models.TextField(blank=True, null=True)
    int_value = models.IntegerField(blank=True, null=True)
    decimal_value = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)

class ProductCategoryAttributesMapping(models.Model):
    class Meta:
        unique_together = (('subscribed_product', 'category_attribute'),)

    """ all attributes including filters """
    subscribed_product = models.ForeignKey(SubscribedProduct, null=True, blank=True)
    subscribed_ref_id = models.CharField(null=True, blank=True, max_length=20)
    category_attribute = models.ForeignKey(CategoryAttributesMapping, null=True, blank=True)
    text_value = models.TextField(blank=True, null=True)
    int_value = models.IntegerField(blank=True, null=True)
    decimal_value = models.DecimalField(blank=True, null=True, max_digits=15, decimal_places=2)

    def __unicode__(self):
        return str(self.subscribed_product) + ' - ' + str(self.category_attribute)
