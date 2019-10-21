# File-Downloader
Download file using any download URL to your system. Implemented using Django, Celery and Redis.


> System Requirement and How to. 

Need to be linux machine (I don't have idea how the dependency script will behave in Windows.)
Python3 and venv must be installed.

---------------------------------------------
As code in Django and Python3, it will run in any system after running the requirement.sh under a virtual environment. 
File location - source/installation/requirement.sh

To run celery manually:

Go to source folder of your code. 

celery -A djapi worker -l info

celery -A djapi beat -l info

OR

Open terminal. 

Go to source/installation/

chmod +x downloader_dep.sh

./downloader_dep.sh

downloader service must be running if not run using:

service <service-name> start

if any service creation fails, run it manually. 
Open terminal.(3 different terminals need to be opened.)
Enable Env and go to source.

python3 manage.py runserver 0:9001

celery -A djapi worker -l info

celery -A djapi beat -l info


> How to use it.

After running the app.
Go to browser and write URL localhost:9001/myapi/download

Using two URLs for the app:

localhost:9001/myapi/download

localhost:9001/myapi/status

It will download the file in the source folder.
