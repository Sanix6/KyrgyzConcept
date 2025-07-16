from pathlib import Path
import os
from datetime import timedelta
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ww$(jy9$)7hra5(i1^1#wxfqig)w6odg%l4c!=c=05fput4'

DEBUG = True

ALLOWED_HOSTS = ["*"]

# ──────────────────────────────── #
#               APPS              #
# ──────────────────────────────── #

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # DRF и сторонние
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'django_prometheus',
    'django_celery_beat',
    'drf_yasg',

    # Аутентификация и OAuth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # приложения
    'apps.main',
    'apps.user',
    'apps.payment',
    'apps.tickets',
]

SITE_ID = 1

# ──────────────────────────────── #
#            MIDDLEWARE           #
# ──────────────────────────────── #

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ──────────────────────────────── #
#             DATABASE            #
# ──────────────────────────────── #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ──────────────────────────────── #
#           AUTH BACKENDS         #
# ──────────────────────────────── #

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'user.User'

# ──────────────────────────────── #
#       REST FRAMEWORK & JWT      #
# ──────────────────────────────── #

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# ──────────────────────────────── #
#              CORS               #
# ──────────────────────────────── #

CORS_ALLOW_METHODS = ("GET", "OPTIONS", "PATCH", "POST", "PUT", "DELETE")
CORS_ALLOW_ALL_ORIGINS = True  # на время разработки

CSRF_TRUSTED_ORIGINS = ["http://*"]

# ──────────────────────────────── #
#        GOOGLE AUTH CONFIG       #
# ──────────────────────────────── #

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        }
    }
}

ACCOUNT_AUTHENTICATION_METHOD = 'phone'
ACCOUNT_SIGNUP_FIELDS = {
    'phone': {'required': True},
    'first_name': {'required': True},
    'last_name': {'required': True},
    'email': {'required': False},
    'password1': {'required': True},
    'password2': {'required': True},
}
ACCOUNT_LOGIN_METHODS = ['phone']
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

REST_AUTH = {
    'LOGIN_SERIALIZER': 'apps.user.serializers.LoginSerializer',
    'REGISTER_SERIALIZER': 'apps.user.serializers.RegisterSerializer',
}

# ──────────────────────────────── #
#             STATIC              #
# ──────────────────────────────── #

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────── #
#              TIME               #
# ──────────────────────────────── #

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────── #
#              CELERY             #
# ──────────────────────────────── #

REDIS_URL = "redis://localhost:6379/0"
CELERY_BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = REDIS_URL

# ──────────────────────────────── #
#               EMAIL             #
# ──────────────────────────────── #

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nurtileksatinbaev1@gmail.com'
EMAIL_HOST_PASSWORD = 'gmys sswd ybpt zvhz'  # лучше брать из переменных окружения
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ──────────────────────────────── #
#               API               #
# ──────────────────────────────── #

FLIGHTS_API_URL = os.getenv("FLIGHTS_API_URL")
ETM_API_URL = os.getenv("ETM_API_URL")
ETM_LOGIN = os.getenv("ETM_LOGIN")
ETM_PASSWORD = os.getenv("ETM_PASSWORD")
