# Register your models here.

from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'created_at', 'updated_at', 'is_active')  # Show category in the list
    list_filter = ('category', 'is_active')  # Filter products by category
    search_fields = ('name', 'description')  # Enable search by name and description
    ordering = ('-created_at',)  # Order by creation date by default
    fields = ('name', 'description', 'price', 'stock', 'category', 'image', 'is_active')  # Show category field

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')  # Show basic info for categories
    list_filter = ('is_active',)  # Filter by active status
    search_fields = ('name',)  # Enable search by category name
    ordering = ('-created_at',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
