from django.shortcuts import render_to_response
from django.http import HttpResponse
from xlrd import open_workbook
import json
import datetime
from settings import BASE_DIR, PROCESS_CLASSES
import importlib
from django.template import RequestContext
from supplified.models import MasterImportUpload
from django.db import connection, connections
import os, sys, traceback
import time
from django.db.models import Q
from Products.models import *
from supplified.sync_query import CreateSync
from Products.views import get_master_product
from xlsxwriter import Workbook
import StringIO
import unicodedata
from settings import BASE_PATH
from Products.static_headers import display_name_db_column_mapping as COL_MAP

def change_log_page(request):
    return render_to_response('')

def dynamic_import(name):
    """ Method to import class dynamically """
    module_name, class_name = name.rsplit(".", 1)
    mod = getattr(importlib.import_module(module_name), class_name)
    return mod

def handle_uploaded_file(upload_dir, f, file_name):
    file_path = os.getcwd() + '/static/%s/'%upload_dir
    if not os.path.exists(os.path.dirname(file_path + file_name)):
	os.makedirs(os.path.dirname(file_path + file_name))
    with open(file_path + file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload(request):
    process_name = request.POST['process_name'] if 'process_name' in request.POST else None
    process_type = request.POST['process_type'] if 'process_type' in request.POST else None  # create/update
    ref_text = request.POST['ref_text'] if 'ref_text' in request.POST else ''
    excel_file = request.FILES['excel_file'] if 'excel_file' in request.FILES else None
    cur_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y-%H-%M-%S')
    file_name = excel_file.name

    # renaming file with datetime
    file_name = file_name.split('.')
    file_ext = file_name.pop(-1)
    file_name = '_'.join(file_name) + '_' + datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%y_%H-%M-%S') + '.' + file_ext
    print 'Uploading file ======>', file_name
    if not file_name.split('.')[-1] in ['xls', 'xlsx']:
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'File type must be .xls or .xlsx',
        }))

    # save file in /static/uploads director
    returned_data = {}
    file_path = 'upload_%s/%s/%s'%(process_name.lower().replace(' ','_'), process_type, datetime.datetime.now().strftime('%d-%m-%y'))
    try:
        handle_uploaded_file(file_path, excel_file, file_name);
        new_upload = MasterImportUpload(**{
            'file_name': file_name,
            'ref_text': ref_text,
            'process_name': process_name,
            'process_type': process_type,
            'user': request.user,
            'uploaded_on': datetime.datetime.now(),
            'file_path': '/static/%s/'%file_path
        })
        new_upload.save()
        returned_data.update({
                'process_name': process_name,
                'process_type': process_type,
                'file_name': file_name,
                'file_id': new_upload.id
            })
    except Exception, e:
        print 'Upload error ===========>', str(e)
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'Error while uploading file' + str(e)
        }))
    return HttpResponse(json.dumps({
            'status_code': 200,
            'status_msg': 'Success',
            'data': returned_data
        }))

def upload_zip(request):
    process_name = request.POST['process_name'] if 'process_name' in request.POST else None
    process_type = request.POST['process_type'] if 'process_type' in request.POST else None  # create/update
    ref_text = request.POST['ref_text'] if 'ref_text' in request.POST else ''
    zip_file = request.FILES['zip_file'] if 'zip_file' in request.FILES else None
    cur_datetime = datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%Y-%H-%M-%S')
    file_name = zip_file.name
    # renaming file with datetime
    file_name = file_name.split('.')
    file_ext = file_name.pop(-1)
    file_name = '_'.join(file_name) + '_' + datetime.datetime.strftime(datetime.datetime.now(), '%d-%m-%y_%H-%M-%S') + '.' + file_ext
    print 'Uploading file ======>', file_name

    if not file_name.split('.')[-1] == 'zip':
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'File type must be .zip',
        }))

    # save file in /static/uploads director
    returned_data = {}
    file_path = 'upload_%s/%s/%s'%(process_name.lower().replace(' ','_'), process_type, datetime.datetime.now().strftime('%d-%m-%y'))
    try:
        handle_uploaded_file(file_path, zip_file, file_name);
        new_upload = MasterImportUpload(**{
            'file_name': file_name,
            'ref_text': ref_text,
            'process_name': process_name,
            'process_type': process_type,
            'user': request.user,
            'uploaded_on': datetime.datetime.now(),
            'file_path': '/static/%s/'%file_path
        })
        new_upload.save()
        returned_data.update({
                'process_name': process_name,
                'process_type': process_type,
                'file_name': file_name,
                'file_id': new_upload.id
            })
    except Exception, e:
        print 'Upload error ===========>', str(e)
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'Error while uploading file' + str(e)
        }))
    return HttpResponse(json.dumps({
            'status_code': 200,
            'status_msg': 'Success',
            'data': returned_data
        }))

def process(request):
    """
    Method to fetch excel file location using file_id in MaterImportUpload and processing
    the error validation on file received
    """
    #try:
    if True:
        file_id = request.POST['file_id'] if 'file_name' in request.POST else None

        upload_obj = MasterImportUpload.objects.get(id=file_id)
        file_name = upload_obj.file_name
        process_name = upload_obj.process_name
        process_type = upload_obj.process_type
        file_path = upload_obj.file_path
        print str(file_path) + file_name
        try:
            book = open_workbook(os.getcwd() + str(file_path) + file_name)
            sheet = book.sheet_by_index(0) # selecting the first sheet in file
        except AssertionError:
		    _, _, tb = sys.exc_info()
		    traceback.print_tb(tb) # Fixed format
		    tb_info = traceback.extract_tb(tb)
		    filename, line, func, text = tb_info[-1]
		    print('An error occurred on line {} in statement {}'.format(line, text))
		    exit(1)
        header_keys = []
        if process_name == 'Category Template':
	        header_keys = [sheet.cell(0, col_index).value.strip().encode('utf8') for col_index in xrange(sheet.ncols)]
        else:
            #for col_index in xrange(sheet.ncols):
            #    print str(sheet.cell(0, col_index).value).strip().encode('utf8')
            for col_index in xrange(sheet.ncols):
                try:
                    cell_val = str(sheet.cell(0, col_index).value.strip()).encode('utf8')
                except:
                    print cell_val, sys.exc_info()
                    cell_val = unicodedata.normalize('NFKD',sheet.cell(0, col_index).value.strip()).encode('ascii','ignore')
                if cell_val in COL_MAP:
                    header_keys.append(COL_MAP[cell_val])
                else:
                    header_keys.append(cell_val)
            #header_keys = [COL_MAP[str(sheet.cell(0, col_index).value).strip().encode('utf8')] \
		    #    if str(sheet.cell(0, col_index).value).strip().encode('utf8') in COL_MAP \
		    #    else str(sheet.cell(0, col_index).value).strip().encode('utf8')\
            #    for col_index in xrange(sheet.ncols)]

        dict_list = []
        for row_index in xrange(1, sheet.nrows):
            d = {
                header_keys[col_index]: unicodedata.normalize('NFKD',sheet.cell(row_index, col_index).value).encode('ascii','ignore') if isinstance(sheet.cell(row_index, col_index).value, unicode) else sheet.cell(row_index, col_index).value for col_index in xrange(sheet.ncols)
            }
            dict_list.append(d)
        # create process class object dynamically using "process_name" and "process_type"
        print ' Processing for ' + process_name + ' with process type : ' + process_type
        pd = PROCESS_CLASSES[process_name]
        print pd['app_name'] + '.' + pd['file_name'] + '.' + pd['class']
        process_obj = dynamic_import(pd['app_name'] + '.' + pd['file_name'] + '.' + pd['class'])
        process_obj = process_obj()
        # call for common method for all processing Class "process data"
        process_obj.processdata({
            'data': dict_list,
            'header_keys': header_keys,
            'process_type': process_type,
            'file_id': file_id
        })

        # updating master query and errors in database for an upload process
        if process_obj.master_query:
            upload_obj.query = process_obj.master_query
            upload_obj.download_data_query = process_obj.download_data_query
            if process_obj.master_category_id:
                upload_obj.master_category_id = process_obj.master_category_id
            if process_obj.return_data['table_data']:
                upload_obj.error = json.dumps(process_obj.return_data['table_data'])
            upload_obj.download_query = process_obj.download_data_query
            print '------------->', upload_obj
            try:
                upload_obj.save()
            except Exception, e:
                process_obj.return_data['stats']['error'] = str(e)
                process_obj.return_data['stats']['success_count'] = 0
                print '======> sql error while saveing processed information.', str(e)

        process_obj.return_data.update({'file_id': file_id})
        return HttpResponse(json.dumps({
            'status_code': 200,
            'status_msg': 'Success',
            'data': process_obj.return_data,
        }))
    """
    except Exception,e:
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'Error occurred while process:' + str(e),
        }))
    """

def process_zip(request):
    file_id = request.POST['file_id'] if 'file_name' in request.POST else None
    upload_obj = MasterImportUpload.objects.get(id=file_id)
    file_name = upload_obj.file_name
    process_name = upload_obj.process_name
    process_type = upload_obj.process_type
    file_path = upload_obj.file_path
    from Products.bulk_image import MasterMedia
    media_obj = MasterMedia()
    media_obj.upload_image(file_path, file_name)
    return HttpResponse(json.dumps({
            'status_code': 200,
            'status_msg': 'Success',
            'data': []
        }))

def apply_query_req(request):
    file_id = request.POST['file_id']
    status_flag = apply_query_on_testing(file_id)
    return HttpResponse(json.dumps({
            'status_code': 200 if status_flag['flag'] else 0,
            'status_msg': 'Success' if status_flag['flag'] else 'Error',
            'errors': status_flag['error']
        }))

def apply_query_on_testing(file_id):
    """ method to apply query on testing server"""
    upload_obj = MasterImportUpload.objects.get(id=file_id)
    sql_error = []
    try:
        print 'Applying changes'
        success_count = 0
        failure_count = 0
        query = upload_obj.query
        eachquery = query.split('!@#$')
        total_query = len(eachquery)
        # creating connection with production database
        cursor = connection.cursor()
        count = 0
        for q in eachquery:
            if len(q) > 1:
                try:
                    #count += 1
                    print 'QUERY ===========>', (q + ';')
                    cursor.execute(q + ';')
                    success_count += 1
                except Exception,e:
                    print 'Exception in running sql query ---> ', str(e)
                    failure_count += 1
                    sql_error.append({
                            'errors': [{
                                'state': 'error',
                                'text': 'ERROR in QUERY: ' + str(e) +' ======= QUERY: ' + q
                            }]
                        })
                    continue
            else:
                print '----------------> blank q'
        # execute query using db cursor
        upload_obj.applied = True
        upload_obj.sql_error = json.dumps(sql_error)
        upload_obj.save()
        print 'Total queries: ', (total_query - 1)
        print 'Success: ', success_count
        print 'Failed: ', failure_count
        return {
                'flag': True if not len(sql_error) else False,
                'error': sql_error,
            }
    except Exception, e:
        print 'Error while applying query on testing', str(e)
        return {
                'flag': False,
                'error': sql_error
            }

def discard_query_req(request):
    """ method to keep track for discarding query changes"""
    file_id = request.POST['file_id']
    upload_obj = MasterImportUpload.objects.get(id=file_id)
    upload_obj.discarded_on = datetime.datetime.now()
    upload_obj.save()
    return HttpResponse(json.dumps({
            'status_code': 200,
            'status_msg': 'Success'
        }))

"""
Method to apply query on production server after applied on
"""
def apply_query_to_production_req(request):
    file_id = request.POST['file_id'] if 'file_id' in request.POST else None
    if not file_id:
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'master import export table id as file_id not provided !'
        }))
    status_flag = apply_query_on_prod(file_id)
    return HttpResponse(json.dumps({
            'status_code': 200 if status_flag else 0,
            'status_msg': 'Success' if status_flag else 'Error'
        }))

def apply_query_on_prod1(file_id):
    """ method to apply query on testing server"""
    upload_obj = MasterImportUpload.objects.get(id=file_id)
    try:
        print 'Applying changes to production'
        success_count = 0
        failure_count = 0
        query = upload_obj.query
        eachquery = query.split('!@#$')
        total_query = len(eachquery)
        # creating connection with production database
        cursor = connections['prod_stack2'].cursor()
        count = 0
        for q in eachquery:
            if len(q) > 1:
                try:
                    count += 1
                    print 'QUERY ===========>', (q + ';')
                    cursor.execute(q + ';')
                    success_count += 1
                    if count == 50:
                        count = 0
                        time.sleep(2)
                except Exception,e:
                    print 'Exception in running sql query ---> ', str(e)
                    failure_count += 1
                    continue
            else:
                print '----------------> blank q'
        # execute query using db cursor
        upload_obj.applied_on_production = True
        upload_obj.applied_on_production_time = datetime.datetime.now()
        upload_obj.save()
        print 'Total queries: ', (total_query - 1)
        print 'Success: ', success_count
        print 'Failed: ', failure_count
        return True
    except Exception, e:
        print 'Error while running query', str(e)
        return False

"""
Method to apply query on production server after applied on
"""
def create_query_req(request):
    file_id = request.GET['file_id'] if 'file_id' in request.GET else None
    if not file_id:
        return HttpResponse(json.dumps({
            'status_code': 0,
            'status_msg': 'master import export table id as file_id not provided !'
        }))
    status_flag = apply_query_on_prod(file_id)
    return HttpResponse(json.dumps(status_flag))

def apply_query_on_prod(file_id, execute_query=False):
    """ method to apply query on testing server"""
    CSync = CreateSync(file_id)
    process_name = CSync.upload_obj.process_name
    process_type = CSync.upload_obj.process_type

    base_products = []
    master_query = []
    if CSync.data_dict:
        success_count = 0
        failure_count = 0
        failure_list = []

        subs_filter_dict = []
        base_filter_dict = []
        store_filter_list = []
        print CSync.data_dict, process_name, process_type
        for k, v in CSync.data_dict.items():
            v = [str(c) for c in v]
            if k in ['subscribed_product_id', 'subscribed_ref_id']:
                subs_filter_dict.append('%s in (%s)'%(k, '"' + '","'.join(v) + '"'))
            if k in ['base_product_id', 'base_ref_id']:
                base_filter_dict.append('%s in (%s)'%(k, '"' + '","'.join(v) + '"'))
            if k in ['store_id']:
                store_filter_list.append('%s in (%s)'%(k, '"' + '","'.join(v) + '"'))

        # ===== BASE PRODUCT (insert/update)
        if base_filter_dict and process_name == 'Subscribed Product':
            base_filter_str = 'where ' + ' and '.join(base_filter_dict)
            base_columns = CSync.get_column_names('base_product')
            base_products = CSync.get_table_values(base_columns, base_filter_str, 'base_product')
            if base_products:
                base_ids = [str(int(c[0])) for c in base_products]
                for each_values_list in base_products:
                    master_query.append(CSync.create_query(base_columns, each_values_list, 'base_product'))

                # ===== PRODUCT CATEGORY MAPPING (delete all + insert)
                # creating Product category mapping queries
                pcm_filter = ['base_product_id in (%s)'%(','.join(base_ids))]
                master_query += CSync.create_bulk_sync_query(**{
                        'table_name': 'product_category_mapping',
                        'filter_list': pcm_filter,
                        'delete_all_flag': True
                    })

        # ==== SUBSCRIBED PRODUCT (insert/update)
        if subs_filter_dict and process_name == 'Subscribed Product':
            master_query += CSync.create_bulk_sync_query(**{
                    'table_name': 'subscribed_product',
                    'filter_list': base_filter_dict + subs_filter_dict
                })
            # ==== Product Category Attribute Mapping (insert/update)
            master_query += CSync.create_bulk_sync_query(**{
                    'table_name': 'Products_productcategoryattributesmapping',
                    'filter_list': subs_filter_dict,
                })

            # ==== Product Category Attribute Mapping Filter (insert/update)
            master_query += CSync.create_bulk_sync_query(**{
                    'table_name': 'Products_productcategoryattributesmappingfilters',
                    'filter_list': base_filter_dict + subs_filter_dict,
                })

        # ==== MEDIA (delete all + insert)
        # creating sync queries for Product Image excel upload
        if subs_filter_dict and process_name == 'Product Image' and process_type == 'c_u':
            subs_filter_list = [c.replace('subscribed_product_id','variant_id') for c in subs_filter_dict]
            master_query += CSync.create_bulk_sync_query(**{
                    'table_name': 'media',
                    'filter_list': base_filter_dict + subs_filter_list,
                    'delete_all_flag': True
                })
            print master_query

        # ==== STORE PRICE MAPPING (insert/update)
        if store_filter_list and process_name == 'Store Price Mapping':
            master_query += CSync.query

        # ============ Executing queries on Production database
        # only if "execute_query" is True and master_query is not empty
        if master_query and execute_query:
            print 'applying query on production'
            cursor = connections['prod_stack2'].cursor()
            for query in master_query:
                try:
                    cursor.execute(query)
                    success_count += 1
                except Exception, e:
                    failure_count += 1
                    failure_list.append(str(e) + ' : ' + query)
            print ' ----------------- Execution stats: ------------------'
            print 'Total queries: ', len(master_query)
            print 'Success: ', success_count
            print 'Failed: ', failure_count

        failure_msg = 'Success'
        if failure_list:
            failure_msg = str(failure_count) + ' out of ' + str(len(master_query)) + ' queries failed to execute'
            print '========================================================================='
            print '================ Following failed queries with errors ==================='
            print '========================================================================='
            print '\n\n'.join(failure_list)

        # saving master query and failure_list to database
        CSync.upload_obj.sync_query = json.dumps(master_query)
        CSync.upload_obj.sync_errors = json.dumps(failure_list)
        CSync.upload_obj.save()

        return {
                'status_code': 200 if not failure_list else 0,
                'status_msg': failure_msg,
                'query_stats': {
                        'success_count': success_count,
                        'failure_count': failure_count,
                        'errors': failure_list
                    }
            }
    else:
        return {
                'status_code': 0,
                'status_msg': 'No Product ids found for syncing !',
            }

def download_as_excel(data):
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

    return xlsx_data

def download_query_data(request):
    """ method to to download uploaded file as master excel with database ids in it """
    file_id = request.GET['file_id']
    CSync = CreateSync(file_id)
    process_name = CSync.upload_obj.process_name
    process_type = CSync.upload_obj.process_type

    base_products = []
    subscribed_products = []
    master_query = []
    data = {
            'table_header': [],
            'table_data': []
        }

    if CSync.data_dict:
        subs_filter_dict = []
        base_filter_dict = []
        store_filter_list = []
        for k, v in CSync.data_dict.items():
            if k in ['subscribed_product_id', 'subscribed_ref_id']:
                subs_filter_dict.append('%s in (%s)'%(k, '"' + '","'.join(v) + '"'))
            if k in ['base_product_id', 'base_ref_id']:
                base_filter_dict.append('%s in (%s)'%(k, '"' + '","'.join(v) + '"'))
            if k in ['store_id']:
                store_filter_list.append('%s in (%s)'%(k, '"' + '","'.join(v) + '"'))
        if base_filter_dict or subs_filter_dict and process_name == 'Subscribed Product' and process_type in ['create','add']:
            CSync.data_dict.update({'category_id': CSync.upload_obj.master_category_id})
            data = get_master_product(CSync.data_dict)

    xlsx_data = download_as_excel(data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=MasterProduct.xlsx'
    response.write(xlsx_data)
    return response

def download_uploaded_file(request):
    """ download file uploaded for a change log id """
    file_id = request.GET['file_id']
    file_obj = MasterImportUpload.objects.get(id=file_id)
    excel_file = open(BASE_PATH + str(file_obj.file_path) + str(file_obj.file_name), 'r')
    response = HttpResponse(excel_file, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=%s'%(str(file_obj.file_name))
    return response
