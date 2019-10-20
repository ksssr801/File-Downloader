#!/bin/bash
#This file is to create the service file for Downloader
INSTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCEDIR="$(dirname "$INSTDIR")"

#Taking Input from user for creating Downloader service
echo ""
echo "Please provide name for creating Downloader Service (Default: 'portal')."
echo ""
read -p "Service Name: " servicevar
servicevar=${servicevar:-portal}

# Creating service file for Downloader Service
rm -rf /usr/lib/systemd/system/$servicevar.service

cat >> /usr/lib/systemd/system/$servicevar.service <<EOF
[Unit]
Description=Downloader
Wants=NetworkManager-wait-online.service network.target network-online.target dbus.service
After=NetworkManager-wait-online.service network-online.target

[Service]
Type=simple
WorkingDirectory=$SOURCEDIR

LimitNOFILE=660000
LimitNPROC=660000
OOMScoreAdjust=-1000

ExecStart=$SOURCEDIR/downloader.sh

TimeoutSec=300

[Install]
WantedBy=multi-user.target
EOF

echo "$SOURCEDIR"

chmod +x $SOURCEDIR/downloader.sh
systemctl enable $servicevar.service
service $servicevar start
echo ""
echo "/usr/lib/systemd/system/$servicevar.service"
echo "Downloader Service Created - '$servicevar'"
echo ""

