import logging
from django.shortcuts import render , redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category , Cart
from .serializers import ProductSerializer, CategorySerializer
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum , F
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


#### View for Add to cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_page')

  
@login_required
def Cart_page(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = cart_items.aggregate(total=Sum(F('quantity') * F('product__price')))['total'] or 0

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_amount': total_amount})


@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        
        if cart_item and quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        elif cart_item and quantity == 0:
            cart_item.delete()

    return redirect('cart_page')


@login_required
def remove_from_cart(request, product_id):
    Cart.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart_page')
