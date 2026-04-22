import os
import urllib.request
from django.core.files.base import ContentFile
from task_manager.models import Attachments


def save_file_from_url(url, task, name=None):
    try:
        response = urllib.request.urlopen(url)
        file_content = response.read()

        if not name:
            name = os.path.basename(url)

        content_file = ContentFile(file_content, name=name)
        attachment = Attachments(
            task=task,
            name=name,
        )
        attachment.file.save(name, content_file, save=True)
        return attachment
    except Exception as e:
        print(f"Ошибка загрузки файла: {e}")
        return None