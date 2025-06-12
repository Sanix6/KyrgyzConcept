from django.shortcuts import render


#rest_framework
from rest_framework import status, generics, views
from rest_framework.response import Response
import requests


from . import serializers
from apps.service.flights import search, booking
from apps.service.auth.etmlogin import get_etm_session


class SearchFlightsView(generics.GenericAPIView):
    """Поиск по авиабилетам."""
    serializer_class = serializers.FlightSearchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        direction = data['directions'][0]

        result = search.search_flights(
            departure_code=direction['departure_code'],
            arrival_code=direction['arrival_code'],
            travel_date=direction['date'],
            adult_qnt=data['adult_qnt'],
            child_qnt=data['child_qnt'],
            infant_qnt=data['infant_qnt'],
            travel_class=data['class'],
            airlines=data.get('airlines'),
            providers=data.get('providers'),
        )
        
        return Response(result, status=status.HTTP_200_OK)
    

class GetScheduleView(generics.GenericAPIView):
    """Получение расписания по request_id запроса."""
    serializer_class = serializers.RequestIdSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_id = serializer.validated_data['request_id']
        
        try:
            result = search.get_schedule(request_id)
            return Response(result, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"Ошибка": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class EtmLoginView(generics.GenericAPIView):
    """Вход в ETM."""
    serializer_class = serializers.EtmLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login = serializer.validated_data['login']
        password = serializer.validated_data['password']

        try:
            result = get_etm_session(login, password)
            return Response(result, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"Ошибка": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"Ошибка": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class CreateOrderView(generics.GenericAPIView):
    serializer_class = serializers.OrderRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            api_response = booking.create_order(
                buy_id=data["buy_id"],
                phone=data["phone"],
                emails=data["emails"],
                address=data["address"],
                passengers=data["passengers"]
            )
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(api_response.json(), status=api_response.status_code)