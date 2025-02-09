# Register your models here.

from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at', 'updated_at', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    fields = ('name', 'description', 'price', 'stock', 'category', 'image', 'is_active')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('-created_at',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
