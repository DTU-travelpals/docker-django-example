import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app: Celery = Celery(os.getenv("COMPOSE_PROJECT_NAME", "hello"))
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

if (app.configured):
    print(f'${app.conf}')
