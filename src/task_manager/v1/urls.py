from django.urls import path
from task_manager.v1.views.task import TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='tasks_list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task_detail'),
]