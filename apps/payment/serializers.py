from rest_framework import serializers
from .models import MkassaPayment

class MkassaPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MkassaPayment
        fields = ['id', 'user', 'payment_id', 'amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
