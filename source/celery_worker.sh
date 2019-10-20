#!/bin/sh

/opt/DownloaderEnv/bin/celery -A djapi worker -l info
