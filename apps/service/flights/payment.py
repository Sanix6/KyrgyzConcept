import requests
from typing import Dict, Any


def order_payment(
    order_id: str,
    for_type: str,
    currency: str,
    total_amount: float,
    headers: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Создание платежа для заказа."""
    url = f"https://stage-api.etm-system.ru/api/air/orders/{order_id}/payment"
    payload = {
        "for_type": for_type,
        "currency": currency,
        "total_amount": total_amount         
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if response else None}


def get_payment_status(
    order_id: str,
    headers: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Получение статуса платежа для заказа."""
    url = f"https://stage-api.etm-system.ru/api/air/orders/{order_id}/payment"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if response else None}
