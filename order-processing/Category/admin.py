from django.contrib import admin
from Category.models import *
from django.utils.safestring import mark_safe
from multidbconfig import MultiDBModelAdmin, MultiDBTabularInline

# Register your models here.
class CategoryAdmin(MultiDBModelAdmin):
    def has_add_permission(self, request):
        return False

    fields = ('category_name', 'parent_category_id', 'level', 'is_deleted', 'status', 'image_form', 'cat_pro_img')
    list_display = ('category_id', 'category_name', 'level', 'parent_category_id','image_tag')
    readonly_fields = ('image_form',)
    search_fields = ('category_name',)

    def image_form(self, obj):
	if obj.cat_pro_img:
	        return mark_safe('<img src="http://www.supplified.com/admin/catproductimages/%s" />'%obj.cat_pro_img.url)
	else:
		return ""
    image_form.short_description = 'Category Image'
    image_form.allow_tags = True

admin.site.register(Category, CategoryAdmin)
