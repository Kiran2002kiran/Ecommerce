from django.urls import path
from .views import PaymentListView , PaymentCreateView , Payment_page

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment_create'),


    path('payment-page/', Payment_page, name='payment_page'),
]