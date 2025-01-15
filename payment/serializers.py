import logging
from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'payment_method', 'status', 'timestamp']
        read_only_fields = ['id', 'user', 'status', 'timestamp']

    def create(self, validated_data):
        try:
            user = self.context['request'].user
            validated_data['user'] = user
            return super().create(validated_data)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating payment record: {str(e)}", exc_info=True)
            raise serializers.ValidationError("An error occurred while processing the payment.")
