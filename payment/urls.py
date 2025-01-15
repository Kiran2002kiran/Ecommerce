from django.urls import path
from .views import PaymentListView , PaymentCreateView

urlpatterns = [
    path('', PaymentListView.as_view(), name='payment-list'),
    path('create/', PaymentCreateView.as_view(), name='payment_create'),
]