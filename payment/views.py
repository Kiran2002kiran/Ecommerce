import logging
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer

logger = logging.getLogger(__name__)

class PaymentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if not request.user.is_staff:
                return Response({"error": "You are not authorized to view payments."}, status=status.HTTP_403_FORBIDDEN)
            
            payments = Payment.objects.all()
            serializer = PaymentSerializer(payments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching payments: {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while fetching payments."}, status=500)

class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = PaymentSerializer(data=request.data, context={"request": request})
            if serializer.is_valid():
                payment = serializer.save(user=request.user)
                return Response({
                    "message": "Payment done successfully!",
                    "payment": PaymentSerializer(payment).data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while creating the payment."}, status=500)
