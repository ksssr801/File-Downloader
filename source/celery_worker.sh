#!/bin/sh

DownloaderEnv/bin/celery -A djapi worker -l info
