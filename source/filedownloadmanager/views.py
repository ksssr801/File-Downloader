from time import sleep
from celery import task, current_task
from celery.result import AsyncResult
from filedownloadmanager.models import FileDownloads
from .serializers import FileDownloadsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
import requests


@task()
def file_downloader(file_url, file_location):
    print (">>>>>>>>>>>>",file_url, file_location,"<<<<<<<<<<<<")
    resp = requests.get(file_url, stream=True)
    total = resp.headers.get('content-length')
    with open(file_location, 'wb') as f:
        if total is None:
            f.write(resp.content)
        else:
            downloaded = 0
            total = int(total)
            total_file_size = round((int(total)/1024)/1024, 2)
            for data in resp.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                sleep(0.1)
                downloaded += len(data)
                f.write(data)
                done_percent = (100*downloaded)/total
                done_size = done_percent * total
                rem_size = (100 - done_percent) * total
                current_task.update_state(state='PROGRESS',
                    meta={
                        'done_percent': done_percent,
                    })


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def download_file_from_url(request):
    file_id = ''
    file_size = 0
    msg = ''
    url = request.GET.get('url', '')
    if url:
        file_id_exist = FileDownloads.objects.values('file_id').filter(file_url=url)
        if file_id_exist:
            file_id = file_id_exist[0].get('file_id', '')
        else:
            try:
                resp = requests.get(url, stream=True)
                file_location = url[url.rfind('/')+1:]
                download_job = file_downloader.delay(url, file_location)
                print ("download_job==>",download_job, type(download_job.id))
                file_id = download_job.id
                file_size = int(resp.headers.get('content-length'))
                new_file_obj = FileDownloads(file_id=file_id, file_url=url, file_size=file_size)
                new_file_obj.save()
            except requests.exceptions.ConnectionError:
                msg = 'Please check the URL ! It might be wrong.'
            except requests.exceptions.MissingSchema:
                msg = 'Please check the URL ! It might be wrong.'
    return Response({'file_id': file_id, 'url': url, 'is_url': msg}, template_name='download_file_template.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def get_file_download_status(request):
    file_url = ''
    file_id = request.GET.get('id', '')
    print (file_id, type(file_id))
    if file_id:
        job = AsyncResult(file_id)
        job_state = job.state
        job_details = job.result
        print ("job_details==>",job.state, job.result)
        return Response({'status': job.result.get('done_percent', None), 'file_id': file_id}, template_name='get_status_template.html')
    else:
        return Response({'msg': 'Provided File Id to get status.'}, template_name='get_status_template.html')
    
