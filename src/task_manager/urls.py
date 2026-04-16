from django.contrib import admin
from django.urls import path, re_path
from task_manager.views import tasks, create_attachment, user_create, home, user_list, create_task_form, user_info, edit_task_form, add_comment, task_detail

urlpatterns = [
    path('', tasks, name='tasks'),
    path('home', home, name='home'),
    path('create', create_task_form, name='create_task'),
    path('users/create/', user_create, name='user_create'),
    path('users/', user_list, name='user_list'),
    path('users/<int:user_id>/user_info/', user_info, name='user_info'),
    path('<int:task_id>/edit/', edit_task_form, name='edit_task_form'),
    path('<int:task_id>/comment/', add_comment, name='add_comment'),
    path('tasks/<int:task_id>/', task_detail, name='task_detail'),
    path('create_attachment', create_attachment, name='create_attachment')
]