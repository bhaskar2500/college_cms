from Orders.models import *
from django.contrib.auth.decorators import login_required
import json 
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from Email.email_views import ShootMail
from django.shortcuts import render
import datetime
from django.template import Context,loader
from django.contrib import admin
from django.conf import settings
try:
    import StringIO
except ImportError:
    from io import StringIO
from django.template.loader import get_template
import os
import subprocess
from Orders.config import *
import pycurl
import urllib
import time
from django.db import models
from xlsxwriter import Workbook
from supplified.sync_query import CreateSync
from config_po import *
from num2words import num2words
# from Products.views import auth
@login_required
def change_order_status(request):
    order_line_id = request.POST['order_line_id'] if 'order_line_id' in request.POST else None
    order_status = request.POST['order_status'] if 'order_status' in request.POST else None
    order_stat = request.POST['order_stat'] if 'order_stat' in request.POST else None
    pickup_date=request.POST['date'] if 'date' in request.POST else None
    header_id=request.POST['header_id'] if 'header_id' in request.POST else None
    message=request.POST.getlist('message[]') if 'message[]' in request.POST  else None
    prev_date=request.POST['prev_date'] if 'prev_date' in request.POST else None
    try: 
        print request.POST
        data={}

        if pickup_date is not None  and order_status=='seller-accepted' :
            data['change_from']= pickup_date
            data['change_to']=prev_date
            data['User']=request.user
            history('Change Date',data,order_line_id)
            orderline = OrderLine.objects.using('orders').get(order_line_id=order_line_id)

            d = datetime.datetime.strptime(pickup_date, "%Y/%m/%d %H:%M:%S")
            d=d.replace(tzinfo=None)
            orderline.pickup_date= d
            orderline.save()
        if order_status is not None:
            orderline = OrderLine.objects.using('orders').get(order_line_id=order_line_id)
            old_status=orderline.status  
            orderline.status = order_status
            orderline.save()
            data['change_from']=old_status
            data['change_to']=order_status
            data['User']=request.user

            history('Change Status',data,order_line_id)
            
        def curl_call(sms_url):
            buffer = StringIO.StringIO()
            c=pycurl.Curl()
            c.setopt(c.URL, sms_url)  
            c.setopt(c.WRITEDATA, buffer)
            c.perform()
            c.close()
            body = buffer.getvalue()
            print body

        
        if message is not None:    
            header_ob = OrderHeader.objects.using('orders').get(order_id=header_id)
            email_customer=OrderHeader.objects.using('orders').filter(user_email=header_ob.user_email,order_id=header_id).values('user_email')
            phone_no_customer=OrderHeader.objects.using('orders').filter(user_phone_no=header_ob.user_phone_no,order_id=header_id).values('user_phone_no')   
            
            if pickup_date is not None or order_status is not None:
                os=orderstatus.objects.using('orders').get(status=str(order_status).capitalize())
                if 'email_seller' in message:
                    print 'Email/SMS will be sent to user for this status change ---> do worry neither update not sent'
                    ShootMail(**{
                    'subject': 'This is a dummy subject line',
                    'body': os.temp_cust_mail   ,
                    'email':'bhaskar.2500@gmail.com'
                    #email_customer[0]['user_email']
                    }).shoot_email()
                if 'sms_seller' in message :  
                            sms_content=os.temp_cust_sms  
                            if order_status=='shipped':
                                sms_content=sms_content%(orderline.order_line_id,orderline.product_title)
                            if order_status=='delivered':
                                sms_content=sms_content%(header_ob.order_number,orderline.product_title)

                            if order_status=="cancelled":
                                sms_content=sms_content%{'order_no':header_ob.order_number}


                            sms_txt=urllib.quote_plus(sms_content)
                            sms_url='http://23.254.128.22:9080/urldreamclient/dreamurl?userName=sup_tech&password=supTech123&clientid=supTedst29&to=9821167654&text='+sms_txt+'&Senderid=SUPTRX' 
                            curl_call(sms_url)


                if 'sms_vendor' in message:  
                            sms_content=os.temp_seller_sms
                            if order_status=='shipped':
                                sms_content=sms_content%(orderline.order_line_id,orderline.product_title)
                            if order_status=='delivered':
                                sms_content=sms_content%{'order_no':header_ob.order_no,'product_name':orderline.product_title}

                            if order_status=="cancelled":
                                sms_content=sms_content%{'order_no':header_ob.order_number}

                            sms_txt=urllib.quote_plus(sms_content)

                            sms_url='http://23.254.128.22:9080/urldreamclient/dreamurl?userName=sup_tech&password=supTech123&clientid=supTedst29&to=9821167654'+'&text='+sms_txt+'&Senderid=SUPTRX' 
                            curl_call(sms_url)

                if 'email_vendor' in message:
                            print 'Email/SMS will be sent to user for this status change ---> do worry neither update not sent'+str(orderline.store_email)
                            ShootMail(**{
                            'subject': 'This is a dummy subject line',
                            'body': os.temp_seller_mail,
                            'email':'bhaskar.2500@gmail.com'
                            # orderline.user_email
                            }).shoot_email()  

                
        return HttpResponse(json.dumps({
                'status_code': 200,
                'status_msg': 'Success'
            }))
            
	
	

    except Exception, e:
        print e
        return HttpResponse(json.dumps({
	        'status_code': 0,
	   	'status_msg': 'Error:' + str(e)	    
	    }))

def get_check(request):

   
    try:
        id_pdf=request.POST['hidden'].split(',') if 'hidden' in request.POST else None
        id_doc=request.POST['hidden_doc'].split(',') if 'hidden_doc' in request.POST else None

        if id_doc!=None:
            ob_doc=OrderLine.objects.using('orders').filter(order_line_id__in=id_doc)
            file_pdf =format(ob_doc,'docx')    
        if id_pdf!=None:
            ob=OrderLine.objects.using('orders').filter(order_line_id__in=id_pdf)
            file_pdf=format(ob,'pdf')
        # for each in file_pdf:
        #     if os.path.exists(each):
        #         fil=each.split('/')
        #         print 'file found ----------------------->>>'+fil[6]
        timestamp=datetime.datetime.now()
        times=timestamp.strftime('%d-%m-%Y %H:%M:%S')
        zip_folder = './po-generation/zip/'



        if not os.path.exists(zip_folder):

            os.makedirs(zip_folder)
        zip_name='PO%s.zip'%(times)
        rc = subprocess.Popen(['7z', 'a','-r', zip_folder+zip_name] +file_pdf)       
        rc.communicate()


        
        wrapper = FileWrapper(file(zip_folder+'PO%s.zip'%(times)))
        rc.wait()

        zip_response=HttpResponse(wrapper, content_type='application/zip')


        zip_response['Content-Disposition'] = 'attachment; filename=PO.zip'
        zip_response.write(wrapper)
        
        return zip_response


            
    except Exception,e:
        print "Could not get the id "+str(e)     
def list_id(key,value):
    list_id=map(lambda x:str(x.order_line_id),value)
    name=key+'-'+((',').join(list_id))
    timestamp=datetime.datetime.now()
    times=timestamp.strftime('%d-%m-%Y %H:%M:%S')
    head=name+" "+times
    return head    
def render_to_pdf(template_src,key,value,new_folder):
    content=PO['head_po']+PO['body_po']+PO['foot_po']
    f=open('./Products/templates/'+template_src,'w')

    f.write(content)
    f.close()

    template = get_template(template_src)
    pickup_details=value[0].pickup_date
    pickup_date=pickup_details.strftime('%d-%m-%Y')
    pickup_time=pickup_details.strftime('%H:%M:%S')
    dob=datetime.datetime.now()
    po_date=dob.strftime("%d-%m-%Y")
    order_header=OrderHeader.objects.using('orders').get(order_id=value[0].order_id)
    email=order_header.user_email
    pincode=order_header.billing_pincode
    order_ref=order_header.order_number
    s=0
    total_value=0
    total_tax=0
    for each in value:
        s=s+each.subtotal
        total_value=float(s)+float(each.total_vat)
        total_tax=float(total_tax)+float(each.total_vat)
    in_words=num2words(total_value).capitalize()
    round_off=round(total_value,3)

    html  = template.render({'round_off':round_off,'value':value,'pickup_date':pickup_date,'pickup_time':pickup_time,'po_date':po_date,'email':email,'pincode':pincode,'order_ref':order_ref,'sum':s,'total_value':total_value,'total_tax':total_tax,'in_words':in_words})
    result = StringIO.StringIO()
    head=list_id(key,value)
    print "=========>>>>>>>>>"+str(head)
    pdf_folder =new_folder+'/pdf/'
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    f=open('any.html','w')
    f.write(html)
    f.close()


    a=subprocess.Popen(['prince','./any.html', '-o' ,pdf_folder+head+'.pdf'])
    a.wait()
    each=pdf_folder+head
    print 'each========================='+each
    if os.path.exists(each):
        # fil=each.split('/')
        print 'file found ----------------------->>>'

    return a,pdf_folder+head,head

def render_to_doc(template_src,key,value,new_folder):
    content=PO['head_invoice']+PO['body_invoice']+PO['foot_invoice']
    f=open('./Products/templates/'+template_src,'w')

    f.write(content)
    f.close()
    template=get_template(template_src)
    pickup_details=value[0].pickup_date
    pickup_date=pickup_details.strftime('%d-%m-%Y')
    pickup_time=pickup_details.strftime('%H:%M:%S')
    dob=datetime.datetime.now()
    po_date=dob.strftime("%d-%m-%Y")
    order_header=OrderHeader.objects.using('orders').get(order_id=value[0].order_id)
    pincode=order_header.billing_pincode
    email=order_header.user_email
    s=0
    total_value=0
    total_tax=0
    for each in value:
        print each.total_vat
        total_value=float(s)+float(each.total_vat)
        total_tax=float(total_tax)+float(each.total_vat)
    in_words=num2words(total_value).capitalize()
    round_off=round(total_value,3)
    html=template.render({'round_off':round_off,'value':value,'pickup_date':pickup_date,'pickup_time':pickup_time,'po_date':po_date,'s':s,'email':email,'pincode':pincode,'sum':s,'total_value':total_value,'total_tax':total_tax,'in_words':in_words})


    head=list_id(key,value)
    doc_folder = new_folder+'/docx/'
    if not os.path.exists(doc_folder):
        os.makedirs(doc_folder)
    f=open('any.html','w')
    f.write(html)
    f.close
    b=subprocess.Popen(['prince','./any.html','-o',doc_folder+head+'.docx'])
    # b.wait()
    
    return b,doc_folder+head,head


def create_path(each,h_ob,h_id):
    print str(h_id) +'in created path'
    new_path='./po-generation/'+str(h_ob.created_date)+'/'+str(h_id)+'/'+str(datetime.date.today())
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        print 'folder_Created'
    return  new_path
        

def format(ob,file_type):

    seller_dict={}
    combination={}
    list_ob=[] 
    order_line_same=[]
    file_pdf=[]
    order_lines=[]
    new_folder={}
    for each in ob:
        print str(each.order_id)+'in loop=========>'+str(each.store_id)
        header_ob=OrderHeader.objects.using('orders').get(order_id=each.order_id)   

        if  each.order_id and len(list_ob)==0 :   
                           #For the initiation and for the first store_id 
            list_ob.append(each)       
            seller_dict[(each.store_id,each.order_id)]=list_ob
            h_id=each.order_id
            new_path=create_path(each,header_ob,h_id)
       
            print '===================> 1', new_path+'new path is here'+'----->vlist ob'+str(list_ob)
            new_folder[each.order_id]=new_path

        elif len(seller_dict) >=1 and (each.store_id,each.order_id) in seller_dict.keys() :   #For appending  Repeated objects to repeated store_ids  
            list_ob.append(each)
            seller_dict[(each.store_id,each.order_id)]=list_ob
            
            h_id=each.order_id

            new_path=create_path(each,header_ob,h_id)
            print '================> 2'+new_path+'new path is here selelr id samse'+'----->vlist ob'+str(list_ob)

            new_folder[each.order_id]=new_path

        else :
            list_ob=[] 
            list_ob.append(each)
            seller_dict[(each.store_id,each.order_id)]=list_ob
            h_id=each.order_id
            new_path=create_path(each,header_ob,h_id)
            new_folder[each.order_id]=new_path
            print '3.------------>'+str(list_ob)

    print seller_dict
    print new_folder

    
    for k,v in seller_dict.iteritems():
        l_orders=[]        
        # print k+':'+v
        # context_dict={'key':v} 
       # html_file=PO['head']+PO['body']+PO['foot']
        if type(v) is list:
            if file_type=='pdf':
                print new_folder[v[0].order_id]
                a,file_returned,head=render_to_pdf('invoice.html',str(k[0]),v,new_folder[v[0].order_id])
                a.communicate()
                a.wait()

            if file_type=='docx':
                b,file_returned,head=render_to_doc('invoice.html',str(k[0]),v,new_folder[v[0].order_id])
                b.communicate()
                b.wait()
           
            file_pdf.append(os.path.join(new_folder[v[0].order_id],file_type,head+'.'+file_type))

    return file_pdf


def  make_data(ol):
    o_name=[]
    names=OrderHeader._meta.get_all_field_names()
    for each in names:
        o_name.append('order__'+each)
    o_name = o_name + OrderLine._meta.get_all_field_names()

    o_name_set= list(ol.values(*o_name))
    print o_name,'=========================================================================\n',o_name_set
    return o_name,o_name_set
def set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value


def download_query_data(request):
    try :
        """ method to to download uploaded file as master excel with database ids in it """
        print request.GET
        selected_id=request.GET['selected_val'].split(',') if 'selected_val' in request.GET else None

       


        query_dict=request.GET
        o_name=[]

        store_id= request.GET['store_id'] if 'store_id' in query_dict else None

        status=request.GET['status__exact'] if 'status__exact'  in query_dict else None
        
        all_ob=request.GET['all'] if 'all'  in query_dict else None
        
        order_line_id=request.GET['order_line_id'] if 'order_line_id' in query_dict else None
        #For all objects i.e when all are selected 
        if all_ob=='all':   
            ol=OrderLine.objects.using('orders').all()
            o_name,o_name_set=make_data(ol)

        query_dict=dict(query_dict.iterlists())


        
        set_if_not_none(query_dict, 'status', status)
        set_if_not_none(query_dict, 'order_line_id', order_line_id)
        set_if_not_none(query_dict, 'store_id', store_id)
        if status is not None:
            del query_dict['status__exact']

        print query_dict
        if status or store_id or order_line_id is not None:

            ol=OrderLine.objects.using('orders').filter(**query_dict)
            o_name,o_name_set=make_data(ol)

        if selected_id is not None:
            ob_doc=OrderLine.objects.using('orders').filter(order_line_id__in=selected_id)
            o_name,o_name_set=make_data(ob_doc)
            print o_name


        data = {
                    'table_header': o_name,
                    'table_data': o_name_set
                }

        xlsx_data = download_as_excel(data)

        response = HttpResponse(xlsx_data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=MasterProduct.xlsx'
        response.write(xlsx_data)
        return response

    except Exception,e:
        print e

def download_as_excel(data):
    output = StringIO.StringIO()
    wb = Workbook(output)
    ws = wb.add_worksheet("Sheet 1")
    first_row = 0
    for header in data['table_header']:

        col = data['table_header'].index(header) # we are keeping order.
        if header in ['order__'+each for each in OrderHeader._meta.get_all_field_names()]:
            header=header.split('__')[1]
            header=header.replace('_',' ')
            header=header.capitalize()
            print 'header----',header
        else:
            
            header=header.capitalize()
            header=header.replace('_',' ')
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


def remarks(request):
    try:
        remark=request.POST['value'] if 'value' in request.POST else None
        old_remark=request.POST['old_value'] if 'old_value' in request.POST else None
        get_id=request.POST['id'] if 'id' in request.POST else None
        print get_id+'==========id'
        data={}
        print remark+'reamark'
        obj=OrderLine.objects.using('orders').get(order_line_id=get_id)
        data['change_from']=old_remark
        data['change_to']=remark
        data['User']=request.user
        history('Change remarks',data,get_id)
        obj.remarks=remark
        obj.save()
        return HttpResponse(json.dumps({
                'status_code': 200,
                'status_msg': 'Success'
            }))
    except Exception ,e:
        print e

class history():
    def __init__(self,action,data,order_line_id):
        date=datetime.datetime.now()
        date.strftime('%d-%m-%Y %H:%M:%S')
      


            
        OrderLine_History.objects.using('orders').create(User=data['User'],created_date=date,order_line_id=order_line_id,actions=action,change_from=data['change_from'],change_to=data['change_to'])


def overview(request):
    get=request.GET['q']
    oh=OrderHeader.objects.using('orders').get(order_id=get)
    ol=OrderLine.objects.using('orders').filter(order_id=get)
    order_id=oh.order_id
    print ol

    template = get_template("h1.html")
    return HttpResponse(template.render({'orderline':ol,'order_id':order_id,'oh':oh}))




