from rest_framework import serializers
from apps.main.models import Airports, Cities, Countries
from django.db import transaction


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airports
        fields = ['id', 'name', 'code_name']


class CitySerializer(serializers.ModelSerializer):
    airports = AirportSerializer(many=True, read_only=True)

    class Meta:
        model = Cities
        fields = ['id', 'name', 'code_name', 'airports']


class CountrySerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Countries
        fields = ['id', 'name', 'code_name', 'img', 'cities']
