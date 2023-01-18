from time import sleep
from celery import shared_task
from auto_variables.models import ExcelFile
from django.core.files import File
from requests import get


@shared_task
def upload(excel_id, file_url):
    print('Downloading...')
    sleep(10)
    response = get(file_url)
    with open(file_url.split('/')[-1], 'wb') as file:
        file.write(response.content)
    with open('output.xlsx', 'rb') as file:
        output_file = File(file, name='output.xlsx')
        instance = ExcelFile.objects.get(id=excel_id, file=output_file, is_download=True)
        instance.save()
    print('Downloaded')
