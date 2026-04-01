from django.core.management import call_command
from django.core.management.base import BaseCommand
from account.models import User
from faker import Faker
fake = Faker('en_US')

"""
Команда для добавления пользователей
"""

class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            '--users',
            type=int,
            default=100
        )

    def handle(self, *args, **options):
        users_count = options['users']

        self.stdout.write(f'\nСоздаем {users_count} пользователей')

        users = []
        for i in range(users_count):
            user = User.objects.create_user(
                email=fake.email(),
                password='password123',
                username=fake.user_name()
            )
            users.append(user)
        self.stdout.write(f'\nВы создали {users_count} пользователей')

        call_command('stats')