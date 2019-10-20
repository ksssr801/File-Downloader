from rest_framework import serializers

from filedownloadmanager.models import FileDownloads

class FileDownloadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDownloads
        fields = '__all__'