import requests
from typing import Dict, Any


def get_order_info(
        order_id: str,  
        headers: Dict[str, str] = None
) -> Dict[str, Any]:
    """Получение информации о заказе."""
    url = f"https://stage-api.etm-system.ru/api/air/orders/{order_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e), "status_code": response.status_code if response else None}