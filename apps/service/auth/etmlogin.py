from celery import shared_task
import requests
from django.conf import settings
from .token import set_etm_token, get_etm_token


@shared_task
def update_etm_token():
    url = f"{settings.ETM_API_URL}/api/login"
    data = {
        "login": settings.ETM_LOGIN,
        "password": settings.ETM_PASSWORD,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    token = response.json().get("etm_auth_key")
    set_etm_token(token)


def get_etm_session():
    token = get_etm_token()
    if not token:
        raise ValueError("Токен недействителен.")
    
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    return session