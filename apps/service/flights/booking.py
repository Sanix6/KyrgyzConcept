import requests
from typing import List, Dict, Any
from datetime import date
from apps.service.auth.etmlogin import get_etm_session
from rest_framework import status


API_URL = "https://stage-api.etm-system.ru"

def serialize_for_json(data: Any) -> Any:
    if isinstance(data, dict):
        return {k: serialize_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_for_json(i) for i in data]
    elif isinstance(data, date):
        return data.isoformat()  
    else:
        return data

def create_order(
    buy_id: str,
    phone: Dict[str, str],
    emails: List[str],
    address: Dict[str, str],
    passengers: List[Dict[str, Any]]
) -> requests.Response:
    session = get_etm_session()

    url = f"{API_URL}/api/air/orders"

    payload = {
        "buy_id": buy_id,
        "phone": phone,
        "emails": emails,
        "address": address,
        "passengers": passengers
    }

    payload = serialize_for_json(payload)

    response = session.post(url, json=payload)
    response.raise_for_status()
    return response


def cancel_order(
    order_id: str,
    headers: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Отмена заказа."""
    url = f"https://stage-api.etm-system.ru/api/air/orders/{order_id}/void"
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "error": str(e),
            "status_code": response.status_code if response else status.HTTP_500_INTERNAL_SERVER_ERROR
        }