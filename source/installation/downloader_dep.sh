#!/bin/sh
INSTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $INSTDIR
SOURCEDIR="$(dirname "$INSTDIR")"
echo $SOURCEDIR

python3 -m venv DownloaderEnv
source DownloaderEnv/bin/activate
echo "Virtual environment (DownloaderEnv) has been created"
echo ""
echo "Installing the Python dependencies"
DownloaderEnv/bin/pip3 install --upgrade pip
chmod +x requirement.sh
./requirement.sh
echo ""
echo "All Python dependencies has been installed"

cd $SOURCEDIR
chmod +x downloader.sh
chmod +x celery_worker.sh
chmod +x celery_beat.sh
DownloaderEnv/bin/python3 manage.py makemigrations
DownloaderEnv/bin/python3 manage.py migrate

cd $INSTDIR
chmod +x createdownloaderservice.sh
echo -n "Install Downloader Service. Type "n" if Apache HTTPD. (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then
    echo ""
    ./createdownloaderservice.sh
else
    echo ""
    echo "Downloader service can be created seperately by executing 'createwebportalservice.sh' from installation folder."
    echo ""
fi

cd $INSTDIR
chmod +x createceleryworkerservice.sh
echo -n "Install Downloader Celery Worker Service. (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then
    echo ""
    ./createceleryworkerservice.sh
else
    echo ""
    echo "Downloader Celery Worker service can be created seperately by executing 'createceleryworkerservice.sh' from installation folder."
    echo ""
fi

cd $INSTDIR
chmod +x createcelerybeatservice.sh
echo -n "Install Downloader Celery Beat Service. (y/n)? "
read answer
if echo "$answer" | grep -iq "^y" ;then
    echo ""
    ./createcelerybeatservice.sh
else
    echo ""
    echo "Downloader Celery Beat service can be created seperately by executing 'createcelerybeatservice.sh' from installation folder."
    echo ""
fi

echo ""
echo "****************** All Configured ******************"
echo ""

