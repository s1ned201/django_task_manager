from django.core.management.base import BaseCommand
from task_manager.models import Tasks, Tags, Projects, Comments
from account.models import User

"""
Счётчик количества задач, пользователей, проектов, тегов и комментариев (Статистика)
"""

class Command(BaseCommand):


    def handle(self, *args, **options):


        stats = {
            'Задачи': Tasks.objects.count(),
            'Проекты': Projects.objects.count(),
            'Комментарии': Comments.objects.count(),
            'Теги': Tags.objects.count(),
            'Пользователи': User.objects.count()
        }



        self.stdout.write('\n Статистика:')
        for key, value in stats.items():
            if value > 0:
                self.stdout.write(f'   {key}: {value:,}')
