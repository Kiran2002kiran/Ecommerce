import logging
from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.contrib.auth.decorators import login_required

logger = logging.getLogger('shop')

class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while fetching products."}, status=500)

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while fetching categories."}, status=500)



@login_required
def Shopping_page(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'shop/shopping.html', {'products': products})