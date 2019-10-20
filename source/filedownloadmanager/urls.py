from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from .views import download_file_from_url, get_file_download_status

router = DefaultRouter()
urlpatterns = router.urls
urlpatterns.append(url(r'download', download_file_from_url))
urlpatterns.append(url(r'status', get_file_download_status))
