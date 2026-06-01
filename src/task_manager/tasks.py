from celery import shared_task
from datetime import datetime

@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def send_sunrise_greeting():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"☀️ Доброе утро! Желаю продуктивного дня! (Время отправки: {current_time})"
    print(message)
    return f"Greeting sent at {current_time}"

"""
Задачу с сообщением на восходу солнца, настраивал через shell,
через вот эти команды:

from django_celery_beat.models import SolarSchedule, PeriodicTask
from datetime import datetime, timedelta
solar_schedule, created = SolarSchedule.objects.get_or_create(
    event='sunrise',
    latitude=55.7558,
    longitude=37.6176,
)
periodic_task, created = PeriodicTask.objects.get_or_create(
    name='Send a good morning greeting every sunrise',
    defaults={
        'task': 'task_manager.tasks.send_sunrise_greeting',
        'solar': solar_schedule,
        'enabled': True,
        'one_off': False,
    }
)
if created:
    print('OK!')
else:
    print("ERROR")
"""