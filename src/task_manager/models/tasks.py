from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from config.models import BaseModel


class TaskStatus(models.TextChoices):
    CREATED = 'CREATED'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
    FAILED = 'FAILED'

class Tasks(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Наименование'
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'

    )

    priority = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        default=5,
        verbose_name = 'Приоритетность'
    )

    status = models.CharField(
        choices=TaskStatus,
        default=TaskStatus.CREATED,
        verbose_name='Статус'
    )

    is_reopened = models.BooleanField(
        default=False,
        verbose_name='Переоткрывалась ли'
    )

    project = models.ForeignKey(
        to='Projects',
        related_name='tasks',
        on_delete=models.CASCADE,
        null=True,
    )

    assignee = models.ForeignKey(
        to="account.user",
        null=True,
        blank=True,
        related_name='tasks',
        on_delete=models.SET_NULL,
    )


    class Meta:
        ordering = ["-created_at"]
        db_table = "tasks"
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        return self.name


class EducationTasks(Tasks):
    class Meta:
        proxy = True
