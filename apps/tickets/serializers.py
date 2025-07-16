from rest_framework import serializers
from apps.tickets.models import  Passenger, Order
from django.db import transaction


class DirectionSerializer(serializers.Serializer):
    departure_code = serializers.CharField(max_length=3)
    arrival_code = serializers.CharField(max_length=3)
    date = serializers.DateField()

class FlightSearchSerializer(serializers.Serializer):
    directions = DirectionSerializer(many=True)
    adult_qnt = serializers.IntegerField(min_value=0)
    child_qnt = serializers.IntegerField(min_value=0)
    infant_qnt = serializers.IntegerField(min_value=0)
    class_ = serializers.CharField(source='class',default='E', required=False, max_length=1)


class RequestIdSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=36, required=True, help_text="ID запроса для получения расписания")


class PhoneSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=10)
    number = serializers.CharField(max_length=20)
    extra = serializers.CharField(max_length=10, required=False, allow_blank=True)


class DocumentSerializer(serializers.Serializer):
    document_type = serializers.CharField()
    document_number = serializers.CharField()
    document_expire = serializers.DateField()

class PassengerSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model = Passenger
        fields = ['type', 'gender', 'last_name', 'first_name', 'middle_name', 'birth_date', 'document']


class OrderRequestSerializer(serializers.ModelSerializer):
    buy_id  = serializers.CharField(max_length=36, required=True, help_text="ID рейса для покупки")
    phone = PhoneSerializer()
    emails = serializers.ListField(child=serializers.EmailField())
    passengers = PassengerSerializer(many=True)

    class Meta:
        model = Order
        fields = ['buy_id', 'phone', 'emails', 'passengers']


class OrderPaymentSerializer(serializers.Serializer):
    order_id = serializers.CharField()
    for_type = serializers.ChoiceField(choices=["avia", "hotel", "bus"])  
    currency = serializers.ChoiceField(choices=["KGS", "USD", "EUR"])   
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
