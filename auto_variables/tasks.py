from celery import shared_task
from auto_variables.models import ExcelFile
from django.core.files import File
import requests
from auto_variables.utils import AutoVariable
from app.settings import BASE_DIR
from django.core.files.base import ContentFile

dir_path = BASE_DIR / 'media/excel_files'


@shared_task
def generate_download(instance):
    response = requests.get(instance.file_url)
    file_name = instance.file_url.split('/')[-1]
    mem_file = ContentFile(response.content, name=file_name)
    instance.file.save(file_name, mem_file, save=False)
    instance.is_download = True
    instance.save()
    return instance


@shared_task
def info_file(instance):
    infos, numerics = AutoVariable(instance.file).info_file()
    info_list = []
    for num in numerics:
        info_list.append({
            'name': num,
            'categorical': False,
            'open_ended': False,
            'numeric': True,
        })
    for key, alias in infos.items():
        if alias:
            info_list.append({
                'name': key,
                'categorical': True,
                'open_ended': False,
                'numeric': False,
            })
        else:
            info_list.append({
                'name': key,
                'categorical': False,
                'open_ended': True,
                'numeric': False,
            })
    instance.is_finished = True
    instance.save()
    return info_list
