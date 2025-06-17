from celery import shared_task
import requests
from django.conf import settings

import requests
from .token import get_etm_token, get_etm_cookies, set_etm_token

ETM_API_URL = "https://stage-api.etm-system.ru"
ETM_LOGIN = "KyrgyzConcept_api"
ETM_PASSWORD = "Conceptapi.007"

@shared_task
def update_etm_token():
    session = requests.Session()

    url = f"{ETM_API_URL}/api/login"
    data = {
        "login": settings.ETM_LOGIN,
        "password": settings.ETM_PASSWORD,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    response = session.post(url, data=data, headers=headers)
    response.raise_for_status()

    token = response.json().get("etm_auth_key")
    cookies = session.cookies.get_dict()

    set_etm_token(token, cookies)



def get_etm_session():
    token = get_etm_token()
    cookies = get_etm_cookies()

    if not token or not cookies:
        raise ValueError("Отсутствует токен.")

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    session.cookies.update(cookies)

    return session

