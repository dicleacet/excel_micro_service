from time import sleep
from celery import shared_task
from auto_variables.models import ExcelFile
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from pathlib import Path


@shared_task
def upload(id, file_url):
    print('Downloading...')
    sleep(10)
    storage = FileSystemStorage()
    path_object = Path(file_url)
    with path_object.open(mode='rb') as file:
        output_file = File(file, name=path_object.name)
        instance = ExcelFile(id=id, output_file=output_file, is_download=True)
        instance.save()
    print('Uploaded!')