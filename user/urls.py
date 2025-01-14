from django.urls import path
from .views import RegisterView, ObtainTokenView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', ObtainTokenView.as_view(), name='token'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
