from django.shortcuts import render


#rest_framework
from rest_framework import status, generics, views
from rest_framework.response import Response
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter


from . import serializers
from apps.service.flights import search, booking, payment, order
from apps.service.common import save
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
        )
        
        return Response(result, status=status.HTTP_200_OK)
    

@extend_schema(parameters=[OpenApiParameter("order_id",str,OpenApiParameter.PATH,description="ID заказа (order_id)")],)
class GetOrderInfoView(views.APIView):
    """Получение информации о заказе по order_id."""

    def get(self, request, order_id, *args, **kwargs):
        try:
            result = order.get_order_info(order_id)
            return Response(result, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


@extend_schema(parameters=[OpenApiParameter("buy_id", str, OpenApiParameter.PATH, description="ID конкретного рейса (buy_id)")],)
class CheckOfferAvailiblityView(views.APIView):
    """Получение деталей рейса по buy_id."""
    def get(self, request, buy_id, *args, **kwargs):
        try:
            result = order.check_offer_avail(buy_id)
            return Response(result, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"Ошибка": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(parameters=[OpenApiParameter("order_id", str, OpenApiParameter.PATH, description="ID конкретного заказа")],)
class CancelOrderView(views.APIView):
    """Отмена заказа."""
    def get(self, request, order_id, *args, **kwargs):
        try:
            api_response = booking.cancel_order(order_id)
            return Response(api_response, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


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
                passengers=data["passengers"]
            )
            api_data = api_response.json()
        except requests.RequestException as e:
            return Response({"error": f"Ошибка при обращении к API: {str(e)}"},
                            status=status.HTTP_502_BAD_GATEWAY)

        save.save_booking(api_data)

        return Response(api_data, status=api_response.status_code)
    

class OrderPaymentView(generics.GenericAPIView):
    serializer_class = serializers.OrderPaymentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        order_id = data['order_id']
        headers = get_etm_session().headers

        try:
            api_response = payment.order_payment(
                order_id=order_id,
                for_type=data['for_type'],
                currency=data['currency'],
                total_amount=data['total_amount'],
                headers=headers
            )
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(api_response, status=status.HTTP_200_OK)
    


class OrderStatusView(views.APIView):
    """Получение статуса заказа."""
    def get(self, request, order_id, *args, **kwargs):
        headers = get_etm_session().headers
        
        try:
            api_response = payment.get_payment_status(order_id=order_id, headers=headers)
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(api_response, status=status.HTTP_200_OK)
    

@extend_schema(parameters=[OpenApiParameter(name="request_id",type=str,location=OpenApiParameter.QUERY,required=True,)],)
class GetOffersView(views.APIView):
    """Получение списка рейсов по request_id (через query-параметр)."""

    def get(self, request, *args, **kwargs):
        request_id = request.query_params.get("request_id")
        if not request_id:
            return Response({"error": "Параметр request_id обязателен."}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            result = order.get_offers(request_id)
            return Response(result, status=status.HTTP_200_OK)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

