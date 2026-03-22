from django.contrib import admin
from django.urls import path, re_path

from task_manager.views import tasks, home, user

urlpatterns = [
    path('', tasks, name='tasks'),
    path('home', home, name='home'),
    path('user', user, name='user'),
]