#!/bin/bash
#This file is to create the service file for Downloader
INSTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCEDIR="$(dirname "$INSTDIR")"

#Taking Input from user for creating Downloader Celery Beat service
echo ""
echo "Please provide name for creating Downloader Celery Beat Service (Default: 'celerybeatservice')."
echo ""
read -p "Service Name: " servicevar
servicevar=${servicevar:-celerybeatservice}

# Creating service file for Downloader Celery Beat Service
rm -rf /usr/lib/systemd/system/$servicevar.service

cat >> /usr/lib/systemd/system/$servicevar.service <<EOF
[Unit]
Description=Downloader Celery Beat Service
Wants=NetworkManager-wait-online.service network.target network-online.target dbus.service
After=NetworkManager-wait-online.service network-online.target

[Service]
Type=Simple
WorkingDirectory=$SOURCEDIR

LimitNOFILE=660000
LimitNPROC=660000

OOMScoreAdjust=-1000
# Pid file for the downloader process
PIDFile=$SOURCEDIR/eve_clry_beat_pid

# Give a reasonable amount of time for the server to start up/shut down
ExecStart=$SOURCEDIR/celery_beat.sh
TimeoutSec=180
# KillMode=none

[Install]
WantedBy=multi-user.target
EOF

chmod +x $SOURCEDIR/celery_beat.sh
systemctl enable $servicevar.service
service $servicevar start
echo ""
echo "/usr/lib/systemd/system/$servicevar.service"
echo "Downloader Celery Beat Service Created - '$servicevar'"
echo ""
