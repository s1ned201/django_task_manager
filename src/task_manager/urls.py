from django.contrib import admin
from django.urls import path, re_path

from task_manager.views import task, home, user

urlpatterns = [
    path('', task, name='tasks'),
    path('home', home, name='home'),
    path('user', user, name='user'),
    # re_path(r'^details/(?P<task>[0-9]{4})/$', index_2),
]