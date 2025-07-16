import requests
from typing import Dict, Any
from apps.service.auth.etmlogin import get_etm_session

def get_offers(
        request_id: str,
) -> Dict[str, Any]:
    """Получение списка рейсов."""
    url = f"https://stage-api.etm-system.ru/api/air/offers/?request_id={request_id}"
    
    session = get_etm_session()
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if response else None} 


def check_offer_avail(buy_id: str,) -> Dict[str, Any]:
    """Получение деталей рейса."""
    url = f"https://stage-api.etm-system.ru/api/air/offers/{buy_id}/availability"
    session = get_etm_session()
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if response else None}
    
    

def get_order_info(order_id: str, ) -> Dict[str, Any]:
    """Получение информации о заказе."""
    url = f"https://stage-api.etm-system.ru/api/air/orders/{order_id}"

    session = get_etm_session()
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if response else None}