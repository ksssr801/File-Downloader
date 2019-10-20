#!/bin/sh
source DownloaderEnv/bin/activate
start()
{
DownloaderEnv/bin/python3 manage.py runserver 0.0.0.0:8080 --noreload
}
start

