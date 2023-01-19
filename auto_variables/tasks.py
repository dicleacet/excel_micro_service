from celery import shared_task
from auto_variables.models import ExcelFile
from django.core.files import File
from requests import get
from auto_variables.utils import AutoVariable


@shared_task
def generate_download(file_id, file_url):
    instance = ExcelFile.objects.get(id=file_id)
    response = get(file_url)
    print(file_url)
    with open(file_url.split('/')[-1], 'wb') as file:
        file.write(response.content)
    with open(file_url.split('/')[-1], 'rb') as file:
        output_file = File(file, name='output.xlsx')
        instance.file = output_file
        instance.is_download = True
        instance.save()


@shared_task
def info_file(file_id):
    instance = ExcelFile.objects.get(id=file_id)
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
    instance.data = info_list
    instance.is_finished = True
    instance.save()
