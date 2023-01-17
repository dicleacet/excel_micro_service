import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'Europe/Istanbul'

app.conf.beat_schedule = {
    "every_thirty_seconds": {
        "task": "account.tasks.thirty_second_func",
        "schedule": timedelta(seconds=30),
    },
}

app.autodiscover_tasks()

