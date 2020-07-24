# ecommerce-api-django

## Clone the repo

Clone this Git repository and navigate to the cloned folder

```
$ git clone https://github.com/renatoaloi/ecommerce-api-django.git
$ cd ecommerce-api-django
```

## Setting up the environment

Create an virtual environment and install requirements.

> Required: Python 3

```
$ virtualenv env
$ source ./env/bin/activate
$ pip install -r requirements.txt
```

## Apply migrations

> The database used is a local SqlLite3 file. If the file ```db.sqlite3``` does not exist yet, don't worry, it will be created automatically.

Run the following command to create database structure:

```
$ python manage.py migrate
```

## Usage

Just bring the server online with this command:

```
$ source ./env/bin/activate
$ python manage.py runserver
```

And navigate to http://localhost:8000/api to list endpoints and REST methods available.

## Unit testing

Type the following in a terminal window:

```
$ source ./env/bin/activate
$ python manage.py test api
```
