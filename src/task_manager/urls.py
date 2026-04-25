from django.contrib import admin
from django.urls import path, re_path, include
from task_manager.views import delete_attachment, download_attachment, attachment_list, create_attachment, \
    user_create, home, user_list, user_info, edit_task_form, add_comment, TaskView, \
    TaskDetailView, TaskCreateView

urlpatterns = [
    path('', home, name='home'),  # Главная страница
    path('tasks/', TaskView.as_view(), name='tasks'),  # Список задач
    path('tasks/create/', TaskCreateView.as_view(), name='create_task'), # Форма создания задач
    path('users/create/', user_create, name='user_create'), # Форма создания пользователей
    path('users/', user_list, name='user_list'), # Список пользователей
    path('users/<int:user_id>/user_info/', user_info, name='user_info'), # Информация о пользователе
    path('tasks/<int:task_id>/edit/', edit_task_form, name='edit_task_form'), # Форма редактирования задач
    path('tasks/<int:task_id>/comment/', add_comment, name='add_comment'), # Форма добавления комментария
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'), # Информация о задаче
    path('attachments/', attachment_list, name='attachment_list'), # Список вложений
    path('attachments/create/', create_attachment, name='create_attachment'), # Форма создания вложений
    path('attachments/<int:attachment_id>/delete/', delete_attachment, name='delete_attachment'), # Удаление вложений
    path('attachments/<int:attachment_id>/download/', download_attachment, name='download_attachment'), # Загрузка вложений
    path('api/', include('task_manager.v1.urls')),
    ]