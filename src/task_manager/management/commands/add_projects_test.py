from django.core.management import call_command
from django.core.management.base import BaseCommand
from task_manager.models import Projects
from faker import Faker
fake = Faker('en_US')

"""
Команда для добавления проектов
"""

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--projects',
            type=int,
            default=5
        )

    def handle(self, *args, **options):
        projects_count = options['projects']
        self.stdout.write(f'\nСоздаем {projects_count} проектов')

        projects = []
        for i in range(projects_count):
            project = Projects.objects.create(
                name=fake.company(),
                description=fake.text()
            )
            projects.append(project)

        self.stdout.write(f'\nВы создали {projects_count} проектов')

        call_command('stats')