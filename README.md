# ecommerce-api-django

## Demo

![](demo2.gif)

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

## Create admin user

In a regular prompt shell, type the following to create a super user:

```
python manage.py createsuperuser
```

Fill the create form typing:

- type ```admin``` in username field
- type ```admin@admin.com``` for email
- type ```123456``` for password
- type ```123456``` again to confirm
- type ```y``` to bypass password validation

> Note: remember to change admin's password later

Now bring the server up:

```
$ python manage.py runserver
```

And navigate to ```http://localhost:8000/admin```

Fill up login form with admin credentials we've created just now.

> Note: Now it's a good time to change admin's password.

Create more users as needed.

## Usage

Just bring the server online with this command:

```
$ source ./env/bin/activate
$ python manage.py runserver
```

And navigate to http://localhost:8000 to get access to the interactive documentation.

Steps to authenticate:

- First call ```auth``` endpoint to get authenticated.
- Copy token value from response body
- Click authorize button and fill ApiKeyAuth with token preceeded by "Token" string
- Finally click Authorize button

ApiKey Example:
```
Token 1b7c9e36b002fdfa9598e3932d56e08b52c55d67
```

CURL example:
```
curl -X GET "http://localhost:8000/api/customers/" -H  "accept: application/json" -H  "AUTHORIZATION: Token 1b7c9e36b002fdfa9598e3932d56e08b52c55d67"
```


## Unit testing

Type the following in a terminal window:

```
$ source ./env/bin/activate
$ python manage.py test api
```
