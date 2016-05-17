from django.shortcuts import render_to_response
from Products.models import *
from django.db import connection
from Category.models import Category
from django.template import RequestContext
from xlsxwriter import Workbook
import StringIO
import json
from django.http import HttpResponse
from django.db.models import Q
from Products.bulk_product import *
from Products.static_headers import display_name_db_column_mapping as COL_MAP

def export_as_excel(request):
    category_id = request.GET['category'] if 'category' in request.GET else None
    data = get_master_product({'category_id': category_id})
    output = StringIO.StringIO()
    wb = Workbook(output)
    ws = wb.add_worksheet("Sheet 1")
    first_row = 0
    for header in data['table_header']:
        col = data['table_header'].index(header) # we are keeping order.
        ws.write(first_row,col,header) # we have written first row which is the header of worksheet also.

    srow=1
    for row in data['table_data']:
        for _key,_value in row.items():
            col = data['table_header'].index(_key)
            try:
                ws.write(srow,col,_value)
            except Exception, e:
                ws.write(srow,col, json.dumps(_value))

        srow += 1 #enter the next row
    wb.close()
    xlsx_data = output.getvalue()

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=MasterProduct.xlsx'
    response.write(xlsx_data)
    return response

def product_import_page(request):
    category_id = request.GET['category'] if 'category' in request.GET else None
    curr_page = request.GET['p'] if 'p' in request.GET else 1
    all_category_obj = list(Category.objects.filter(level__in=[2,3,4]).\
        values('category_id', 'category_name', 'parent_category_id', 'level').order_by('level', 'category_name'))

    categ_dict_level2 = {}
    categ_dict_level3 = {}
    all_categ_dict = {}
    for c in all_category_obj:
        level = c['level']
        all_categ_dict.update({c['category_id']: c})
        if level == 2:
            categ_dict_level2.update({
                    c['category_id']: []
                })
        if level == 3:
            categ_dict_level2[c['parent_category_id']].append(c['category_id'])
            categ_dict_level3.update({
                    c['category_id']: []
                })
        if level == 4:
            if c['parent_category_id'] in categ_dict_level3:
                categ_dict_level3[c['parent_category_id']].append(c['category_id'])

    category_str = '';
    for key, value in categ_dict_level2.items():
        category_str += '<option class="text-success" value="'+ str(all_categ_dict[key]["category_id"]) +\
             '">' + all_categ_dict[key]["category_name"] + '</option>'
        if value:
            for key2 in value:
                category_str += '<option class="text-info" value="'+ str(all_categ_dict[key2]["category_id"]) + '">&nbsp;-- ' +\
                     all_categ_dict[key2]["category_name"] + '</option>'
                if key2 in categ_dict_level3 and categ_dict_level3[key2]:
                    for key3 in categ_dict_level3[key2]:
                        category_str += '<option class="text-danger" value="'+\
                            str(all_categ_dict[key3]["category_id"]) + '">&nbsp;&nbsp;&nbsp;&nbsp;-- ' +\
                            all_categ_dict[key3]["category_name"] + '</option>'

    returned_data = {
        'all_category': category_str,
        'selected_category_id': int(category_id) if category_id else None
    }
    returned_data.update(get_master_product({
            'curr_page': curr_page,
            'category_id': category_id
        }))
    return render_to_response('product_import.html', returned_data, context_instance=RequestContext(request))

def get_master_product(filter_dict={}):
    print ' ========== Getting master data for filters =============> ', filter_dict
    """ master excel containing subscribed product data """
    mp_obj = MasterProduct()
    mp_obj.getProductCategory()
    base_category_dict = mp_obj.prod_categ_map

    pcam_query_dict = Q()
    subs_prod_filter_dict = Q()

    base_product_ids_list = []
    # filter for category ( mandatory )
    if 'category_id' in filter_dict and filter_dict['category_id']:
        base_product_ids = ProductCategoryMapping.objects.\
            filter(category_id=filter_dict['category_id']).\
            values_list('base_product_id', flat=True)
        print 'base ids ---->', base_product_ids, filter_dict['category_id']
        base_product_ids_list = [int(c) for c in base_product_ids]
        pcam_query_dict &= Q(category_attribute__category_id=filter_dict['category_id'])
    else:
        return {
            'table_header': [],
            'table_data': [],
            'total_count': 0
        }

    print '------------------------------------------>'
    # filter for base product
    if 'base_product_id' in filter_dict:
        base_product_ids_list += filter_dict['base_product_id']
    if 'base_ref_id' in filter_dict:
        subs_prod_filter_dict &= Q(base_ref_id__in = filter_dict['base_ref_id'])

    if base_product_ids_list:
        subs_prod_filter_dict &= Q(base_product_id__in = base_product_ids_list)
    else:
        return {
            'table_header': [],
            'table_data': [],
            'total_count': 0
        }
    # filter for subscribed product
    if 'subscribed_product_id' in filter_dict:
        subs_prod_filter_dict &= Q(subscribed_product_id__in = filter_dict['subscribed_product_id'])
        pcam_query_dict &= Q(subscribed_product_id__in = filter_dict['subscribed_product_id'])

    if 'subscribed_ref_id' in filter_dict:
        subs_prod_filter_dict &= Q(subscribed_ref_id__in = filter_dict['subscribed_ref_id'])
        pcam_query_dict &= Q(subscribed_ref_id__in = filter_dict['subscribed_ref_id'])

    subs_base_columns = ['base_product_id', 'business_unit', \
        'sub_category', 'sub_sub_category', 'brand', 'brand_type', 'title',\
        'description', 'standard_packing_uom', \
        'unit_quantity_uom', 'purchase_price_uom', 'unit_of_measurement_one', \
        'unit_of_measurement_two', 'installation_uom', 'installation_with_material_uom', \
        'classifications', 'categoryids']

    subs_base_columns = ['base_product__' + c for c in subs_base_columns]
    subs_base_columns.insert(1, 'subscribed_product_id')
    subs_columns = ['standard_packing_quantity', \
        'installation_price', 'installation_sow', 'installation_with_material_price', \
        'installation_with_material_sow', 'combo', 'status', 'sku', 'quantity',\
        'thumb_url', 'specifications']

    final_subs_columns = subs_base_columns + subs_columns

    # getting subscribed product
    products = SubscribedProduct.objects.filter(subs_prod_filter_dict).values(*final_subs_columns).order_by('subscribed_product_id')
    total_product = len(products)
    if 'curr_page' in filter_dict:
        curr_page = filter_dict['curr_page']
        page_limit = 100
        products = products[(curr_page-1)*page_limit : curr_page*page_limit]
    else:
        products = products

    # getting attributes for fetched subscribed products in above query
    subscribed_ids = [int(c['subscribed_product_id']) for c in products]

    pcam_list = ProductCategoryAttributesMapping.objects.filter(subscribed_product_id__in = subscribed_ids).\
        values('subscribed_product_id', 'category_attribute__attribute__name', \
            'text_value', 'int_value', 'decimal_value', 'category_attribute__attr_type')

    # merging rows that belong to same subscribed id into one dictionary,
    # and key subscribed_product_id, values as merged dictionary
    pcam_subs_map = {}
    for pcam in pcam_list:
        attr_type = pcam['category_attribute__attr_type']
        attr_type = 'text' if attr_type == 'dropdown' else attr_type
        pcam_subs_map.setdefault(pcam['subscribed_product_id'], {}).\
            update({
                    pcam['category_attribute__attribute__name']: pcam[attr_type + '_value'] or ''
                })

    # adding the merged dictionary to respective subscribed product row
    # and changing the column name wherever required (for base and subscribed product only)
    final_products = []
    product_keys = {}
    COL_MAP_REV = {v: k for k, v in COL_MAP.items()}

    # getting attribute name list w.r.t category id
    categ_attr_list = CategoryAttributesMapping.objects.filter(category_id=filter_dict['category_id'], status=True)
    categ_attr_list = [str(c.attribute.name) for c in categ_attr_list]
    categ_attr_dict = {
        str(c): '' for c in categ_attr_list
    }

    for prod in products:
        prod_with_new_keys = {}
        prod.update(categ_attr_dict)
        for k,v in prod.items():
            col_index = None
            try:
                col_index = final_subs_columns.index(k)
            except:
                pass
            k = k.replace('base_product__', '')
            # special case for key features
            if k == 'key_features':
                v = deserialise_key_features(v)
            if k == 'categoryids':
                if prod['base_product__base_product_id'] in base_category_dict:
                    v = ','.join(base_category_dict[prod['base_product__base_product_id']])
            k = COL_MAP_REV[k] if k in COL_MAP_REV else k
            if not col_index == None:
                final_subs_columns[col_index] = k
            product_keys.update({k: 1})
            prod_with_new_keys.update({k: v})

        if prod['subscribed_product_id'] in pcam_subs_map:
            prod_with_new_keys.update(pcam_subs_map[prod['subscribed_product_id']])
        final_products.append(prod_with_new_keys)

    # creating header keys for excel column
    print 'Category attributes : ', categ_attr_list
    header_keys = final_subs_columns + categ_attr_list
    return {
            'table_header': header_keys,
            'table_data': final_products,
            'total_count': total_product
        }

def deserialise_specifications(data):
    if not data:
       return ''
    try:
        data = json.loads(data)
        rdata = []
        for k,v in data.items():
            rdata.append(k + ':' + v)
        return ';'.join(rdata)
    except Exception, e:
        return data

def deserialise_key_features(data):
    if not data:
       return ''
    try:
        data = json.loads(data)
        rdata = []
        for k,v in data.items():
            rdata.append(k)
        return ';'.join(rdata)
    except Exception, e:
        return data

def product_bulk_page(request):
    return render_to_response("common_bulk_upload.html", {
            'page_header': 'Product',
            'process_name': 'Subscribed Product',
            'process_type': [
                    {'text': 'Create new Products', 'value': 'create'},
                    {'text': 'Add New Subscribed', 'value': 'add'},
                    {'text': 'Update Products', 'value': 'update'},
                ],
            'action_url': '/admin/upload'
        }, context_instance=RequestContext(request))
