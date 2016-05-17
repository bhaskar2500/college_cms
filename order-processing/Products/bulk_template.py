import xlrd, sys
from xlrd.sheet import ctype_text
from django.shortcuts import render_to_response
from django.template import RequestContext
from Products.models import *
from Category.models import Category

base_fields = ["base_product_id", "Business Unit","Sub Category","Sub Sub Category","Brand","Brand Type","Product Name","Product Description - Content","Standard Packing UOM","Unit Quantity UOM","Purchase Price UOM","Unit Of Measurement - 1","Unit Of Measurement - 2","Installation - UOM","Intst with Mat - UOM","Classifications","Category_ID","Status","Key Features"]

subscribed_fields = ["subscribed_product_id", "Standard Packing Quantity","Unit Quantity","Installation Price","Installation SOW","Installation with Material Price","Installation with Material SOW","Combo/Related Products","Variant On","Status"]

ignore_store = ['Store Name','Pincode Mapping','Price Type','Price (MRP/LP)','Discount','Purchase Price','Markup','Offer Price','MOQ Retail','MOQ Increment Retail','MOQ Enterprise','MOQ Increment Enterprise','Dispatch Location','VAT','Shipping Charge','Stock Status','Price Validity','Shipment Mode','Is_Cancelable','Is_Cod','Is_Returnable','Processing_Time','Conforming Standard','Warranty','Item Buying Type']

not_attr_fields = base_fields + subscribed_fields + ignore_store

def product_bulk_template(request):
    return render_to_response("common_bulk_upload.html", {
            'page_header': 'Category Template',
            'process_name': 'Category Template',
            'process_type': [
            {'text': 'Create/Update', 'value': 'c_u'},
            ],
            'action_url': '/admin/upload'
            }, context_instance=RequestContext(request))

class Category_Template():

    def __init__(self):
        self.download_data_query = {}
        self.master_category_id = ''
        self.error_list = []
        self.error_str = ''
        self.return_data = {'table_header': [],
            'table_data': [],
            'stats': {
                'error': '',
                'extra_headers': [],
                'error_count': 0,
                'success_count': 0
            }}
        self.master_query = ""
        # Check if Base and Subscribed Fields in Database
        db_b_s_fields = CategoryAttributesMapping.objects.filter(category_id=None).values('attribute__name', 'for_base', 'for_subscribed')
        b_missing_fields = list(set(base_fields) - set(map(lambda x:x['attribute__name'], filter(lambda y:y['for_base'] , db_b_s_fields))))
        s_missing_fields = list(set(subscribed_fields) - set(map(lambda x:x['attribute__name'], filter(lambda y:y['for_subscribed'] , db_b_s_fields))))
        b_extra_fields = list(set(map(lambda x:x['attribute__name'], filter(lambda y:y['for_base'] , db_b_s_fields))) - set(base_fields))
        s_extra_fields = list(set(map(lambda x:x['attribute__name'], filter(lambda y:y['for_subscribed'] , db_b_s_fields))) - set(subscribed_fields))
        for b_fields in b_missing_fields:
            b_attr = Attributes(name = b_fields)
            b_attr.save()
            c_attr = CategoryAttributesMapping(attribute_id=b_attr.id, category_id=None, for_base=True)
            c_attr.save()
        for s_fields in s_missing_fields:
            s_attr = Attributes(name = s_fields)
            s_attr.save()
            c_attr = CategoryAttributesMapping(attribute_id=s_attr.id, category_id=None, for_subscribed=True)
            c_attr.save()
        print "Deleting Attributes for Base : ",b_extra_fields
        print "Deleting Attributes for Subscribed : ",s_extra_fields
        CategoryAttributesMapping.objects.filter(attribute__name__in=b_extra_fields, for_base=1).update(status=0)
        CategoryAttributesMapping.objects.filter(attribute__name__in=s_extra_fields, for_subscribed=1).update(status=0)
        return

    def create_update_data(self):
        # Main Category
        category_name = self.data_dict['data'][0]['Category']
        db_cat_vals = Category.objects.filter(parent_category_id__parent_category_id__category_name = category_name).values('category_name','category_id')
        db_cat_map = {str(x['category_name']).strip() : int(x['category_id']) for x in db_cat_vals}
        cat_ignore_cols = ["S.No.","Category","Attribute Name","Specifications","Attribute Type","Input Value Type",
        "Nature of Attributes","Filter"]
        # Mandatory Header Check
        missing_headers = list(set(cat_ignore_cols) - set(self.data_dict['header_keys']))
        if len(missing_headers):
            self.error_str = 'Error : Mandatory Headers required\n ' + (','.join(missing_headers))
            self.return_data = {'table_header': [],
            'table_data': [],
            'stats': {
                'error': self.error_str,
                'extra_headers': [],
                'error_count': 0,
                'success_count': 0
            }}
            return False
        cat_data_key = filter(lambda x: not (x in cat_ignore_cols), self.data_dict['data'][0].keys())
        cat_not_in_db = filter(lambda x: not (x in db_cat_map.keys()), cat_data_key)
        print "Categories in DB : ", db_cat_map.keys()
        if len(cat_not_in_db):
            self.error_str = 'Error : Category Not Found in Database\n %s'%(" , ".join(cat_not_in_db))
            self.return_data = {'table_header': [],
            'table_data': [],
            'stats': {
                'error': self.error_str,
                'extra_headers': [],
                'error_count': 0,
                'success_count': 0
            }}
        print "Categories not in Database : ", cat_not_in_db
        cat_data_key = list(set(cat_data_key) - set(cat_not_in_db))
        print "Category Data to be fed for : ",cat_data_key
        if not len(db_cat_map.keys()):
            print "Couldn't find Master Category : %s"%category_name
        db_attr_list = CategoryAttributesMapping.objects.filter(category_id__in=db_cat_map.values()).values('attribute__name',
                'category_id', 'value_constraint',
                'attribute__id', 'category__category_name', 'attr_type', 'is_mandatory', 'is_spec', 'is_varing', 'is_filter',
                'sequence', 'id')
        # Formating DB attribute category data
        attr_data = {}
        for attr in db_attr_list:
            if not attr['attribute__name'] in attr_data.keys():
                attr_data[attr['attribute__name']] = {'is_mandatory': attr['is_mandatory'], 'is_spec': attr['is_spec'],
                'value_constraint': attr['value_constraint'],
                'attr_type': attr['attr_type'], 'attr_id': attr['attribute__id'],
                'cat_data': {attr['category_id']: {'cat_attr_id' : attr['id'], 'sequence': attr['sequence'],
                'is_filter': attr['is_filter'], 'is_varing': attr['is_varing']}}}
            else:
                attr_data[attr['attribute__name']]['cat_data'][attr['category_id']] = {'cat_attr_id' : attr['id'],
                'sequence': attr['sequence'], 'is_filter': attr['is_filter'], 'is_varing': attr['is_varing']}
        create_attr = []
        create_attr_query = ""
        update_query = ""
        create_query = ""
        delete_query = ""
        insert_values = ""
        delete_attr_ids = []
        attribute_del = list(set(attr_data.keys()) - set(map(lambda x:x['Attribute Name'] ,self.data_dict['data'])))
        print "Attributes in DB : ",attr_data.keys()
        print "Attributes in Sheet : ",map(lambda x:x['Attribute Name'] ,self.data_dict['data'])
        print "Attributes to be deleted : ",attribute_del
        update_cat_attr = ""
        if len(attribute_del):
            del_attr_ids = []
            for del_attr_data in attribute_del:
                del_attr_ids.append(attr_data[del_attr_data]['attr_id'])
            update_cat_attr = """UPDATE Products_categoryattributesmapping as PCAM set status=0 where PCAM.category_id in %s AND PCAM.attribute_id in %s !@#$"""%('('+",".join(map(lambda x: str(x) ,db_cat_map.values())) + ')',
                    '('+",".join(map(lambda x: str(x) ,del_attr_ids)) + ')')
        CategoryAttributesMapping.objects.filter(category_id__in=db_cat_map.values(), attribute__name__in=attribute_del).update()
        for col_data in self.data_dict['data']:
            if 'Attribute Name' not in col_data.keys():
                break
            # Check if Attribute Name
            if col_data['Attribute Name'] not in attr_data.keys():
                # ignore fixed columns (base /subscribed/ store)
                if col_data['Attribute Name'] in not_attr_fields:
                    continue
                new_attr = Attributes(name=col_data['Attribute Name'])
                new_attr.save()
                create_attr_query += "INSERT INTO Products_attributes (id, name) VALUES (%s, '%s') ON DUPLICATE KEY UPDATE name = '%s' !@#$"%(\
                    new_attr.id, col_data['Attribute Name'], col_data['Attribute Name'])
                create_attr += col_data
                attr_data[col_data['Attribute Name']] = {'attr_id': new_attr.id, 'cat_data': {}}
                #continue
            attr_cat_ids = map(lambda x:attr_data[col_data['Attribute Name']]['cat_data'][x]['cat_attr_id'], attr_data[col_data['Attribute Name']]['cat_data'].keys())
            # Checking for updates on attributes
            temp_update_query = ""
            spec_val = 1 if col_data['Specifications'] == 'Yes' else 0
            mandatory_val = 1 if col_data['Attribute Type'] else 0
            try:
                attr_type_val = filter(lambda x: col_data['Input Value Type'].find(x[1]) != -1, ATTR_TYPE_CHOICES)[0][0]
            except:
                print col_data['Input Value Type'],sys.exc_info()
            #filter_val = 1 if col_data['Filter'] else 0
            if len(attr_cat_ids):
                # Specifications
                if attr_data[col_data['Attribute Name']]['is_spec'] != spec_val:
                    attr_data[col_data['Attribute Name']]['is_spec'] = spec_val
                    temp_update_query += "is_spec = %s"%(spec_val)
                # Attribute Type
                if attr_data[col_data['Attribute Name']]['is_mandatory'] != mandatory_val:
                    attr_data[col_data['Attribute Name']]['is_mandatory'] = mandatory_val
                    temp_update_query += "is_mandatory = %s"%(mandatory_val)
                # Input Value Type
                if attr_data[col_data['Attribute Name']]['attr_type'] != attr_type_val:
                    attr_data[col_data['Attribute Name']]['attr_type'] = attr_type_val
                    temp_update_query += "attr_type = '%s'"%attr_type_val
                # Filter
                #if attr_data[col_data['Attribute Name']]['is_filter'] != filter_val:
                #        temp_update_query += "is_filter = "%(filter_val)
                # Forming the Common update query for attribute
                if temp_update_query:
                    update_query += "UPDATE Products_categoryattributesmapping SET " + temp_update_query +\
                        " WHERE id in (" + ",".join(map(lambda x: str(attr_data[col_data['Attribute Name']]['cat_data'][x]['cat_attr_id']),
                                         attr_data[col_data['Attribute Name']]['cat_data'].keys())) + ') !@#$'
            # Checking for sub-sub-category mapping
            cat_update_query = ""
            add_cat_attr_list = []
            delete_cat_attr_list = []
            for cat_name in cat_data_key:
                # Create and Update List
                if col_data[cat_name].find('Yes') != -1:
                    is_varing = 1 if col_data[cat_name].find('Yes V') !=-1 else 0
                    seq_val = col_data[cat_name].replace('Yes V', '') if col_data[cat_name].find('Yes V') !=-1 else 0
                    # Create new mapping
                    if db_cat_map[cat_name] not in attr_data[col_data['Attribute Name']]['cat_data'].keys():
                        add_cat_attr_list.append({'cat_id': db_cat_map[cat_name],
                                              'is_varing': is_varing,
                                              'sequence': seq_val})
                    # Update
                    else:
                        temp_update_query = ""
                        cat_attr_data = attr_data[col_data['Attribute Name']]['cat_data'][db_cat_map[cat_name]]
                        # Check if filter changed
                        if cat_attr_data['is_varing'] != is_varing:
                            temp_update_query += " is_varing = %s "%is_varing
                        if int(cat_attr_data['sequence']) != int(seq_val):
                            if len(temp_update_query):
                                temp_update_query += ','
                            temp_update_query += " sequence = %s "%seq_val
                        if len(temp_update_query):
                            update_query += "UPDATE Products_categoryattributesmapping SET " + temp_update_query +\
                                " WHERE id = %s"%cat_attr_data['cat_attr_id'] + " !@#$"
                else:
                    delete_cat_attr_list.append(db_cat_map[cat_name])
            delete_old_cat_attr_list = list(set(delete_cat_attr_list).intersection(set(attr_data[col_data['Attribute Name']]['cat_data'].keys())))
            print delete_old_cat_attr_list
            if (len(delete_old_cat_attr_list)):
                delete_attr_ids += map(lambda x: attr_data[col_data['Attribute Name']]['cat_data'][x]['cat_attr_id'], delete_old_cat_attr_list)
            # Creating New Category Attribute Mapping
            for cat_attr_data in add_cat_attr_list:
                insert_values += "(%s, %s, '%s', %s, %s, %s, %s),"%(cat_attr_data['cat_id'],
                    attr_data[col_data['Attribute Name']]['attr_id'],
                    attr_type_val, mandatory_val, spec_val, cat_attr_data['is_varing'], cat_attr_data['sequence'])

        if len(insert_values):
            insert_values = insert_values[:-1]
            create_query = "INSERT INTO Products_categoryattributesmapping (category_id, attribute_id, attr_type, is_mandatory, is_spec, is_varing, sequence) VALUES %s !@#$"%(insert_values)
        if len(delete_attr_ids):
            print "DELETE : ",delete_attr_ids
            delete_query = "UPDATE Products_categoryattributesmapping set status=0 where id in (%s) !@#$"%(",".join(map(lambda x: str(int(x)), delete_attr_ids)))
        print create_attr_query
        self.master_query = create_attr_query + update_cat_attr + create_query + update_query + delete_query
        print self.master_query
        return False

    def processdata(self, data_dict):
        self.data_dict = data_dict
        final_data = {}
        final_data = self.create_update_data()
        self.data_dict['data'] = final_data
        return self.data_dict
