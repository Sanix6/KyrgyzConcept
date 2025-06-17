import redis
import pickle
from django.conf import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)

ETM_TOKEN_KEY = "etm_auth_key"
ETM_COOKIES_KEY = "etm_cookies"

def set_etm_token(token: str, cookies: dict):
    redis_client.setex(ETM_TOKEN_KEY, 6 * 3600, token)
    redis_client.setex(ETM_COOKIES_KEY, 6 * 3600, pickle.dumps(cookies))

def get_etm_token():
    token = redis_client.get(ETM_TOKEN_KEY)
    return token.decode() if token else None

def get_etm_cookies():
    cookies = redis_client.get(ETM_COOKIES_KEY)
    return pickle.loads(cookies) if cookies else None
