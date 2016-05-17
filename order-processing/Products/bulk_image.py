from django.shortcuts import render_to_response
from Products.models import *
from django.db import connection
import zipfile
import os.path
import os, sys
import subprocess
import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance
from settings import CUR_ENV, ENVIRONMENT_VAR
from django.template import RequestContext
import datetime
import json

def product_bulk_image_page(request):
    return render_to_response("common_bulk_upload.html", {
            'page_header': 'Product Image',
            'process_name': 'Product Image',
            'process_type': [
                    {'text': 'Create/Update', 'value': 'c_u'},
                ],
            'action_url': '/admin/upload'
        }, context_instance=RequestContext(request))

def bulk_zip_upload_page(request):
    return render_to_response("imagezip_bulk_upload.html", {
            'page_header': 'Product Image',
            'process_name': 'Product Image',
            'process_type': [
                    {'text': 'Upload Zip', 'value': 'u'},
                ],
            'action_url': '/admin/upload_zip'
        }, context_instance=RequestContext(request))

class MasterMedia():
    def __init__(self):
        self.master_query = ""
        self.return_data = {}
        self.download_data_query = '{}'

    def create_update_data(self):
        error_list = []
        delete_query = ""
        create_query = ""
        thumb_data = {}
        required_headers = ['base_product_id', 'media', 'subscribed_product_id']
        extra_header = list(set(self.data_dict['header_keys']) - set(required_headers))
        if 'subscribed_product_id' not in self.data_dict['header_keys'] or 'media' not in self.data_dict['header_keys']:
            self.return_data = {'table_header': [],
                'table_data' : [],
                'stats': {
                    'error' : "%s Required. Processing Failed"%('Subscribed Product Id' if 'subscribed_product_id' not in self.data_dict['header_keys'] else "Media"),
                    'extra_headers':extra_header,
                    'error_count': 0,
                    'success_count':0}
            }
            return False
        #thumb_data = map(lambda x: map(lambda y: "%s_%s"%(x['variant_id'], y) ,
        #    x['media'].replace(" ","").split(',')) , self.data_dict['data'])
        download_query_data = {}  # for donwload query
        for x in self.data_dict['data']:
            for y in x['media'].replace(" ","_").split(','):
                thumb_data["%s_%s"%(str(int(x['subscribed_product_id'])),y.replace(" ","_"))] = x
        subscribed_prod_data = {str(int(x['subscribed_product_id'])) : x for x in self.data_dict['data']}
        db_subscribed_data = { "%s_%s"%(str(int(x['variant_id'])), x['media_url'].split('/')[0]) : x['media_id'] for x in Media.objects.\
            filter(variant_id__in = subscribed_prod_data).values('variant_id','media_url', 'media_id')}
        # New Media
        new_subscribed_media = set(thumb_data.keys()) - set(db_subscribed_data.keys())
        # Delete Media
        media_deleted = set(db_subscribed_data.keys()) - set(thumb_data.keys())
        delete_media_id_list = [db_subscribed_data[key] for key in media_deleted]
        # Deleting Media
        #Media.objects.filter(media_id__in = delete_media_id_list).delete()
        if len(delete_media_id_list):
            delete_query = """DELETE from media WHERE media_id in (%s) !@#$"""%(",".join(str(int(x)) for x in delete_media_id_list))
        # Checking for Subscribed Products
        subsc_id_list = map(lambda x:x.split('_')[0] ,new_subscribed_media)
        subsc_data = map(lambda x:x['subscribed_product_id'] ,SubscribedProduct.objects.filter(subscribed_product_id__in = subsc_id_list).values('subscribed_product_id'))
        no_exist_subsc_ids = list(set(subsc_id_list) - set(subsc_data))
        # Creating Media
        bulk_create_objs = []
        value_list = ""
        insert_count = 0
        for media_data in new_subscribed_media:
            if thumb_data[media_data]['subscribed_product_id'] in no_exist_subsc_ids:
                thumb_data[media_data].update({'errors': [{'text': 'Subscribed Id does not exist', 'state': 'error'}],})
                error_list.append(thumb_data[media_data])
                continue
            insert_count += 1
            image_name = "_".join(media_data.split("_")[1:]).replace(" ","_")

            # added for collecting base and subscribed product ids
            download_query_data.setdefault('base_product_id',[]).append(str(thumb_data[media_data]['base_product_id']))
            download_query_data.setdefault('subscribed_product_id',[]).append(str(thumb_data[media_data]['subscribed_product_id']))
            value_list += """(%s, %s, "%s", "%s"), """%(thumb_data[media_data]['base_product_id'], thumb_data[media_data]['subscribed_product_id'],
            'images/media/product/main/new/%s'%image_name, 'images/media/product/thumbnails/new/%s'%image_name)

            #bulk_create_objs.append(Media(**{'base_product_id': thumb_data[media_data]['base_product_id'],
            #   'media_url': 'images/media/product/main/new/%s'%(thumb_data[media_data]['media']),
            #   'thumb_url': 'images/media/product/thumbnails/new/%s'%(thumb_data[media_data]['media']),
            #   'status': 0}))
            #Media.objects.bulk_create(bulk_create_objs)
        if len(value_list):
            # Removing last comma
            value_list = value_list[:-2]
            create_query = """INSERT INTO media (base_product_id, variant_id, media_url, thumb_url) VALUES %s !@#$"""%value_list
        self.master_query = delete_query + create_query
        print self.master_query
        if download_query_data:
            self.download_data_query = json.dumps(download_query_data)
        self.return_data = {'table_header': [] if not len(error_list) else ['Error'] + required_headers,
                'table_data' : error_list,
                'stats': {
                    'error' : "",
                    'extra_headers': extra_header,
                    'error_count': len(error_list),
                    'success_count': insert_count}
                }

    def upload_image(self, file_path, filename):
        print "Unzipping %s on Test Server on path %s"%(filename, file_path)
        subprocess.call('python /www/supplified-cms/bulk_upload_images.py -f %s -p %s'%(filename, file_path), shell=True)
        print "Sending File to Prod Server ...... "
        try:
            today_date = datetime.date.strftime(datetime.date.today(), '%d-%m-%y')
            file_path = '/www/supplified-cms/static/upload_product_image/u/%s/%s'%(today_date, filename)
            subprocess.call(["scp","-i",ENVIRONMENT_VAR[CUR_ENV]['pem'], file_path, "ubuntu@%s:/www/public_html/upload_zip/"%(ENVIRONMENT_VAR[CUR_ENV]['dns'])])
            conn = boto.ec2.connect_to_region('us-west-2')
            instance = conn.get_all_instances(ENVIRONMENT_VAR[CUR_ENV]['instance_id'])[0].instances[0]
            ssh_client = sshclient_from_instance(instance,
            ENVIRONMENT_VAR[CUR_ENV]['pem'],
            user_name='ubuntu')
            status, stdout, stderr = ssh_client.run('python /www/public_html/bulk_upload_images.py -f %s -p %s'%(filename, "/www/public_html/upload_zip/"))
        except:
            print "Error : ",sys.exc_info()
        print "Successfully Uploaded and Compressed"

    def processdata(self, data_dict):
        self.data_dict = data_dict
        final_data = {}
        final_data = self.create_update_data()
        self.data_dict['data'] = final_data
        return self.data_dict
