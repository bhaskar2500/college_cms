from supplified.models import MasterImportUpload
from xlrd import open_workbook
from django.http import *

class MasterImportExport(object):
    def __init__(self):
        pass

    def temp(self, data):
        error_list = data[:20]
        return error_list
