from django.core.management.base import BaseCommand
from django.core.management import call_command
from account.models import User
from task_manager.models import Tasks, Tags, Projects, Comments
from faker import Faker
import random
from task_manager.models.tasks import TaskStatus
fake = Faker('en_US')

"""
Команда для добавления задач
(default=5  |  --tasks)
"""

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--tasks',
            type=int,
            default=5
        )

    def handle(self, *args, **options):

        tasks_count = options['tasks']

        self.stdout.write(f'\nСоздаем {tasks_count} задач и присваиваем им теги')

        statuses = [
            TaskStatus.CREATED,
            TaskStatus.STARTED,
            TaskStatus.COMPLETED,
            TaskStatus.CANCELED,
            TaskStatus.FAILED
        ]
        priorities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        users = list(User.objects.all())
        projects = list(Projects.objects.all())
        tags = list(Tags.objects.all())

        tasks = []
        for i in range(tasks_count):
            task = Tasks.objects.create(
                name=fake.sentence(nb_words=5)[:64],
                description=fake.text() if random.random() > 0.5 else '',
                status=random.choice(statuses),
                priority=random.choice(priorities),
                assignee=random.choice(users),
                project=random.choice(projects)
            )

            task.tags.set(random.sample(tags, random.randint(1, 3)))
            tasks.append(task)

        self.stdout.write(f'\nКомментируем... Почти готово!!!')
        for task in tasks:
            if random.random() < 0.3:
                for _ in range(random.randint(1, 5)):
                    Comments.objects.create(
                        task=task,
                        user=random.choice(users),
                        message=fake.text(max_nb_chars=128)
                    )
        self.stdout.write(f'\nПоздравляю, вы успешно создали {tasks_count} задач')
        call_command('stats')