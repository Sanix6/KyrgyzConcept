import json
import requests
from typing import List, Dict, Any

API_URL = "https://stage-api.etm-system.ru"

def create_order(
    buy_id: str,
    phone: Dict[str, str],
    emails: List[str],
    address: Dict[str, str],
    passengers: List[Dict[str, Any]]
) -> requests.Response:
    
    url = f"{API_URL}/api/air/search"
    
    payload = {
        "buy_id": buy_id,
        "phone": phone,
        "emails": emails,
        "address": address,
        "passengers": passengers
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload, default=str), headers=headers)
    response.raise_for_status()
    return response
