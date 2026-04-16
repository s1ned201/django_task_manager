from django.db import models
from config.models import BaseModel


class Attachments(BaseModel):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Наименование'
    )

    task = models.ForeignKey(
        to='Tasks',
        related_name='attachments',
        on_delete=models.CASCADE
    )

    photo = models.ImageField(
        upload_to='attachments',
        blank=True,
        null=True,
        verbose_name='Фото'
    )


    class Meta:
        ordering = ["name"]
        db_table = "attachments"
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return self.name
