from django.urls import path
from .views import ProductListView, CategoryListView , Shopping_page , Cart_page , add_to_cart , update_cart , remove_from_cart

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),


    ##Html pages
    path('shopping-page/' , Shopping_page , name='shopping_page'),
    path('cart-page/' , Cart_page , name='cart_page'),
    
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update-cart/<int:product_id>/', update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    
]