from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from multidbconfig import MultiDBModelAdmin, MultiDBTabularInline
from import_export import resources
from import_export.admin import *
from Orders.models import OrderHeader, 	OrderLine, Login,OrderLine_History,orderstatus,	linestatus
from django.db.models import Q
from django.contrib.admin.widgets import AdminDateWidget
import datetime
from django import forms
from django.db import models
import json
from cms.plugin_base import CMSPluginBase

from Orders.configure_lines import *


class OrderHeaderResource(resources.ModelResource):
    class Meta:
        model = OrderHeader

class OrderHeaderAdmin(ExportMixin, MultiDBModelAdmin):
	def overview(self,obj):
		return "<a href='/admin/view/?q="+str(obj.order_id)+"'"+ " target='_blank' >OverView</a>"

	def snap(self,obj):
		order_obj=OrderLine.objects.using('orders').filter(order_id=obj.order_id)
		s=" "
		for each in order_obj:						

			s=s+"<tr><td>"+str(each.product_title)+" </td><td>"+str(each.product_qty)+"</td><td>"+str(each.pickup_date)+"</td> </tr> "
		return "<table><thead><tr><th>Product Name</th><th>Product Quantity</th><th>Pickup date</th> </tr> </thead> <tbody>"+s+"</tbody></table>"
	snap.allow_tags=True

	def custom_status(self, obj):
		l = {

		'processing':0,
		'payment-pending':0,
		'exportable':0,
		'exported':0,
		'po-created':0,	
		'ready-to-pickup':0,
		'fullfillment-center':0,
		'invoice-created':0,
		'qc-packaging':0,
		'shipped':0,
		'delivered':0,
		'closed':0,
		'return-request':0,
		'policy-not-applicable':0,
		'return-denied':0,
		'return-accepted':0,
		'returned':0,
		'to-be-returned-to-vendor':0,
		'new-proc-exchange':0,
		'exchange':0,
		'refund':0,
		'closed':0,
		'order-cancelled':0,
		'seller-accepted':0,
		'seller-rejected':0,

		}
		query=OrderLine.objects.using('orders').filter(order_id=obj.order_id)

		st= ''
		for each in query:
			try:
				l[each.status]+=1
			except:
				print 'sup'
		for key,value in l.iteritems():
			if value != 0 :
				if  key=="processing":
					st += str(value) +"P"
				elif key=="shipped":
					st += str(value) +"S"
				elif key=="refund":
					st += str(value) +"R"
				elif key=="seller-accepted":
					st+=str(value)+"SA"

				# l[key]=0
				st+='<br>'
				
		return st
	custom_status.allow_tags=True	
	resource_class = OrderHeaderResource
	list_display = ('order_id', 
	'order_number',
	'custom_status',
	'created_date',
	'snap','overview',
	'payment_type',	
	'total_payable_amount',
	'billing_name',
	'billing_email','billing_pincode',
	'shipping_name',
	'billing_phone',
	'shipping_phone',
	'user_phone_no',
	'user_email',
	
	)

    	search_fields = ('order_id', 'order_number','user_phone_no')
    	list_filter = (
			('created_date', DateFieldListFilter),
			)

    	readonly_fields = ('custom_status','snap' ,'overview')
    	overview.allow_tags=True


admin.site.register(OrderHeader, OrderHeaderAdmin)


def create_box(Linestatus_ob,obj):
	s=''	
	for each in Linestatus_ob:
		os=orderstatus.objects.using('orders').get(status=each.order_status)
		comm_dict=json.dumps({'seller_email':os.seller_mail,'cust_mail':os.cust_email,'seller_sms':os.seller_sms,'cust_sms':os.cust_sms})
		if obj.status == str(each.order_status).lower():
			
			temp = 'selected'
			s=s+'<option  data-comm=%s value="%s" %s>%s</option>'%(("'"+comm_dict+"'"),str(each.order_status).lower(),temp,each.order_status)
			continue
		s=s+'<option data-comm=%s data-name="status__exact" value="%s" >%s</option>'%(("'"+comm_dict+"'"),str(each.order_status).lower(),each.order_status,)
	return '<select style="width: 130px;" selected_status="status">'+s+'</select>'

class OrderLineResource(resources.ModelResource):
    class Meta:
       	model = OrderLine

class OrderLineAdmin(ExportMixin, MultiDBModelAdmin):

	def custom_stat(self,obj):
		l_ob=linestatus.objects.using('orders').raw(' select * from linestatus join orderstatus on (linestatus.order_status=orderstatus.id) where line_name="orderline" order by orderstatus.order_by asc')
		a=create_box(l_ob,obj)
		return a
	
	custom_stat.allow_tags=True



	class Media:
		js=('http://localhost/cadmin/static/js/jquery.js',
			'http://localhost/cadmin/static/js/jquery.datetimepicker.full.js',
			'http://localhost/cadmin/static/js/remarks.js',
			'http://localhost/cadmin/static/js/export.js',
			'http://localhost/cadmin/static/js/boots.js',
			'http://localhost/cadmin/static/js/bootbox.min.js',
			'http://localhost/cadmin/static/js/jquery.datetimepicker.full.min.js',
			'http://localhost/cadmin/static/js/export.js','http://localhost/cadmin/static/js/jquery.datetimepicker.js',
			'http://localhost/cadmin/static/js/pickupline.js','http://localhost/cadmin/static/js/select.js',
			'http://localhost/cadmin/static/js/modal.js','http://localhost/cadmin/static/js/order_line.js')
		css = {
            'all': ('http://localhost/cadmin/static/js/jquery.datetimepicker.css',)
        }
	        resource_class = OrderLineResource
        list_display = ('order_id',
        'order_line_id', 
        'store_id',	
	'custom_stat',
	'store_name',
	'pickup_date',
	'seller_name',
	'seller_phone',
	'product_title','product_name',
	'product_qty',
	'unit_price',
	'price',
	'vatrate',
	'total_vat',
	'subtotal',
	'lead_time','store_email','remarks',
	)		
        # search_fields = ('order_id', 'order_line_id',)
    	list_filter = ('status','order_line_id','store_id')
	readonly_field=('pickup_date','snap')




admin.site.register(OrderLine, OrderLineAdmin)



class PickupLine(OrderLine,models.Model):
	class Meta:
		proxy = True


class PickupLineAdmin(OrderLineAdmin):

	class Media:
		js=('http://localhost/cadmin/static/js/order_line.js',
			'http://localhost/cadmin/static/js/delivery.js',
			'http://localhost/cadmin/static/js/datePicker.js')
	def custom_stat(self,obj):
		l_ob=linestatus.objects.using('orders').raw(' select * from linestatus join orderstatus on (linestatus.order_status=orderstatus.id) where line_name="pickupline" order by orderstatus.order_by asc')
		a=create_box(l_ob,obj)
		return a

		
	custom_stat.allow_tags=True



	def get_queryset(self,request):	
		try:
			qs=OrderLine.objects.using('orders').filter(pickup_date__contains='2')
			
			return qs
		except Exception , e:

			return qs 

	search_fields=('order_id',)
	list_filter = ('pickup_date',)
	list_display=('order_id','custom_stat','order_line_id','price','store_id','product_title','product_qty','seller_name','pickup_date','seller_phone','seller_address','seller_city',)
admin.site.register(PickupLine, PickupLineAdmin)


class LoginResource(resources.ModelResource):
    class Meta:
        model = Login
    


class LoginAdmin(ExportMixin, MultiDBModelAdmin):
    resource_class = LoginResource
    # list_display = ('username', 'name', 'email', 'registere	d_at', 'last_login', 'is_verified')
    search_fields = ['name',	 'username','email']

admin.site.register(Login, LoginAdmin)



class DeliveryLine(OrderLine):


	class Meta:
		proxy=True


class DeliveryLineAdmin(OrderLineAdmin):
	

	def get_queryset(self,request):	
		qs=super(OrderLineAdmin,self).get_queryset(request)
		# print qs 
		try:
			pickup_date= request.GET['q'] if 'q' in request.GET else None
			# print pickup_date

			d = datetime.datetime.strptime(pickup_date, "%d/%m/%Y") 
				# d=d.isoformat().strip('T00:00:00')
			if d:

				date_query=OrderLine.objects.using('orders').filter(pickup_date=d)
				return date_query

		except:
			return qs		
	def pincodes(self,obj):

		ob=OrderHeader.objects.using('orders').values_list('billing_pincode').filter(order_id=obj.order_id)

		for tup in ob:
			for item in tup:
				return item 
		
	def billing_address(self ,obj):
		return  str(obj.seller_name)+'</br>'+str(obj.seller_address)+'</br>'

	billing_address.allow_tags=True
	list_filter=()
	
	list_display=('order_id','billing_address','product_qty','product_name','unit_price','seller_phone','pincodes','seller_name','order_line_id','seller_address','subtotal','pickup_date')
	# list_filter=('pickup_date',)
admin.site.register(DeliveryLine,DeliveryLineAdmin)




class historyline(resources.ModelResource):
    class Meta:
        model = OrderLine_History
    


class historyAdmin(ExportMixin, MultiDBModelAdmin):
    resource_class = historyline
    list_display = ('created_date','order_line_id', 'User','actions', 'change_from', 'change_to',)

admin.site.register(OrderLine_History, historyAdmin)

class crm(OrderLine):
	class Meta:
		proxy=True
class crmAdmin(OrderLineAdmin):
	def custom_stat(self,obj):
		l_ob=linestatus.objects.using('orders').raw(' select * from linestatus join orderstatus on (linestatus.order_status=orderstatus.id) where line_name="crmline" order by orderstatus.order_by asc')
		a=create_box(l_ob,obj)
		return a
	
	list_display=('order_line_id','custom_stat')
	readonly_fields=('custom_stat',)
	custom_stat.allow_tags=True


admin.site.register(crm,crmAdmin)	


class linestatusResource(resources.ModelResource):
    class Meta:
        model = linestatus
    


class LineAdmin(MultiDBModelAdmin):
    resource_class =linestatusResource

    list_display = ( 'line_name','order_status')
    # search_fields = ['name',	 'username','email']

admin.site.register(linestatus, LineAdmin)


class orderstatusResource(resources.ModelResource):
    class Meta:
        model = orderstatus
    

class OrderAdmin(ExportMixin, MultiDBModelAdmin):
	resource_class=orderstatusResource

    	list_display = ( 'status','status_name','order_by')
    # search_fields = ['name',	 'username','email']

admin.site.register(orderstatus, OrderAdmin)
	