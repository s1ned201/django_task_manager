import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'task_every_3min_40sec': {
        'task': 'task_manager.tasks.add',
        'schedule': timedelta(minutes=3, seconds=40),
        'args': (),
        'kwargs': {},
        'options': {}
    },

    'task_19-21': {
        'task': 'task_manager.tasks.mul',
        'schedule': crontab(
            hour='*',
            day_of_month='19-21',
            month_of_year='*',
            day_of_week='*',
        ),
        'args': (),
        'kwargs': {},
    },
}