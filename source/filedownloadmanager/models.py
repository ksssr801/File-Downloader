from __future__ import unicode_literals
from django.db import models

class FileDownloads(models.Model):
    file_id = models.CharField(primary_key=True, max_length=500)
    name = models.CharField(max_length=500, blank=True)
    file_url = models.CharField(max_length=1000)
    file_size = models.IntegerField(blank=True, null=True)
    isdeleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'tbl_file_downloads'
