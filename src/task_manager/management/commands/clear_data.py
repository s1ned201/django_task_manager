
from django.core.management.base import BaseCommand
from account.models import User
from task_manager.models import Tasks, Tags, Projects, Comments

"""
Команда для удаления всех данных
"""

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-users',
            action='store_true'
        )
        parser.add_argument(
            '--yes',
            action='store_true'
        )

    def handle(self, *args, **options):
        keep_users = options['keep_users']
        auto_yes = options['yes']

        if not auto_yes:
            confirm = input('Вы уверены, что хотите удалить все данные? (y/N): ')
            if confirm.lower() != 'y':
                self.stdout.write('Операция отменена')
                return

        Comments.objects.all().delete()
        Tasks.objects.all().delete()
        Projects.objects.all().delete()
        Tags.objects.all().delete()

        if not keep_users:
            User.objects.exclude(is_superuser=True).delete()

        self.stdout.write(self.style.SUCCESS('\n Очистка завершена!'))