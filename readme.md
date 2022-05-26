 # SOFTDESK app

The SOFTDESK app is a back-end solution aiming at helping users to manage projects and their dependencies (issues, comments, contributions, etc…).

Based on DJANGO REST FRAMEWORK, this app provides a collection of endpoints that the users would be able to access to from different devices and apps.

This app should be secured so that only authenticated users with the right permissions could use it.

## Installation

Below the instructions will be given to properly proceed to the needed packages installing.

### Virtual environment configuration

**Install the virtual environment package**

```bash
pip install virtualenv
```

**Create the virtual environment**

```bash
virtualenv localdir
```

You must specify the local directory path

**Activate the virtual environment**

Mac OS/Linux
```bash 
source localdir/bin/activate
```

Windows
```bash
localdir/Scripts/activate
```

### Install the necessary packages

All necessary packages are contained in the requirements.txt.
```bash
asgiref==3.5.0
async-timeout==4.0.2
authentication==1.1.0
certifi==2021.10.8
charset-normalizer==2.0.12
click==8.1.2
colorama==0.4.4
coreapi==2.3.3
coreschema==0.0.4
Deprecated==1.2.13
Django==4.0.3
django-filter==21.1
django-icons==21.3
django-widget-tweaks==1.4.12
djangorestframework==3.13.1
djangorestframework-simplejwt==5.1.0
drf-yasg==1.20.0
flake8==4.0.1
flake8-html==0.4.1
Flask==2.1.1
idna==3.3
importlib-metadata==4.11.2
inflection==0.5.1
itsdangerous==2.1.2
itypes==1.2.0
Jinja2==3.0.3
Markdown==3.3.6
MarkupSafe==2.1.0
mccabe==0.6.1
packaging==21.3
passlib==1.7.4
Pillow==9.0.1
pycodestyle==2.8.0
pycryptodome==3.14.1
pyflakes==2.4.0
Pygments==2.11.2
PyJWT==2.3.0
pyparsing==3.0.8
pytz==2022.1
redis==4.2.2
requests==2.27.1
ruamel.yaml==0.17.21
ruamel.yaml.clib==0.2.6
sqlparse==0.4.2
tzdata==2021.5
uritemplate==4.1.1
urllib3==1.26.9
Werkzeug==2.1.1
wrapt==1.14.0
WTForms==3.0.1
zipp==3.7.0
```

Install them all by running the following command in terminal.
```bash
pip install -r requirements.txt
```

## Usage

### Run the server

Open your terminal and run the following command:
```bash
python .\softdesk\manage.py runserver
```

### Test the APIs

Once the terminal command is executed, you can test the endpoints through different ways

#### Use the Postman collection

Follow the link below.
```bash
https://go.postman.co/workspace/New-Team-Workspace~23c58d19-ba3e-4393-97fe-d94ea4106519/collection/20673323-5a378156-87a0-4d0f-9407-8ffe486edc68?action=share&creator=20673323
```

#### Use Swagger

Follow the link below.
```bash
http://127.0.0.1:8000/swagger/
```

## Flake8 set-up and checks

### Flake 8 configuration

In the project directory, create a file as follows:
```bash
setup.cfg
```

In this file, write the following:
```bash
[flake8]
max-line-length = 119
exclude = venv, __init__.py, *.txt, *.csv, *.md
```
We restrict the maximum number of characters per line at 119. So flake8 won't consider as errors a line as long as it
has fewer characters.
We exclude from the flake8 checks the followings:
- Our virtual environment libraries
- Our packages init files
- Our requirement file
- Our readme file
- Our CSV databases
- Our migrations files


### Execute flake8 report

In case the user requests a regular flake8 check on the terminal, proceed as follows:
```bash
flake8 path/to/project/directory
```

In case a html reporting is preferred, proceed as follows:
```bash
flake8 --format=html --htmldir=flake-report
```