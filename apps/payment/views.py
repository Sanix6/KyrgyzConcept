from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.service.mkassa.createpay import (
    mkassa_login,
    mkassa_create_payment,
    mkassa_check_payment
)
from apps.payment.models import MkassaPayment


class MKassaLoginView(APIView):

    def post(self, request):
        response = mkassa_login()
        return Response(response.json(), status=response.status_code)


class MKassaCreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_amount = request.data.get("payment_amount")
        products = request.data.get("products", [])

        if not payment_amount:
            return Response({"error": "payment_amount обязателен"}, status=status.HTTP_400_BAD_REQUEST)

        token = None
        if hasattr(request, 'auth') and request.auth:
            token = request.auth.key

        response = mkassa_create_payment(token, payment_amount, products)

        if response.status_code == 200:
            data = response.json()
            payment_id = data.get("payment_id") or data.get("id")  # Подкорректируй под реальный ключ

            if payment_id:
                MkassaPayment.objects.create(
                    user=request.user,
                    payment_id=payment_id,
                    amount=payment_amount,
                    status="created"
                )

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Не удалось получить ID платежа"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(response.json(), status=response.status_code)


class MKassaCheckPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        token = None
        if hasattr(request, 'auth') and request.auth:
            token = request.auth.key

        response = mkassa_check_payment(token, payment_id)

        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)


class MkassaCallbackView(APIView):

    permission_classes = [AllowAny]  #

    def post(self, request):
        data = request.data
        payment_id = data.get('payment_id') or data.get('id')
        status_mkassa = data.get('status')

        if not payment_id or not status_mkassa:
            return Response({"error": "payment_id и status обязательны"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = MkassaPayment.objects.get(payment_id=payment_id)
        except MkassaPayment.DoesNotExist:
            return Response({"error": "Платеж не найден"}, status=status.HTTP_404_NOT_FOUND)

        payment.status = status_mkassa
        payment.save()


        return Response({"status": "ok"}, status=status.HTTP_200_OK)
