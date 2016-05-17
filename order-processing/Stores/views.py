from django.shortcuts import render_to_response
from Stores.models import *
from django.db import connection
from Category.models import Category
from django.template import RequestContext
from xlsxwriter import Workbook
import StringIO
import json
from django.http import HttpResponse
from django.db.models import Q




def store_bulk_update(request):
    return render_to_response("common_bulk_upload.html", {
            'page_header': 'Store Price',
            'process_name': 'Store Price Mapping',
            'process_type': [
                    #{'text': 'Create', 'value': 'create'},
                    {'text': 'Create/Update', 'value': 'c_u'},
                ],
            'action_url': '/admin/upload'
        }, context_instance=RequestContext(request))






