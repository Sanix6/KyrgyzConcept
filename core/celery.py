import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()



app.conf.beat_schedule = {
    "refresh-etm-token-every-6-hours": {
        "task": "apps.service.auth.etmlogin.update_etm_token",
        "schedule": crontab(minute=0, hour='*/6'),
    },
}