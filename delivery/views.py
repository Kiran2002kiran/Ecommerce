from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Delivery
from .serializers import DeliverySerializer
from django.shortcuts import render

class DeliveryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        deliveries = Delivery.objects.filter(is_active=True)
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)


def Delivery_page(request):
    return render(request,'delivery/delivery.html')