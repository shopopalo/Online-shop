from django.contrib import admin
from .models import Category, Product
from parler.admin import TranslatableAdmin


class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    # используя TranslatableAdmin указание prepopulated_fields
    # возможно только так
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']

    # используя TranslatableAdmin указание prepopulated_fields
    # возможно только так
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)
