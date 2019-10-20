#!/bin/sh
source /opt/DownloaderEnv/bin/activate
start()
{
/opt/DownloaderEnv/bin/python3 manage.py runserver 0.0.0.0:9001 --noreload
}
start

