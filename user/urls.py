from django.urls import path
from.import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView , UserProfileView , LoginView , register_page, login_page , forgot_password , send_otp , reset_password

urlpatterns = [
    path('',views.Index,name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),


    # HTML page endpoints
    path('register-page/', register_page, name='register_page'),
    path('login-page/', login_page, name='login_page'),
    # FORGETPASS ENDPOINTS
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('send-otp/', send_otp, name='send_otp'),
    path('reset-password/', reset_password, name='reset_password'),
]


