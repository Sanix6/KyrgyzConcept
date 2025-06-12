from rest_framework import serializers

class DirectionSerializer(serializers.Serializer):
    departure_code = serializers.CharField(max_length=3)
    arrival_code = serializers.CharField(max_length=3)
    date = serializers.DateField()

class FlightSearchSerializer(serializers.Serializer):
    directions = DirectionSerializer(many=True)
    adult_qnt = serializers.IntegerField(min_value=0)
    child_qnt = serializers.IntegerField(min_value=0)
    infant_qnt = serializers.IntegerField(min_value=0)
    class_ = serializers.CharField(source='class', max_length=1)
    airlines = serializers.ListField(
        child=serializers.CharField(max_length=10), required=False
    )
    providers = serializers.ListField(
        child=serializers.IntegerField(), required=False
    )

class RequestIdSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=36, required=True, help_text="ID запроса для получения расписания")


class EtmLoginSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=100, required=True, help_text="Логин для входа в ETM")
    password = serializers.CharField(max_length=100, write_only=True, required=True, help_text="Пароль для входа в ETM")


class PhoneSerializer(serializers.Serializer):
    code = serializers.CharField()
    number = serializers.CharField()
    extra = serializers.CharField(allow_blank=True, required=False)

class AddressSerializer(serializers.Serializer):
    zip = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    additional = serializers.CharField()

class DocumentSerializer(serializers.Serializer):
    type = serializers.CharField()
    number = serializers.CharField()
    expire = serializers.DateField()

class PassengerSerializer(serializers.Serializer):
    type = serializers.CharField()
    gender = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    birth_date = serializers.DateField()
    citizenship = serializers.CharField()
    document = DocumentSerializer()
    frequent_numbers = serializers.ListField(child=serializers.CharField(), required=False)

class OrderRequestSerializer(serializers.Serializer):
    buy_id = serializers.CharField()
    phone = PhoneSerializer()
    emails = serializers.ListField(child=serializers.EmailField())
    address = AddressSerializer()
    passengers = PassengerSerializer(many=True)
