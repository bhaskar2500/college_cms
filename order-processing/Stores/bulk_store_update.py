from Stores.models import *
from Products.bulk_product import MasterProduct
import json

class MasterStorePrice():
        def __init__(self):
            self.master_query = ""
            self.return_data = ""
            self.download_data_query = "{}"
            self.master_category_id = 0

        def getStores(self):
            """ get brands all brands with key as brand name and brand id as value """
            self.all_stores = Store.objects.all().values_list('store_id', flat=True)
            return

        def create_update_data(self):
            self.getStores()
            error_list = []
            required_headers = ['base_product_id', 'subscribed_product_id', 'store_id', 'region_id', 'store_price', 'store_offer_price', 'publish']
            store_price_headers = required_headers + ['price_type', 'discount', 'purchase_price', 'markup', 'moq_retail', 'moq_incremental_retail',
                'moq_enterprise', 'moq_increment_enterprise', 'dispatch_location', 'vat' ,'shipping_charge', 'stock_status', 'price_validity',
                'shipment_mode', 'is_cancelable', 'is_cod', 'is_returnable' ,'processing_time' ,'conforming_standard', 'warranty', 'item_buying_type']
            extra_header = list(set(self.data_dict['header_keys']) - set(store_price_headers))
            headers_missing = list(set(required_headers) - set(self.data_dict['header_keys']))
            print headers_missing
            if len(headers_missing):
                self.return_data = {'table_header': [],
                    'table_data' : [],
                    'stats': {
                    'error' : "%s Required. Processing Failed"%(" , ".join(headers_missing)),
                    'extra_headers':extra_header,
                    'error_count': 0,
                    'success_count':0}
                    }
                return False

            combined_base_list = []
            combined_subscribed_list = []
            combined_list = []
            # ===== looping data for collectin base product id and subscribed product id
            for d in self.data_dict['data']:
                if not d['subscribed_product_id'] == 'XXX':
                    combined_base_list.append(str(int(d['base_product_id'])))
                    combined_subscribed_list.append(str(int(d['subscribed_product_id'])))
                    combined_list.append(str(int(d['base_product_id'])) + '_' + str(int(d['subscribed_product_id'])))

            # get ids from database (base and subscribed)
            if combined_list:
                mpobj = MasterProduct()
                mpobj.getallsubscribed_product({
                    'base_ids': combined_base_list,
                    'subs_ids': combined_subscribed_list
                })

            ignore_subscribed_product_ids = []

            # feeding subscribed product id into ignore_subscribed_product_ids in second loop
            if combined_list and not combined_list == mpobj.subscribed_product_list:
                ignore_subscribed_product_ids = list(set(combined_list) - set(mpobj.subscribed_product_list))

            download_query_data = {}
            insert_update_values = ''
            insert_count = 0
            i = 0
            for store_price_data in self.data_dict['data']:
                i += 1
                store_price_data.update({'row_no': i})
                temp = store_price_data.copy()

                # error handling for blank product id
                if not store_price_data['base_product_id']:
                    temp.setdefault('errors', []).append({
                        'text': 'Base product id cannot be left blank',
                        'state': 'error',
                    })
                    error_list.append(temp)
                    continue

                # checking for subscribe product id in data from file
                if 'subscribed_product_id' in store_price_data and store_price_data['subscribed_product_id']:
                    # error handling for XXX in subscribed product id
                    if str(store_price_data['subscribed_product_id']) == 'XXX':
                        temp.setdefault('errors', []).append({
                            'text': 'Subscribed id cannot be XXX',
                            'state': 'error'
                        })
                        error_list.append(temp)
                        continue

                base_product_id = str(int(store_price_data['base_product_id']))
                subscribed_product_id = str(int(store_price_data['subscribed_product_id']))

                # error handing for subscribed product id in combination with base that are not in database
                if (base_product_id + '_' + subscribed_product_id) in ignore_subscribed_product_ids:
                    temp.setdefault('errors', []).append({
                        'text': 'Subscribed product id: '+ subscribed_product_id +
                        ' not found in database for base product id: ' + base_product_id,
                        'state': 'error'
                        })
                    error_list.append(temp)
                    continue

                if not store_price_data['store_id']:
                    temp.setdefault('errors', []).append({
                        'text': 'Store id cannot be left blank',
                        'state': 'error',
                    })
                    error_list.append(temp)
                    continue
                elif not store_price_data['store_id'] in self.all_stores:
                    temp.setdefault('errors', []).append({
                        'text': 'Store id not found in database',
                        'state': 'error',
                    })
                    error_list.append(temp)
                    continue

                download_query_data.setdefault('base_product_id', []).append(store_price_data['base_product_id'])
                download_query_data.setdefault('subscribed_product_id', []).append(store_price_data['subscribed_product_id'])

                # Initializing Store Price Data
                init_store_price_data = {x:"" for x in store_price_headers}
                init_store_price_data.update(store_price_data)
                store_price_data = init_store_price_data
                key_int = []
                key_str = ["store_price", "store_offer_price", "region_id", "discount",
                        "purchase_price", "markup", "moq_retail", "moq_incremental_retail", "moq_enterprise", "moq_increment_enterprise",
                        "vat", "shipping_charge", "is_cancelable", "is_cod", "is_returnable", "publish",
                        "price_type","dispatch_location", "stock_status", "price_validity",
                        "processing_time", "conforming_standard", "warranty","item_buying_type"]
                key_null = ["price_validity"]
                for key in store_price_data.keys():
                    print key, not len(str(store_price_data[key]))
                    if not len(str(store_price_data[key])):
                        if key in key_int:
                            store_price_data[key] = 0
                        elif key in key_str:
                            store_price_data[key] = ""
                        elif key in key_null:
                            store_price_data[key] = "NULL"
                print store_price_data
                insert_update_values += ('("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s",\
                     "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"),')%(store_price_data['base_product_id'],
                    store_price_data['subscribed_product_id'],
                    store_price_data['store_id'],
                    store_price_data['store_price'],
                    store_price_data['store_offer_price'],
                    store_price_data['region_id'],
                    store_price_data['price_type'],
                    store_price_data['discount'],
                    store_price_data['purchase_price'],
                    store_price_data['markup'],
                    store_price_data['moq_retail'],
                    store_price_data['moq_incremental_retail'],
                    store_price_data['moq_enterprise'],
                    store_price_data['moq_increment_enterprise'],
                    store_price_data['dispatch_location'],
                    store_price_data['vat'],
                    store_price_data['shipping_charge'],
                    store_price_data['stock_status'],
                    store_price_data['price_validity'],
                    store_price_data['shipment_mode'],
                    store_price_data['is_cancelable'],
                    store_price_data['is_cod'],
                    store_price_data['is_returnable'],
                    store_price_data['processing_time'],
                    store_price_data['conforming_standard'],
                    store_price_data['warranty'],
                    store_price_data['item_buying_type'],
                    #store_price_data['unit_price'],
                    #store_price_data['secondary_store_price'],
                    store_price_data['publish'])
                print insert_update_values
                insert_count += 1
            if insert_count:
                insert_update_values = insert_update_values[:-1]
                self.master_query = """insert into store_price_mapping (base_product_id, subscribed_product_id,
                    store_id, store_price, store_offer_price, region_id, price_type, discount, purchase_price,
                    markup, moq_retail, moq_incremental_retail, moq_enterprise, moq_increment_enterprise, dispatch_location,
                    vat, shipping_charge, stock_status, price_validity, shipment_mode, is_cancelable, is_cod,
                    is_returnable, processing_time, conforming_standard, warranty, item_buying_type,
                    publish) VALUES %s on duplicate key update
                    store_price = CASE WHEN VALUES(store_price) = "" THEN store_price ELSE VALUES(store_price) END,
                    store_offer_price = CASE WHEN VALUES(store_offer_price) = "" THEN store_offer_price ELSE VALUES(store_offer_price) END,
                    region_id = CASE WHEN VALUES(region_id) = "" THEN region_id ELSE VALUES(region_id) END,
                    price_type = CASE WHEN VALUES(price_type) = "" THEN price_type ELSE VALUES(price_type) END,
                    discount = CASE WHEN VALUES(discount) = "" THEN discount ELSE  VALUES(discount) END,
                    purchase_price = CASE WHEN VALUES(purchase_price) = "" THEN purchase_price ELSE VALUES(purchase_price) END,
                    markup = CASE WHEN VALUES(markup) = "" THEN markup ELSE VALUES(markup) END,
                    moq_retail = CASE WHEN VALUES(moq_retail) = "" THEN moq_retail ELSE VALUES(moq_retail) END,
                    moq_incremental_retail = CASE WHEN VALUES(moq_incremental_retail) = "" THEN moq_incremental_retail ELSE VALUES(moq_incremental_retail) END,
                    moq_enterprise = CASE WHEN VALUES(moq_enterprise) = "" THEN moq_enterprise ELSE VALUES(moq_enterprise) END,
                    moq_increment_enterprise = CASE WHEN VALUES(moq_increment_enterprise) = "" THEN moq_increment_enterprise ELSE VALUES(moq_increment_enterprise) END,
                    dispatch_location = CASE WHEN VALUES(dispatch_location) = "" THEN dispatch_location ELSE VALUES(dispatch_location) END,
                    vat = CASE WHEN VALUES(vat) = 0 THEN vat ELSE VALUES(vat) END,
                    shipping_charge = CASE WHEN VALUES(shipping_charge) = "" THEN shipping_charge ELSE VALUES(shipping_charge) END,
                    stock_status = CASE WHEN VALUES(stock_status) = "" THEN stock_status ELSE VALUES(stock_status) END,
                    price_validity = CASE WHEN VALUES(price_validity) = "NULL" THEN price_validity ELSE VALUES(price_validity) END,
                    shipment_mode = CASE WHEN VALUES(shipment_mode) = "" THEN shipment_mode ELSE VALUES(shipment_mode) END,
                    is_cancelable = CASE WHEN VALUES(is_cancelable) = "" THEN is_cancelable ELSE VALUES(is_cancelable) END,
                    is_cod = CASE WHEN VALUES(is_cod) = "" THEN is_cod ELSE VALUES(is_cod) END,
                    is_returnable = CASE WHEN VALUES(is_returnable) = "" THEN is_returnable ELSE VALUES(is_returnable) END,
                    processing_time = CASE WHEN VALUES(processing_time) = "" THEN processing_time ELSE VALUES(processing_time) END,
                    conforming_standard = CASE WHEN VALUES(conforming_standard) = "" THEN conforming_standard ELSE VALUES(conforming_standard) END,
                    warranty = CASE WHEN VALUES(warranty) = "" THEN warranty ELSE VALUES(warranty) END,
                    item_buying_type = CASE WHEN VALUES(item_buying_type) = "" THEN item_buying_type ELSE VALUES(item_buying_type) END,
                    publish = CASE WHEN VALUES(publish) = "" THEN publish ELSE VALUES(publish) END !@#$"""%(insert_update_values)
            if download_query_data:
                self.download_data_query = json.dumps(download_query_data)
            self.return_data = {'table_header': [] if not len(error_list) else ['errors'] + required_headers,
                'table_data' : error_list,
                'stats': {
                    'error' : "",
                    'extra_headers': extra_header,
                    'error_count': len(error_list),
                    'success_count': insert_count}
            }

        def processdata(self, data_dict):
            self.data_dict = data_dict
            final_data = {}
            final_data = self.create_update_data()
            self.data_dict['data'] = final_data
            return self.data_dict
