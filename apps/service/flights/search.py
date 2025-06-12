import requests
from typing import List, Optional
from datetime import date
from django.conf import settings
from apps.service.auth.etmlogin import get_etm_session
from apps.service.auth.token import set_etm_token, get_etm_token


API_URL = "https://stage-api.etm-system.ru"

def search_flights(
    departure_code: str,
    arrival_code: str,
    travel_date: date,
    adult_qnt: int = 1,
    child_qnt: int = 0,
    infant_qnt: int = 0,
    travel_class: str = "E",
    airlines: Optional[List[str]] = None,
    providers: Optional[List[int]] = None,
    timeout: int = 10
) -> dict:
    session = get_etm_session()

    payload = {
        "directions": [
            {
                "departure_code": departure_code,
                "arrival_code": arrival_code,
                "date": travel_date.isoformat()
            }
        ],
        "adult_qnt": adult_qnt,
        "child_qnt": child_qnt,
        "infant_qnt": infant_qnt,
        "class": travel_class,
    }

    if airlines:
        payload["airlines"] = airlines
    if providers:
        payload["providers"] = providers

    url = f"{API_URL}/api/air/search"
    response = session.post(url, json=payload, timeout=timeout)

    response.raise_for_status()
    return response.json()

    

def get_schedule(request_id: str) -> dict:
    url = f"{API_URL}/api/air/schedule"
    token = get_etm_session()

    payload = {
        "request_id": request_id
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        with requests.Session() as session:
            session.headers.update(headers)
            response = session.post(url, json=payload, timeout=10)
            print("Status Code:", response.status_code)
            print("Response Text:", response.text)
            response.raise_for_status()
            return response.json()

    except requests.RequestException as e:
        raise RuntimeError(f"Ошибка при получении расписания: {e}")
    except ValueError:
        raise ValueError("Неправильный JSON ответ от расписания API.")