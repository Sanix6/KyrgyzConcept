import requests
from typing import List, Dict, Any
from apps.service.auth.etmlogin import get_etm_session

API_URL = "https://stage-api.etm-system.ru"


from datetime import date

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