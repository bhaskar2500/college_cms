from Products.models import *
from django.db.models import Q

def update_slug():
    base_ids = SubscribedProduct.objects.filter(Q(base_product__slug__isnull=True)).\
        values('base_product_id', 'base_product__title', 'subscribed_product_id')
    subs_ids = [int(c['subscribed_product_id']) for c in base_ids]
    base_title_map = {}

    for base in base_ids:
        if not base['base_product__title']:
            continue
        base_title_map.update({base['base_product_id']: base['base_product__title']})

    pcam_list = ProductCategoryAttributesMapping.objects.filter(\
        subscribed_product_id__in=subs_ids, category_attribute__is_varing=True).\
        values('subscribed_product__base_product_id', \
           'text_value', \
           'int_value', \
           'decimal_value',\
           'category_attribute__attr_type')

    base_slug_dict = {}

    for pcam in pcam_list:
        attr_type = pcam['category_attribute__attr_type']
        attr_type = attr_type if not attr_type == 'dropdown' else 'text'
        value = pcam[attr_type + '_value'].replace(' ','-')
        base_slug_dict.setdefault(pcam['subscribed_product__base_product_id'], []).append(value)

    for bid, title in base_slug_dict.items():
        variant_val_list = []
        title = base_title_map[bid]
        if bid in base_slug_dict:
            variant_val_list = base_slug_dict[bid]
            variant_val_list = list(set(variant_val_list))
        main_slug = str(title.replace(' ','-')) + '-' + '-'.join(variant_val_list)
        base_slug = "/buy-online/" + main_slug + "/" + str(bid)
        print '--->' + str(bid) + ' == ' + main_slug

        pcm_obj = ProductCategoryMapping.objects.filter(base_product_id=bid)
        default_category_id = pcm_obj[0].category_id if pcm_obj else 0

        BaseProduct.objects.filter(base_product_id=bid).update(slug=base_slug, default_category=default_category_id)
        ProductCategoryMapping.objects.filter(base_product_id=bid).update(slug=base_slug)
