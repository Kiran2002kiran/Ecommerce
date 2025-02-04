from django.urls import path
from .views import DeliveryListView , Delivery_page
urlpatterns = [
    path('delivery_list/', DeliveryListView.as_view(), name='delivery-list'),

    path('delivery-page/' , Delivery_page , name='delivery_page'),
]