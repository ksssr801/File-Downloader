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

if any service creation fails, run it manually. 
Open terminal. 
Enable Env and go to source.

python3 manage.py runserver 0:80

celery -A djapi worker -l info

celery -A djapi beat -l info

