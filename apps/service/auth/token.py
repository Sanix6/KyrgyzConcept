import redis
from django.conf import settings

redis_client = redis.StrictRedis.from_url(settings.REDIS_URL)
ETM_TOKEN_KEY = "etm_auth_key"

def set_etm_token(token: str):
    redis_client.setex(ETM_TOKEN_KEY, 6 * 3600, token)

def get_etm_token():
    token = redis_client.get(ETM_TOKEN_KEY)
    return token.decode() if token else None
