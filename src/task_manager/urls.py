from django.contrib import admin
from django.urls import path, re_path
from task_manager.views import tasks, home, user_list, create_task_form, user_info

urlpatterns = [
    path('', tasks, name='tasks'),
    path('home', home, name='home'),
    path('create', create_task_form, name='create_task'),
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/user_info/', user_info, name='user_info'),
]