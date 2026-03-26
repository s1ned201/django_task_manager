from django.db import models
from config.models import BaseModel
# from account.models import User


class Projects(BaseModel):
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

    owner = models.ForeignKey(
        to="account.user",
        related_name="projects",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        ordering = ["-created_at"]
        db_table = "projects"
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name

