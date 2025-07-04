import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update-etm-token-every-5-minutes': {
        'task': 'apps.service.auth.etmlogin.update_etm_token',
        'schedule': 300.0,  
    },
}