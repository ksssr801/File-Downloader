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
    resp = requests.get(file_url, stream=True)
    total = resp.headers.get('content-length')
    with open(file_location, 'wb') as f:
        if total is None:
            f.write(resp.content)
        else:
            downloaded = 0
            total = int(total)
            total_file_size = str(round((int(total)/1024)/1024, 2)) + ' MB'
            for data in resp.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done_percent = (100*downloaded)/total
                done_percent_str = str(round(done_percent, 2)) + ' %'
                done_size = (done_percent * total)/100
                done_size_str = str(round((int(done_size)/1024)/1024, 2)) + ' MB'
                rem_size = ((100 - done_percent) * total) / 100
                rem_size_str = str(round((int(rem_size)/1024)/1024, 2)) + ' MB'
                current_task.update_state(state='PROGRESS',
                    meta={
                        'file_name': file_location,
                        'status': done_percent_str,
                        'file_size': total_file_size,
                        'downloaded_file_size': done_size_str,
                        'remaining_file_size': rem_size_str,
                    })


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def download_file_from_url(request):
    file_id = ''
    file_size = 0
    msg = ''
    file_location = ''
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
                file_id = download_job.id
                file_size = int(resp.headers.get('content-length'))
                new_file_obj = FileDownloads(file_id=file_id, name=file_location, file_url=url, file_size=file_size, isdeleted=False)
                new_file_obj.save()
            except requests.exceptions.ConnectionError:
                msg = 'Please check your Internet Connection or URL might not be reachable.'
            except requests.exceptions.MissingSchema:
                msg = 'Please check the URL ! It might be wrong.'
            except requests.exceptions.InvalidURL:
                msg = 'Please check the URL ! It might be wrong.'
    return Response({'file_id': file_id, 'url': url, 'is_url_msg': msg, 'file_name':file_location}, template_name='download_file_template.html')

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@renderer_classes([TemplateHTMLRenderer])
def get_file_download_status(request):
    file_url = ''
    file_name = ''
    file_size = ''
    file_id = request.GET.get('id', '')
    if file_id:
        file_obj = FileDownloads.objects.values('name', 'file_size').filter(file_id=file_id)
        if file_obj:
            file_name = file_obj[0].get('name', '')
            total_file_size = file_obj[0].get('file_size', None)
            file_size = str(round((int(total_file_size)/1024)/1024, 2)) + ' MB'
        job = AsyncResult(file_id)
        job_state = job.state
        job_details = {}
        if job_state == 'SUCCESS':
            FileDownloads.objects.filter(file_id=file_id).update(isdeleted=True)
            job_details = {
                'status': 'Completed!',
                'file_name': file_name,
                'file_id': file_id,
                'file_size': file_size,
            }
        elif job_state == 'PENDING':
            job_details = {'msg': 'Check the Provided File Id. It might be wrong!'}
        else:
            job_details = job.result
            if job_state == 'PROGRESS':
                job_details.update({'file_id': file_id})
            elif job_state == 'STARTED':
                job_details.update({'status': 'Starting...', 'file_id': file_id, 'file_size': file_size})
            else:
                job_details.update({'status': job_state, 'file_id': file_id, 'file_size': file_size})
        return Response(job_details, template_name='get_status_template.html')
    else:
        return Response({'msg': 'Provide File Id to get status.'}, template_name='get_status_template.html')
    
