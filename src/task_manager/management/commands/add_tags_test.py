from django.core.management import call_command
from django.core.management.base import BaseCommand
from task_manager.models import Tags
from faker import Faker
fake = Faker('en_US')

"""
Команда для добавления тегов
"""

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--tags',
            type=int,
            default=5
        )

    def handle(self, *args, **options):
        tags_count = options['tags']
        self.stdout.write(f'\nСоздаем {tags_count} тегов')
        tags = []
        for i in range(tags_count):
            tag_name = fake.word()
            if Tags.objects.filter(name=tag_name).exists():
                tag_name = f"{tag_name}_{i}"
            tag, created = Tags.objects.get_or_create(name=tag_name)
            tags.append(tag)
        self.stdout.write(f'\nВы создали {tags_count} тегов')

        call_command('stats')