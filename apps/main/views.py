from rest_framework import generics
from apps.main import serializers
from apps.main.models import Countries

class CountryAirportListView(generics.ListAPIView):
    queryset = Countries.objects.prefetch_related('cities__airports').all()
    serializer_class = serializers.CountrySerializer
