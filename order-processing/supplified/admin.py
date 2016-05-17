from django.contrib import admin
from supplified.models import MasterImportUpload
import json
from django.utils.safestring import mark_safe

class MasterImportUploadAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    """
    def has_change_permission(self, request, obj=None):
        if obj is not None and True:
            return False
        return super(MasterImportUploadAdmin, self).has_change_permission(request, obj=obj)
    """
    list_display = ('id', 'ref_text', 'process_name', 'process_type',\
      'uploaded_on', 'applied', 'applied_on_production', 'download_excel_link')
    list_filter = ('process_name','process_type','uploaded_on', 'applied', 'applied_on_production')
    fields = ('file_name', 'ref_text', 'process_name', 'process_type', 'uploaded_on',\
         'applied_on', 'query', 'sql_errors_table', 'error', 'applied', 'applied_on_production', 'discarded_on',\
         'user', 'applied_ids', 'sync_query', 'sql_sync_errors_table')
    readonly_fields = ('sql_errors_table', 'user', 'uploaded_on', 'applied_on',\
        'file_name', 'ref_text', 'process_name', 'process_type', 'applied_ids', 'discarded_on', 'sql_sync_errors_table')
    search_fields = ('id', 'file_name', 'ref_text')

    def download_excel_link(self, obj):
        link = '<a href="/admin/download_file?file_id=%s">%s</a>'%(obj.id, obj.file_name)
        return mark_safe(link)

    def sql_errors_table(self, obj):
        sql_error = json.loads(obj.sql_error)
        if sql_error:
            html = '<table class="table table-striped table-bordered table-hover table-condensed" style="width: 90%;">' +\
                '<tr><th>SQL query Errors </th></tr>';
            for err in sql_error:
                html += '<tr><td>%s</td></tr>'%(err['errors'][0]['text'])
            html += '</table>'
            return mark_safe(html)
        else:
            return ""
    sql_errors_table.short_description = 'Sql Errors (Testing)'
    sql_errors_table.allow_tags = True

    def sql_sync_errors_table(self, obj):
        sql_error = json.loads(obj.sync_errors)
        if sql_error:
            html = '<table class="table table-striped table-bordered table-hover table-condensed" style="width: 90%;">' +\
                '<tr><th>SQL Sync Production query Errors </th></tr>';
            for err in sql_error:
                html += '<tr><td>%s</td></tr>'%(err)
            html += '</table>'
            return mark_safe(html)
        else:
            return ""
    sql_sync_errors_table.short_description = 'Sync Sql Errors (Production)'
    sql_sync_errors_table.allow_tags = True

    def applied_ids(self, obj):
       try:
          query = json.loads(obj.download_query)
       except Exception, e:
          return ""
       if query:
            html = '<table class="table table-striped table-bordered table-hover table-condensed" style="width: 90%;">' +\
                '<tr><th>Column Name</th><th>Ids</th></tr>';
            for key, val in query.items():
                html += '<tr><td>%s</td><td>%s</td></tr>'%(key, [str(c) for c in val])
            html += '</table>'
            return mark_safe(html)
       else:
            return ""
    applied_ids.short_description = 'Download Query ids'
    applied_ids.allow_tags = True

admin.site.register(MasterImportUpload, MasterImportUploadAdmin)
