from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, RegisterSerializer
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as DjangoUser
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.contrib.auth import logout
import datetime
import logging



logger = logging.getLogger(__name__)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.debug(f"Received data: {request.data}")
        serializer = RegisterSerializer(data=request.data) 
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return redirect('login_page')
        logger.warning(f"Registration failed: {serializer.errors}")
        return render(request , 'user/register.html' , {'errors':'serializers.error'})
    
    def get(self,request):
        return render(request,'user/register.html') 



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        # print(f"Received Username: {username}, Password: {password}")

        if not username or not password:
            return JsonResponse({'success': False, 'message': 'Username and password are required'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        
        if user and user.is_active:
            login(request, user)
            return JsonResponse({'success': True, 'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password.'}, status=401)

    def get(self, request):
        return render(request, 'user/login.html')



            
class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)



def Index(request):
    return render(request,'user/index.html')


def register_page(request):
    return render(request, 'user/register.html')


def login_page(request):
    return render(request, 'user/login.html')

def Logout(request):
    logout(request)
    return redirect('index')


####Forget password....

# Render Forgot Password Page
def forgot_password(request):
    if request.method == 'GET':
        return render(request, 'user/forgotpass.html')
    

otp_storage = {}
@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({"error": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email)
            
            # Generate a secure OTP (alphanumeric for extra security)
            otp = get_random_string(6, allowed_chars='0123456789')
            
            # Store OTP with expiration time (5 minutes)
            otp_storage[email] = {
                "otp": otp,
                "expires_at": datetime.datetime.now() + datetime.timedelta(minutes=5)
            }
            
            # Send email with OTP
            send_mail(
                'Password Reset OTP',
                f'Your OTP for password reset is: {otp}. This OTP is valid for 5 minutes.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return JsonResponse({"message": "OTP sent successfully. Please check your email."}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "No user found with this email."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')

        if not email or not otp or not new_password:
            return JsonResponse({"error": "Email, OTP, and new password are required."}, status=400)

        # Validate OTP
        otp_data = otp_storage.get(email)
        if not otp_data:
            return JsonResponse({"error": "No OTP found for this email."}, status=400)

        # Check OTP expiration
        if otp_data["expires_at"] < datetime.datetime.now():
            del otp_storage[email]  # Remove expired OTP
            return JsonResponse({"error": "OTP has expired. Please request a new one."}, status=400)

        # Validate OTP match
        if otp_data["otp"] != otp:
            return JsonResponse({"error": "Invalid OTP."}, status=400)

        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            
            del otp_storage[email]  # Clear OTP after successful reset
            return JsonResponse({"message": "Password reset successful."}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)

