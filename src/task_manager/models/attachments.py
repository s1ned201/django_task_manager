import os
from django.db import models
from config.models import BaseModel
from django.core.validators import FileExtensionValidator


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

    file = models.FileField(
        upload_to='attachments',
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    'jpg',
                    'jpeg',
                    'png',
                    'gif',
                    'pdf',
                    'doc',
                    'docx',
                    'txt'
                ]
            )
        ],
        verbose_name='Файл'
    )


    class Meta:
        ordering = ["name"]
        db_table = "attachments"
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

    def get_file_type(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        file_types = {
            '.jpg': 'image', '.jpeg': 'image', '.png': 'image', '.gif': 'image',
            '.pdf': 'pdf', '.doc': 'word', '.docx': 'word',
            '.txt': 'text'
        }
        return file_types.get(ext, 'file')

    def is_image(self):
        return self.get_file_type() == 'image'
