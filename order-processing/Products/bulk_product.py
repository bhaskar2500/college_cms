from django.db import connection
from Products.models import *
import time
import json
import unicodedata
from Products.static_headers import display_name_db_column_mapping as COL_MAP
from django.db.models import Q

"""
Master Product Bulk Upload Class
"""
class MasterProduct():
    def __init__(self):
        self.download_data_query = '{}'
        self.mandatory_attr_headers = []  # to be added with subscribed product columns
        self.all_attr_list = []
        self.all_attr_dict = {}
        self.attr_categ_dict = {}
        self.master_category_name = ''
        self.sub_category = ''
        self.sub_sub_category = ''
        self.error_list = []  # contains row with error message prepended
        self.master_query = ''
        self.master_header_key = []
        self.header_key_excluded = []
        self.error_str = ''
        self.missing_columns = []

    def mandatory_attr_columns(self):
        """
        Checking for mandatory headers (columns)
        params: category id (category id against which the excel is uploaded)
                header_keys (column received from excel file)
        return:
            list of mandatory attributes
            dictionary with key: attribute name and value as attribute data
        """
        # getting master category id from first row
        categ_id = [None]
        master_categ_id = 0
        if self.data_dict['data']:
            if 'categoryids' in self.data_dict['data'][0] and \
                    self.data_dict['data'][0]['categoryids']:
                master_categ_id = int(str(self.data_dict['data'][0]['categoryids']).split(',')[0].replace('.0',''))
                categ_id.append(master_categ_id)
        self.master_category_id = master_categ_id
        print 'Master Category id: ', master_categ_id

        # getting sub category and sub sub category name of master category id
        display_categ = Category.objects.filter(level=4,category_id=master_categ_id).\
                values('category_name', 'parent_category_id__category_name')
        if display_categ:
            self.sub_sub_category = display_categ[0]['category_name']
            self.sub_category = display_categ[0]['parent_category_id__category_name']

        # getting attribute list for master category id
        attrs_list = CategoryAttributesMapping.objects.filter(\
            Q(Q(category_id=master_categ_id) | \
            Q(category__isnull=True)) & Q(status=True))
        if attrs_list:
            for attr in attrs_list:
                if attr.category:
                    self.master_category_name = attr.category.category_name
                # all attributes name list
                key_name = COL_MAP[attr.attribute.name.strip()] if attr.attribute.name.strip() in COL_MAP else attr.attribute.name.strip()
                self.all_attr_list.append(key_name.strip())

                # dictionary with key attribute name, value as attribute
                try:
                    key_name = str(key_name)
                except:
                    key_name = unicodedata.normalize('NFKD', key_name).encode('ascii','ignore')
                self.all_attr_dict.update({
                        str(key_name): attr.__dict__
                    })
                self.attr_categ_dict.update({
                        str(key_name): attr.__dict__
                    })

                # list of mandatory columns name
                if attr.is_mandatory:
                    self.mandatory_attr_headers.append(key_name.strip())

    def attr_value_constraint_check(self, key, data, data_dict):
        """
        Method to validate and convert data to their respective data
        type for a key and its data
        """
        errors = {}
        try:
            data = data.strip()
        except:
            pass

        if self.all_attr_dict[key]['is_varing']:
            if data == 'NA' or data == "":
                errors.update({key: '"' + key + '" is a varying column, value cannot be "NA" or blank'})
                return errors

        if data == 'NA' or data == "":
            del(data_dict[key])
            return 'skip_me'

        val_constraint = []
        if self.all_attr_dict[key]['value_constraint']:
            val_constraint = json.loads(self.all_attr_dict[key]['value_constraint'])
        attr_type = self.all_attr_dict[key]['attr_type']

        # special case for key features
        if key == 'key_features' and data:
            try:
                if data == 'XXX' and not key in self.mandatory_attr_headers:
                    data = "{}"
                elif not data == 'XXX':
                    data = self.format_key_features(data)
            except Exception, e:
                errors.update({ key: str(e) })

        # checking for XXX value and mandatory value check
        if data == 'XXX' and not key in self.mandatory_attr_headers:
            data = ''
        elif data == 'XXX':
            errors.update({key: key + ' is a mandatory field, XXX is given'})

        # checking for blank value and mandatory value check
        if data == '' and key in self.mandatory_attr_headers:
            errors.update({key: key + ' is a mandatory field, cannot be left blank'})

        if attr_type == 'text' and data:  # attr type is text
            # hack
            try:
                data = json.dumps(data.strip())
            except:
                pass

            try:
                data = str(float(data))
            except:
                data = str(data)
            # hack ends here

            try:
                data = json.dumps(data.strip())
            except Exception, e:
                errors.update({ key: str(e) })

        if attr_type == 'int' and not data == '':  # attr type is int
            try:
                data = str(int(data))
            except Exception, e:
                errors.update({key: 'Number required for "'+ key +'": ' + str(data)})

        if attr_type == 'float' and data:  # attr type is float
            try:
                data = str(float(data))
            except Exception, e:
                errors.update({key: str(e)})

        # checking for value constraint if no error is found in above conditions
        if not errors and val_constraint and not data in val_constraint:
            errors.update({key: str(e)})

        return errors

    def getBrands(self):
        """ get brands all brands with key as brand name and brand id as value """
        brands = Brand.objects.all().values('store_front_id', 'store_front_name')
        self.brands_dict = {
                b['store_front_name']: b['store_front_id'] for b in brands
            }

    def getProductCategory(self):
        """ to get dict with key as base_product_id and value as comma separated category_ids"""
        existing_categ = Category.objects.filter(level=4).values('category_id', 'category_name')
        self.existing_categ = map(lambda x: str(x['category_id']), existing_categ)

        self.categ_id_dict = {
            str(c['category_id']): c['category_name'] for c in existing_categ
        }

        cursor = connection.cursor()
        cursor.execute(""" select base_product_id,
                                  group_concat(category_id)
                           from product_category_mapping
                           group by base_product_id; """)
        categ_data = cursor.fetchall()
        self.prod_categ_map = {
               str(int(c[0])): c[1].split(',') for c in categ_data
            }

    def getallsubscribed_product(self, id_dict={}):
        """ method to get all subscribed product id along with base product """
        data_obj = SubscribedProduct.objects.\
            filter(base_product_id__in=id_dict['base_ids'],\
                 subscribed_product_id__in=id_dict['subs_ids']).\
            values('base_product_id', 'subscribed_product_id', 'specifications')
        self.subscribed_product_list = map(lambda x: str(x['base_product_id']) + '_' + str(x['subscribed_product_id']), data_obj)
        self.subscribed_ref_map = {
            str(x['subscribed_product_id']): json.loads(x['specifications']) if x['specifications'] else x['specifications'] for x in data_obj
        }

    def getallbase_product(self, id_list=[]):
        """ method to get all base product ids"""
        base_product_list = BaseProduct.objects.\
            filter(base_product_id__in=id_list).\
            values('base_product_id', 'base_ref_id','brand', 'brand_id', 'business_unit')
        print 'baseids =================>', id_list
        self.base_data_dict = {
            str(x['base_product_id']): x for x in base_product_list
        }
        self.base_product_list = map(lambda x: str(x['base_product_id']), base_product_list)
        self.base_ref_map = {
            str(x['base_product_id']): x['base_ref_id'] for x in base_product_list
        }

    def getproduct_column_name(self):
        fixed_column = CategoryAttributesMapping.objects.filter(category=None)

        self.base_column_list = [COL_MAP[c.attribute.name] if c.attribute.name in COL_MAP \
            else c.attribute.name for c in fixed_column if c.for_base == True]
        self.only_subscribed_columns = [COL_MAP[c.attribute.name] if c.attribute.name in COL_MAP \
            else c.attribute.name for c in fixed_column if c.for_subscribed == True]
        self.subscribed_column_list = list(set(self.all_attr_list) - set(self.base_column_list) - set(['variant_on']))
        self.subscribed_column_list.append('status')
        self.allowed_column_list = self.all_attr_list
        # appending attributes list for base + subscribed column list

    def mandatory_header_check(self, mandatory_headers):
        """ method to check for mandatory column """
        diff = list(set(mandatory_headers) - set(self.data_dict['header_keys']))
        if diff:
            self.master_header_key = []
            self.error_list = []
            self.header_key_excluded = []
            self.error_str = 'Mandatory Headers required : ' + (','.join(diff))
            return diff
        return None

    def mandatory_value_check(self, columns, value_dict):
        returnlist = []
        for key in columns:
            if not key in value_dict or not value_dict[key] or value_dict[key] == 'XXX':
                returnlist.append(key)
        return returnlist

    def extra_header_check(self):
        """method to get extra column which are not present in database """
        self.header_key_excluded = []
        print 'header keys', self.data_dict['header_keys']
        print '=============================================='
        print 'allowed column', self.allowed_column_list
        additional_column = list(set(self.data_dict['header_keys']) - set(self.allowed_column_list))
        if additional_column:
            extra_column = list(set(additional_column) - set(['row_no']))
            if extra_column:
                print 'column not found in database', extra_column
                # ignore and remove extra column from header keys received from file data

                self.data_dict['header_keys'] = self.master_header_key = \
                    [key for key in self.data_dict['header_keys'] if key not in extra_column]
                self.header_key_excluded += extra_column
        return self.header_key_excluded

    def format_key_features(self, data):
        if not data:
            return json.dumps([])
        data = data.split(';')
        temp_list = []
        for d in data:
            if not d:
                continue
            temp_list.append('"' + d + '": ""')
        return json.dumps('{' + ','.join(temp_list) + '}')

    def get_ids_not_in_db(self, data):
        """ method to get ids which are not found in database"""
        only_base_list = []  # contains base product ids
        combined_base_list = [] # contains only base ids  from combinedd_list
        combined_subscribed_list = [] # contains only subscribed ids from combined_list
        combined_list = [] #contains base + subscribed ids
        for d in data:
            if not d['base_product_id'] and not d['base_product_id'] == 'XXX':
                continue
            # hack for delete data
            if 'base_product_id' in d or d['base_product_id']:
                only_base_list.append(str(int(d['base_product_id'])))

            if not 'subscribed_product_id' in d or not d['subscribed_product_id']:
                only_base_list.append(str(int(d['base_product_id']))) # only base product update
            else:
                if not d['subscribed_product_id'] == 'XXX':
                    combined_base_list.append(str(int(d['base_product_id'])))
                    combined_subscribed_list.append(str(int(d['subscribed_product_id'])))
                    combined_list.append(str(int(d['base_product_id'])) + '_' + str(int(d['subscribed_product_id'])))

        # get base and subscribed ids from database (base and subscribed)
        self.getallbase_product(only_base_list)
        if combined_list:
            self.getallsubscribed_product({
                    'base_ids': combined_base_list,
                    'subs_ids': combined_subscribed_list
                })

        ignore_base_ids = [] # base ids which are not in database
        ignore_subscribed_product_ids = []  # subscribed id which are not in database

        if not only_base_list == self.base_product_list:
            ignore_base_ids = list(set(only_base_list) - set(self.base_product_list))

        if combined_list and not combined_list == self.subscribed_product_list:
            ignore_subscribed_product_ids = list(set(combined_list) - set(self.subscribed_product_list))

        return {
                'ignore_base_ids': ignore_base_ids,
                'ignore_subscribed_product_ids': ignore_subscribed_product_ids
            }

    def updatedata(self):
        """
        Update process steps:
        1. check for mandatory headers (base product id in update case)
        2. Search for extra headers and ignore them
            Each row validation
                check for base product id (mandatory)
                check for subscribed product id (not mandatory)
                check for categoryids ( id must be there in Category table)
        """
        update_query = ''  # final update query string
        product_categ_query = ''  # product category mapping update/insert query string

        # checking for mandatory headers
        return_dict = self.mandatory_header_check(['base_product_id', 'categoryids'])
        if return_dict:
            return False

        self.master_header_key = list(self.data_dict['header_keys'])
        self.header_key_excluded = self.extra_header_check();

        # getting base and subscribed ids which are not present in database
        ids_not_in_db = self.get_ids_not_in_db(self.data_dict['data'])

        download_query_data = {}  # dict containing updated base and subscribed ids
        updated_base_dict = {}
        master_attr_specs_data = []  # list for storing data to be update for specs attr table
        master_attr_filter_data = [] # list for storing data to be update for filter attr table
        i = 0

        print '================== Staring second looping into data'
        for d in self.data_dict['data']:  # looping on processes data received from excel file
            i += 1
            d.update({'row_no': i})
            temp = d.copy()

            # error handling for blank product id
            err_list = self.mandatory_value_check(['base_product_id'], temp)
            if err_list:
                temp.setdefault('errors', []).append({
                    'text': 'Base product id cannot be left blank or XXX',
                    'state': 'error',
                })
                self.error_list.append(temp)
                continue

            # converting base product id from float to string
            base_product_id = str(int(d['base_product_id']))

            # error handling for base product ids which are not in database
            if base_product_id in ids_not_in_db['ignore_base_ids']:
                temp.setdefault('errors', []).append({
                        'text': 'Base product id  '+ base_product_id + ' not found in database',
                        'state': 'error'
                    })
                self.error_list.append(temp)
                continue

            # checking for subscribed product id column in headers from file
            if 'subscribed_product_id' in d and d['subscribed_product_id']:
                # error handling for XXX in subscribed product id
                if str(d['subscribed_product_id']) == 'XXX':
                    temp.setdefault('errors', []).append({
                            'text': 'Subscribed id cannot be XXX',
                            'state': 'error'
                        })
                    self.error_list.append(temp)
                    continue

                # converting subscribed product id from float to string
                subscribed_product_id = str(int(d['subscribed_product_id']))

                # error handing for subscribed product id in combination with base that are not in database
                if (base_product_id + '_' + subscribed_product_id) in ids_not_in_db['ignore_subscribed_product_ids']:
                    temp.setdefault('errors', []).append({
                            'text': 'Subscribed product id: '+ subscribed_product_id +
                                ' not found in database for base product id: ' + base_product_id,
                            'state': 'error'
                        })
                    self.error_list.append(temp)
                    continue

            # updating a dict just to keep track of updating base products
            updated_base_dict.update({base_product_id: temp})

            # ======= PRODUCT_CATEGORY_MAPPING CHECK
            if 'categoryids' in d and d['categoryids'] == 'NA':
                temp.setdefault('errors', []).append({
                        'text': 'Category ID cannot be "NA"',
                        'state': 'error'
                    })
                self.error_list.append(temp)
                continue
            # checking for product category mapping
            if 'categoryids' in d and d['categoryids'] and not d['categoryids'] == 'XXX':   # category if not present of empty/blank
                insert_val_str = '), (' + base_product_id + ','
                categ_in_data = [str(int(float(c))) for c in str(d['categoryids']).split(',')]  # convert comma separated string into list

                # checking for category ids which are not present in database
                categ_not_found = list(set(categ_in_data) - set(self.existing_categ))
                if categ_not_found:  # if found then throw error
                    print 'Categories not found in database'
                    temp.setdefault('errors', []).append({
                            'text': 'Categories ids are not found in sub sub categories ["' + ('","'.join(categ_not_found)) + '"]',
                            'state': 'error'
                        })
                    self.error_list.append(temp)
                    continue  # do not proceed further if category ids not found and go to next iteration

                # checking if base product id present in existing product category mapping
                if base_product_id in self.prod_categ_map:

                    # getting category ids need to be removed
                    add_categ_id = list(set(categ_in_data) - set(self.prod_categ_map[base_product_id]))

                    # getting category ids need to be inserted
                    remove_categ_id = list(set(self.prod_categ_map[base_product_id]) - set(categ_in_data))

                    # creating query string for both delete and insert
                    if remove_categ_id:
                        product_categ_query += """DELETE FROM product_category_mapping
                            where base_product_id=%s and category_id in (%s) !@#$ """%(base_product_id, ','.join(remove_categ_id))
                    if add_categ_id:
                        product_categ_query += """INSERT INTO product_category_mapping
                            (base_product_id, category_id)
                            values%s !@#$ """%('(' + base_product_id + ',' + insert_val_str.join(add_categ_id)+ ')')

                # if base product id is not present in existing product category mapping
                else:
                    # insert category mapping for base product
                    product_categ_query += """INSERT INTO product_category_mapping
                        (base_product_id, category_id)
                        values%s !@#$ """%('(' + base_product_id + ',' + insert_val_str.join(categ_in_data)  + ')')

            # if category ids is XXX in data, then remove all mapping
            elif 'categoryids' in d and d['categoryids'] == 'XXX':
                product_categ_query += """DELETE FROM product_category_mapping where base_product_id=%s !@#$ """%(base_product_id)

            # ===== BRAND CHECK
            if 'brand' in d.keys() and not d['brand'] in self.brands_dict:
                temp.setdefault('errors', []).append({
                        'text': 'Brand "'+ d['brand'] +'" not found in database',
                        'state': 'error'
                    })
                self.error_list.append(temp)
                continue

            # checking for empty value for each column in a row
            base_update_data = [] # update base product value list
            subscribed_update_data = [] # update subscribed product value list
            attr_specs_data_dict= {} # dict key as attribute name, value
            attr_filter_data_dict = {} # dict key as attribute name, value

            each_error = []
            for key in self.data_dict['header_keys']:
                err = self.attr_value_constraint_check(key, d[key], d)
                if err == 'skip_me':
                    continue
                if err:
                    each_error.append('; '.join(err.values()))
                    continue

                # condition for Base Product only
                if not 'subscribed_product_id' in d or not d['subscribed_product_id']:
                    if key in self.base_column_list:
                        if not key in ['base_product_id'] and not d[key] == "":
                            # for all keys except base_product_id
                            base_update_data.append(key + "='" + str(d[key]) + "'")
                            if key == 'brand':  # updating brand_id for the given base
                                base_update_data.append("brand_id='" + str(self.brands_dict[str(d[key])]) + "'")

                # condition for Subscribed Product only
                elif d['subscribed_product_id']:
                    if key in self.subscribed_column_list:
                        # checking for specification
                        if self.all_attr_dict[key]['is_spec']:
                            attr_specs_data_dict.update({key: d[key]})

                        # checking for filters
                        if self.all_attr_dict[key]['is_filter']:
                            attr_filter_data_dict.update({key: d[key]})

                        if not key in ['subscribed_product_id', 'base_product_id'] and key in self.only_subscribed_columns:
                            subscribed_update_data.append(key + "='" + str(d[key]) + "'")
            if each_error:
                temp.setdefault('errors', []).append({
                    'text': ' || '.join(each_error),
                    'state': 'error'
                })
                self.error_list.append(temp)
                continue

            if base_update_data:
                # creating base update query
                download_query_data.setdefault('base_product_id', []).append(base_product_id)
                update_query += """UPDATE base_product set %s \
                    where base_product_id=%s !@#$"""%((','.join(base_update_data)), base_product_id)

            if subscribed_update_data:
                # creating subscribed update query

                rd = self.ProductAttributeUpdateQuery(attr_specs_data_dict, attr_filter_data_dict,\
                     subscribed_product_id, base_product_id)
                if rd['specification_json']:
                    subscribed_update_data.append("specifications=" + json.dumps(rd['specification_json']))

                if rd['prod_attr_data']:
                    master_attr_specs_data += rd['prod_attr_data']

                if rd['prod_attr_filter_data']:
                    master_attr_filter_data += rd['prod_attr_filter_data']

                download_query_data.setdefault('subscribed_product_id', []).append(subscribed_product_id)

                update_query += """UPDATE subscribed_product set %s \
                    where base_product_id=%s and subscribed_product_id=%s !@#$\
                    """%((','.join(subscribed_update_data)), base_product_id, subscribed_product_id)

            if 'errors' in temp.keys():
                self.error_list.append(temp)

        if master_attr_specs_data:
            update_list = ['text_value','int_value','decimal_value']
            update_str = [c +'=values('+ c + ')' for c in update_list]
            prod_attr_specs_query = """INSERT INTO Products_productcategoryattributesmapping \
                (subscribed_product_id,category_attribute_id,text_value,int_value,decimal_value) \
                VALUES %s ON DUPLICATE KEY UPDATE %s !@#$"""%(",".join(master_attr_specs_data), ','.join(update_str))
            update_query += prod_attr_specs_query

        if master_attr_filter_data:
            update_list = ['text_value','int_value','decimal_value']
            update_str = [c +'=values('+ c + ')' for c in update_list]
            prod_attr_filter_query = """INSERT INTO Products_productcategoryattributesmappingfilters \
                (base_product_id,subscribed_product_id,category_attribute_id,text_value,int_value,decimal_value) \
                VALUES %s ON DUPLICATE KEY UPDATE %s !@#$"""%(",".join(master_attr_filter_data), ','.join(update_str))
            update_query += prod_attr_filter_query

        if download_query_data:
            self.download_data_query = json.dumps(download_query_data)

        print 'Download query data', download_query_data
        self.master_query = update_query + product_categ_query

    def createdata(self):
        """
        Create process steps:
        1. check for mandatory headers
           base product headers must be present
        2. Search for extra headers and ignore them
            Each row validation
                check for brand (brand must exist in database)
                check for categoryids ( id must be there in Category table)
        """
        insert_query = ''  # final update query string
        product_categ_query = ''  # product category mapping update/insert query string

        # adding base_ref_id column in mandatory header, all columns, all column dict
        self.mandatory_attr_headers.append('base_ref_id')
        self.allowed_column_list.append('base_ref_id')
        self.base_column_list.append('base_ref_id')
        self.all_attr_dict.update({
                'base_ref_id': {
                    'value_constraint': '[]',
                    'attr_type': 'text',
                    'is_mandatory': True
                }
            })

        # checking for mandatory headers
        return_dict = self.mandatory_header_check(list(set(self.mandatory_attr_headers)\
             - set(['base_product_id', 'subscribed_product_id'])))
         # all mandatory headers except base and subscribed ids
        if return_dict:
            self.return_data = return_dict
            return False

        self.master_header_key = list(self.data_dict['header_keys'])
        self.header_key_excluded = self.extra_header_check();

        # checking for base product id and subscribed product id column in header keys
        remove_headers = list(set(['base_product_id','subscribed_product_id']) - set(self.master_header_key))
        # show error to remove these column from excel file
        if not remove_headers:
            self.header_key_excluded += remove_headers

        download_query_data = {}
        new_base_dict = {}  # with key base_ref_id and file_id (unique)
        i = 0
        master_attr_specs_data = []
        master_attr_filter_data = []
        self.missing_columns = list(set(self.allowed_column_list) - set(self.data_dict['header_keys']))
        for d in self.data_dict['data']:  # looping on processes data received from excel file
            i += 1
            d.update({'row_no': i})
            temp = d.copy()

            # error handling for blank ref id
            if not d['base_ref_id']:
                temp.setdefault('errors', []).append({
                    'text': 'Base ref id cannot be left blank',
                    'state': 'error',
                })
                self.error_list.append(temp)
                continue

            # error handling for XXX in base ref id
            if d['base_ref_id'] == 'XXX':
                temp.setdefault('errors', []).append({
                        'text': 'Base ref id  cannot be XXX',
                        'state': 'error'
                    })
                self.error_list.append(temp)
                continue

            # converting base ref id from float to string
            base_ref_id = str(int(d['base_ref_id']))
            master_ref_id = base_ref_id + '_' + self.data_dict['file_id']
            mvc_list = [] # list of those column whose values are mandatory

            # ===== BRAND CHECK
            # checking for brand
            if not master_ref_id in new_base_dict and 'brand' in d and d['brand']:
               if not d['brand'] in self.brands_dict:
                    temp.setdefault('errors', []).append({
                        'text': 'Brand "'+ d['brand'] +'" not found in database',
                        'state': 'error'
                    })
                    self.error_list.append(temp)
                    continue

            # adding query_created to row for the first time for each base product
            if not master_ref_id in new_base_dict:
                print 'creating master_ref_id in base dict ===============>', master_ref_id
                temp.update({'query_created': False})
                new_base_dict.update({ master_ref_id: temp})

            # ======= CATEGORY CHECK
            if 'categoryids' in d and d['categoryids'] == 'NA':
                temp.setdefault('errors', []).append({
                        'text': 'Category ID cannot be "NA"',
                        'state': 'error'
                    })
                self.error_list.append(temp)
                continue
            # checking for product category mapping
            if 'categoryids' in d and d['categoryids'] and not d['categoryids'] == 'XXX':   # category if not present of empty/blank
                #insert_val_str = '), (' + base_ref_id + ','
                categ_in_data = [str(int(float(c))) for c in str(d['categoryids']).split(',')]  # convert comma separated string into list

                # checking for category ids which are not present in database
                categ_not_found = list(set(categ_in_data) - set(self.existing_categ))
                if categ_not_found:  # if found then throw error
                    temp.setdefault('errors', []).append({
                            'text': 'Categories ids are not found in sub sub categories ["' + ('","'.join(categ_not_found)) + '"]',
                            'state': 'error'
                        })
                    self.error_list.append(temp)
                    continue  # do not proceed further if category ids not found and go to next iteration

                # creating insert base product - category mapping query
                for c in categ_in_data:
                    product_categ_query += """INSERT INTO product_category_mapping (base_ref_id,base_product_id,category_id) %s !@#$ """%(\
                        '(' + 'select base_ref_id,base_product_id,"'+ c +'" as category_id from base_product where base_ref_id="' +\
                         master_ref_id + '")')

            # ==== EMPTY VALUE CHECK
            #checking for empty value for each column in a row
            base_insert_cols = []
            base_insert_data = [] # update base product value list
            subscribed_insert_cols = []
            subscribed_insert_data = [] # update subscribed product value list

            attr_specs_data_dict= {}
            attr_filter_data_dict = {}
            each_error = []
            for key in self.data_dict['header_keys']:
                err = self.attr_value_constraint_check(key, d[key], d)
                if err == 'skip_me':
                    continue
                if err:
                    each_error.append('; '.join(err.values()))
                    continue

               # condition for base product
                if key in self.base_column_list and d[key] and master_ref_id in new_base_dict and\
                        not new_base_dict[master_ref_id]['query_created']:

                    if key == 'brand' and d['brand']:
                        base_insert_cols.append('brand,brand_id')
                        base_insert_data.append(d['brand'])
                        new_base_dict[master_ref_id].update({'brand_id': self.brands_dict[str(d[key])]})
                        base_insert_data.append(str(self.brands_dict[str(d[key])]))
                        continue

                    base_insert_cols.append(key)
                    if key == 'base_ref_id':
                        base_insert_data.append(master_ref_id)
                    else:
                        base_insert_data.append(str(d[key]))

                # condition for subscribed product
                if key in self.subscribed_column_list and d[key]:
                    # checking for specification
                    if self.all_attr_dict[key]['is_spec']:
                        attr_specs_data_dict.update({key: d[key]})

                    # checking for filters
                    if self.all_attr_dict[key]['is_filter']:
                        attr_filter_data_dict.update({key: d[key]})

                    if not key == 'base_ref_id' and key in self.only_subscribed_columns:
                        subscribed_insert_cols.append(key)
                        subscribed_insert_data.append("'" + str(d[key]) + "' as " + key )

            if each_error:
                temp.setdefault('errors', []).append({
                    'text': '\n'.join(each_error),
                    'state': 'error'
                })
                self.error_list.append(temp)
                continue

            if base_insert_data:
                new_base_dict[master_ref_id].update({'query_created': True})
                special_data = []
                special_str = ''

                download_query_data.setdefault('base_ref_id', []).append(master_ref_id)
                insert_query += """INSERT INTO base_product (%s) VALUES(%s) !@#$ """%(\
                         (",".join(base_insert_cols)),\
                         ("'" + "','".join(base_insert_data) + "'" + \
                         special_str))

            if subscribed_insert_data:
                # syncing data from base to subscribed
                subscribed_ref_id = master_ref_id +'_'+ str(i)

                if not 'sku' in subscribed_insert_cols:
                    subscribed_insert_cols.append('sku')
                    skucode = str(new_base_dict[master_ref_id]['brand'][:2]).upper() + \
                        str(self.brands_dict[new_base_dict[master_ref_id]['brand_id']]) + \
                        str(self.master_category_name[:2]).upper() + \
                        str(self.master_category_id)
                    skucode += str(int(time.time() + i))[(len(skucode) - 16):]

                    subscribed_insert_data.append("'" + skucode + "' as sku")

                rd = self.ProductAttributeInsertQuery(attr_specs_data_dict, attr_filter_data_dict, subscribed_ref_id)
                if rd['specification_json']:
                    subscribed_insert_cols.append('specifications')
                    subscribed_insert_data.append(rd['specification_json'])

                if rd['prod_attr_data']:
                    master_attr_specs_data += rd['prod_attr_data']

                if rd['prod_attr_filter_data']:
                    master_attr_filter_data += rd['prod_attr_filter_data']

                download_query_data.setdefault('subscribed_ref_id', []).append(master_ref_id +'_'+ str(i))

                insert_query += """INSERT INTO subscribed_product (base_ref_id,subscribed_ref_id,base_product_id,%s) %s !@#$"""%(\
                    ','.join(subscribed_insert_cols), \
                    'select "'+ master_ref_id +'" as base_ref_id, "'+ \
                        master_ref_id +'_'+ str(i) +'" as subscribed_ref_id, \
                        base_product_id,'+ (','.join(subscribed_insert_data)) +\
                        ' from base_product where base_ref_id="' + master_ref_id + '"')

        if master_attr_specs_data:
            prod_attr_specs_query = """INSERT INTO Products_productcategoryattributesmapping \
                (subscribed_ref_id,category_attribute_id,text_value,int_value,decimal_value) \
                VALUES %s !@#$"""%(",".join(master_attr_specs_data))

            insert_query += prod_attr_specs_query
            update_prod_attr_specs_query = """UPDATE Products_productcategoryattributesmapping as PCAM\
                JOIN subscribed_product as SP ON SP.subscribed_ref_id = PCAM.subscribed_ref_id
                set PCAM.subscribed_product_id=SP.subscribed_product_id \
                where PCAM.subscribed_product_id IS NULL !@#$"""
            insert_query += update_prod_attr_specs_query

        #  creating insert query for filters in attributes
        if master_attr_filter_data:
            prod_attr_specs_query = """INSERT INTO Products_productcategoryattributesmappingfilters \
                (subscribed_ref_id,category_attribute_id,text_value,int_value,decimal_value) \
                VALUES %s !@#$"""%(",".join(master_attr_filter_data))

            insert_query += prod_attr_specs_query
            update_prod_attr_specs_query = """UPDATE Products_productcategoryattributesmappingfilters as PCAMF\
                JOIN subscribed_product as SP ON SP.subscribed_ref_id = PCAMF.subscribed_ref_id
                set PCAMF.base_product_id=SP.base_product_id, PCAMF.subscribed_product_id=SP.subscribed_product_id \
                where PCAMF.subscribed_product_id IS NULL"""
            insert_query += update_prod_attr_specs_query

        if download_query_data:
            self.download_data_query = json.dumps(download_query_data)
        print 'Download data ref ids: ', download_query_data
        self.master_query = insert_query + product_categ_query

    def adddata(self):
        """
        add subscribed process steps:
        1. check for mandatory headers
           base_product_id, variant_on headers must be present
           subscribed_product_id column should not be there
        2. Search for extra headers and ignore them
        3. Search for base product id which are not present in database
            Each row validation
                variant cannot be blank
                variant can either be a string of 'NA' i.e. single product for a base
        """
        insert_query = ''  # final update query string

        self.mandatory_attr_headers = list(set(self.mandatory_attr_headers) - set('subscribed_product_id'))
        self.allowed_column_list = list(set(self.allowed_column_list) - set('subscribed_product_id'))
        self.subscribed_column_list = list(set(self.subscribed_column_list) - set(['subscribed_product_id']))
        # checking for mandatory headers
        return_dict = self.mandatory_header_check(['base_product_id'] + self.subscribed_column_list)
        #self.subscribed_column_list.append('subscribed_product_id')
        if return_dict:
            return False

        self.master_header_key = list(self.data_dict['header_keys'])
        self.header_key_excluded = self.extra_header_check();

        # checking for base product id and subscribed product id column in header keys
        remove_headers = list(set(['subscribed_product_id']) - set(self.master_header_key))
        # show error to remove these column from excel file
        if not remove_headers:
            self.header_key_excluded += remove_headers

        # getting base ids which are not present in database
        ids_not_in_db = self.get_ids_not_in_db(self.data_dict['data'])
        new_base_dict = {}
        download_query_data = {}
        new_subscribed_dict = {}  # with key base_ref_id and file_id (unique)
        master_attr_specs_data = []
        master_attr_filter_data = []
        self.missing_columns = list(set(self.subscribed_column_list) - set(self.data_dict['header_keys']))
        print 'Missing ---->', self.missing_columns
        i = 0
        for d in self.data_dict['data']:  # looping on processes data received from excel file
            i += 1
            d.update({'row_no': i})
            temp = d.copy()

            # error handling for blank ref id
            if not d['base_product_id']:
                temp.setdefault('errors', []).append({
                    'text': 'Base product id cannot be left blank',
                    'state': 'error',
                })
                self.error_list.append(temp)
                continue

            # converting base ref id from float to string
            base_product_id = str(int(d['base_product_id']))
            master_ref_id = base_product_id

            # error handling for base product ids which are not in database
            if base_product_id in ids_not_in_db['ignore_base_ids']:
                temp.setdefault('errors', []).append({
                        'text': 'Base product id: '+ base_product_id + ' not found in database',
                        'state': 'error'
                    })
                self.error_list.append(temp)
                continue

            # creating insert query for new subscribed products
            subscribed_insert_cols = [] # insert column name list
            subscribed_insert_data = [] # insert value list
            counter = 0
            attr_specs_data_dict = {}
            attr_filter_data_dict = {}
            each_error = []

            for key in self.data_dict['header_keys']:
                counter += 1
                err = self.attr_value_constraint_check(key, d[key], d)
                if err == 'skip_me':
                    continue
                if err:
                    each_error.append('; '.join(err.values()))
                    continue

                if key in self.subscribed_column_list and len(str(d[key])):
                    # checking for specification
                    if self.all_attr_dict[key]['is_spec']:
                        attr_specs_data_dict.update({key: d[key]})

                    # checking for filters
                    if self.all_attr_dict[key]['is_filter']:
                        attr_filter_data_dict.update({key: d[key]})

                    if key in self.only_subscribed_columns:
                        subscribed_insert_cols.append(key)
                        subscribed_insert_data.append("'" + str(d[key]) + "'")

            if each_error:
                temp.setdefault('errors', []).append({
                    'text': '\n'.join(each_error),
                    'state': 'error'
                })
                self.error_list.append(temp)
                continue

            if subscribed_insert_data:
                subscribed_ref_id = str(base_product_id) + '_'+ self.data_dict['file_id'] + '_' + str(i)
                if not 'base_product_id' in subscribed_insert_cols:
                    subscribed_insert_cols.append('base_product_id')
                    subscribed_insert_data.append(base_product_id)
                if not 'base_ref_id' in subscribed_insert_cols:
                    if base_product_id in self.base_ref_map:
                        subscribed_insert_cols.append('base_ref_id')
                        subscribed_insert_data.append("'" + (str(self.base_ref_map[base_product_id]) or base_product_id) + "'")
                if not 'subscribed_ref_id' in subscribed_insert_cols:
                    if base_product_id in self.base_ref_map:
                        download_query_data.setdefault('subscribed_ref_id', []).append(subscribed_ref_id)
                        subscribed_insert_cols.append('subscribed_ref_id')
                        subscribed_insert_data.append("'" + subscribed_ref_id + "'")

                if not 'sku' in subscribed_insert_cols:
                    subscribed_insert_cols.append('sku')
                    self.master_category_id = self.prod_categ_map[base_product_id][0]
                    self.master_category_name = str(self.categ_id_dict[self.master_category_id])
                    skucode = str(self.base_data_dict[base_product_id]['brand'][:2]).upper() + \
                        str(self.base_data_dict[base_product_id]['brand_id']) + \
                        str(self.master_category_name[:2]).upper() + \
                        str(self.master_category_id)
                    skucode += str(int(time.time() + i))[(len(skucode) - 16):]

                    subscribed_insert_data.append("'" + skucode + "'")

                rd = self.ProductAttributeInsertQuery(attr_specs_data_dict, attr_filter_data_dict, subscribed_ref_id)
                if rd['specification_json']:
                    subscribed_insert_cols.append('specifications')
                    subscribed_insert_data.append(rd['specification_json'])

                if rd['prod_attr_data']:
                    master_attr_specs_data += rd['prod_attr_data']

                if rd['prod_attr_filter_data']:
                    master_attr_filter_data += rd['prod_attr_filter_data']

                insert_query += """INSERT INTO subscribed_product (%s) VALUES(%s) !@#$ """%(\
                    ','.join(subscribed_insert_cols), ','.join(subscribed_insert_data))

        #  creating insert query for all attributes
        if master_attr_specs_data:
            prod_attr_specs_query = """INSERT INTO Products_productcategoryattributesmapping \
                (subscribed_ref_id,category_attribute_id,text_value,int_value,decimal_value) \
                VALUES %s !@#$"""%(",".join(master_attr_specs_data))

            insert_query += prod_attr_specs_query
            update_prod_attr_specs_query = """UPDATE Products_productcategoryattributesmapping as PCAM\
                JOIN subscribed_product as SP ON SP.subscribed_ref_id = PCAM.subscribed_ref_id
                set PCAM.subscribed_product_id=SP.subscribed_product_id \
                where PCAM.subscribed_product_id IS NULL !@#$"""
            insert_query += update_prod_attr_specs_query

        #  creating insert query for filters in attributes
        if master_attr_filter_data:
            prod_attr_filter_query = """INSERT INTO Products_productcategoryattributesmappingfilters \
                (subscribed_ref_id,category_attribute_id,text_value,int_value,decimal_value) \
                VALUES %s !@#$"""%(",".join(master_attr_filter_data))

            insert_query += prod_attr_filter_query
            update_prod_attr_filter_query = """UPDATE Products_productcategoryattributesmappingfilters as PCAMF\
                JOIN subscribed_product as SP ON SP.subscribed_ref_id = PCAMF.subscribed_ref_id
                set PCAMF.base_product_id=SP.base_product_id, PCAMF.subscribed_product_id=SP.subscribed_product_id \
                where PCAMF.subscribed_product_id IS NULL !@#$"""
            insert_query += update_prod_attr_filter_query

        if download_query_data:
            self.download_data_query = json.dumps(download_query_data)
        print self.download_data_query
        self.master_query = insert_query

    def ProductAttributeInsertQuery(self, data_dict, filter_data_dict, subscribed_ref_id):
        specs_str = ''
        insert_data_list = []
        filter_data_list = []
        if data_dict:
            # collecing specification into a dictionary to be stored in 'specification' column
            specs_str_list = []
            insert_cols = ['subscribed_ref_id','category_attribute_id','text_value','int_value','decimal_value']
            update_data = []
            for k, v in data_dict.items():
                specs_str_list.append('"' + k + '": "' + str(v) + '"')
                categ_attr_id = self.attr_categ_dict[k]['id']
                attr_type = self.attr_categ_dict[k]['attr_type']
                insert_data = ['"' + subscribed_ref_id + '"', str(categ_attr_id), '""','""','""']
                # updating data according to attribute type
                attr_type = 'text' if attr_type == 'dropdown' else attr_type  # hack for dropdown
                if attr_type == 'text':
                    v = json.dumps(str(v))
                insert_data[insert_cols.index(attr_type + '_value')] = v
                insert_data_list.append("(" + ",".join(insert_data) + ")")
        if filter_data_dict:
            insert_cols = ['base_product_id','subscribed_product_id','category_attribute_id',\
                'text_value','int_value','decimal_value']
            for k, v in filter_data_dict.items():
                categ_attr_id = self.attr_categ_dict[k]['id']
                attr_type = self.attr_categ_dict[k]['attr_type']
                insert_data = ['"' + subscribed_ref_id + '"', str(categ_attr_id), '""','""','""']
                # updating data according to attribute type
                attr_type = 'text' if attr_type == 'dropdown' else attr_type  # hack for dropdown
                if attr_type == 'text':
                    v = json.dumps(str(v))
                insert_data[insert_cols.index(attr_type + '_value')] = v
                filter_data_list.append("(" + ",".join(insert_data) + ")")

        specs_str = json.dumps('{' + ",".join(specs_str_list) + '}')

        return {
                'specification_json': specs_str,
                'prod_attr_data': insert_data_list,
                'prod_attr_filter_data': filter_data_list
            }

    def ProductAttributeUpdateQuery(self, data_dict, filter_data_dict, subscribed_product_id, base_product_id):
        specifications = {}
        insert_data_list = []
        filter_data_list = []

        if data_dict:
            # collecing specification into a dictionary to be stored in 'specification' column
            insert_cols = ['subscribed_product_id','category_attribute_id',\
                'text_value','int_value','decimal_value']
            specifications = self.subscribed_ref_map.copy()
            specifications.update(data_dict)

            for k, v in data_dict.items():
                categ_attr_id = self.attr_categ_dict[k]['id']
                attr_type = self.attr_categ_dict[k]['attr_type']
                insert_data = [subscribed_product_id, str(categ_attr_id), '""','""','""']
                # updating data according to attribute type
                attr_type = 'text' if attr_type == 'dropdown' else attr_type  # hack for dropdown
                if attr_type == 'text':
                    v = json.dumps(str(v))
                insert_data[insert_cols.index(attr_type + '_value')] = v
                insert_data_list.append("(" + ",".join(insert_data) + ")")
        if filter_data_dict:
            insert_cols = ['base_product_id','subscribed_product_id','category_attribute_id',\
                'text_value','int_value','decimal_value']

            for k, v in filter_data_dict.items():
                categ_attr_id = self.attr_categ_dict[k]['id']
                attr_type = self.attr_categ_dict[k]['attr_type']
                insert_data = [base_product_id, subscribed_product_id, str(categ_attr_id), '""','""','""']
                # updating data according to attribute type
                attr_type = 'text' if attr_type == 'dropdown' else attr_type  # hack for dropdown
                if attr_type == 'text':
                    v = json.dumps(v)
                insert_data[insert_cols.index(attr_type + '_value')] = v
                filter_data_list.append("(" + ",".join(insert_data) + ")")

        return {
                'specification_json': json.dumps(specifications),
                'prod_attr_data': insert_data_list,
                'prod_attr_filter_data': filter_data_list
            }

    def processdata(self, data_dict):
        self.data_dict = data_dict
        self.mandatory_attr_columns()
        self.getBrands()
        self.getProductCategory()
        self.getproduct_column_name()

        if data_dict['process_type'] == 'create':
            self.createdata()
        elif data_dict['process_type'] == 'update':
            self.updatedata()
        elif data_dict['process_type'] == 'add':
            self.adddata()

        self.master_header_key.insert(0, 'errors')
        self.master_header_key.insert(0, 'row_no')

        # converting db column name to attribute name
        if self.header_key_excluded:
            COL_MAP_REV = {v: k for k, v in COL_MAP.items()}
            for i in range(len(self.header_key_excluded)):
                if self.header_key_excluded[i] in COL_MAP_REV:
                    self.header_key_excluded[i] = COL_MAP_REV[self.header_key_excluded[i]]

        self.return_data = {
                'table_header': self.master_header_key,
                'table_data': self.error_list,
                'stats': {
                        'error': self.error_str,
                        'extra_headers': self.header_key_excluded,
                        'missing_headers': self.missing_columns,
                        'error_count': len(self.error_list),
                        'success_count': abs(len(self.data_dict['data']) - len(self.error_list))
                    }
            }
        return self.data_dict
