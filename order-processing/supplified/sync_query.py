from supplified.models import MasterImportUpload
from Products.models import *
from django.db import connection
import json

class CreateSync():
    def __init__(self, file_id):
        self.upload_obj = MasterImportUpload.objects.get(id=file_id)
        self.data_dict = json.loads(self.upload_obj.download_query)
        base_products = []
        subscribed_products = []
        master_query = []
        self.cursor = connection.cursor()
        self.json_columns = ['size', 'title', 'description', 'length', 'height', 'width', 'specifications', 'key_features']
        if self.upload_obj.master_category_id:
            self.json_columns = CategoryAttributesMapping.objects.filter(category_id=None,\
                 attr_type="text").values_list('attribute__name', flat=True)

    def get_column_names(self, table_name):
        self.cursor.execute('SHOW COLUMNS FROM %s'%(table_name))
        return [str(c[0]) for c in self.cursor.fetchall()]

    def get_table_values(self, column_names, filters, table_name):
        self.cursor.execute('SELECT %s FROM %s %s'%(','.join(column_names), table_name, filters))
        return self.cursor.fetchall()

    def create_query(self, column_names, each_values_list, table_name):
        each_update_list = []
        new_each_values_list = []
        for i in range(len(each_values_list)):
            val = each_values_list[i] or ''
            if not column_names[i] in self.json_columns:
                try:
                    each_update_list.append(column_names[i] + '="' + str(float(val)) + '"')
                    new_each_values_list.append('"' + str(float(val)) + '"')
                except Exception, e:
                    each_update_list.append(column_names[i] + '="' + str(val) + '"')
                    new_each_values_list.append('"' + str(val) + '"')
            else:
                try:
                    each_update_list.append(column_names[i] + '=' + json.dumps(val))
                    new_each_values_list.append(json.dumps(val))
                except Exception, e:
                    each_update_list.append(column_names[i] + '=' + str(val))
                    new_each_values_list.append(str(val))

        query = """INSERT INTO %s (%s) values(%s) ON DUPLICATE KEY UPDATE %s"""%(\
                     table_name,\
                     ','.join(column_names),\
                     ','.join(new_each_values_list),\
                     ','.join(each_update_list))
        return query

    def create_bulk_sync_query(self, **kwargs):
        bulk_query = []
        filter_str = 'where ' + ' and '.join(kwargs['filter_list'])
        columns = self.get_column_names(kwargs['table_name'])
        data = self.get_table_values(columns, filter_str, kwargs['table_name'])
        if data:
            if 'delete_all_flag' in kwargs and kwargs['delete_all_flag']:
                bulk_query.append('DELETE FROM %s %s'%(kwargs['table_name'], filter_str))
            for each_values_list in data:
                bulk_query.append(self.create_query(columns, each_values_list, kwargs['table_name']))
        return bulk_query
