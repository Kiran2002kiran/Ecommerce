from django.urls import path
from .views import ProductListView, CategoryListView , Shopping_page

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),


    ##Html pages
    path('shopping-page/' , Shopping_page , name='shopping_page'),
]