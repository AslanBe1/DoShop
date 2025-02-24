from import_export import resources
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

from shops.models import Product, ProductImages, Category, Attribute, AttributeValue, ProductAttribute, Comment

# Register your models here.

# admin.site.register(Product)

admin.site.site_header = "Shop's Admin"
admin.site.site_title = "Welcome To Admin Page"
admin.site.index_title = "Welcome To Admin Page"


@admin.register(Product)
class ProductModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'price','rating','quantity','description','discount','image_tag')
    search_fields = ('name', 'price')
    list_filter = ('quantity','price','rating')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:50px; max-height:50px"/>'.format(obj.image.url))
        return ''

    image_tag.short_description = 'Image'


admin.site.register(ProductImages)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
admin.site.register(Comment)