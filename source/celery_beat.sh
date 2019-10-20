#!/bin/sh

/opt/DownloaderEnv/bin/celery -A djapi beat -l debug --max-interval=10
