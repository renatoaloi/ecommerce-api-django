# ecommerce-api-django

## Demo

![](demo2.gif)


## Setting up the environment

If you will, you can raise up a Ubuntu's docker container to host all that stuff, and yet expose 8000 port

```
$ docker run -it --rm -p 8000:8000 ubuntu /bin/bash
```

And install the basic software:

> Requires: Python 3.8

```
$ apt-get update
$ apt-get install -y git python3.8 python3.8-venv python3-venv python3-pip
$ python3.8 -m pip install --upgrade pip
```

## Clone the repo

Clone this Git repository and navigate to the cloned folder

```
$ git clone https://github.com/renatoaloi/ecommerce-api-django.git
$ cd ecommerce-api-django
```

Create an virtual environment and install requirements.

```
$ python3.8 -m venv env
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

or if you are inside a docker container, you could use:

```
$ python manage.py runserver 0.0.0.0:8000
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

## CI Deploy

Created as an Github's Action

```
https://github.com/renatoaloi/ecommerce-api-django/actions
```

Check for CI pipeline's configurations in the file ```.github/workflows/django.yml```

Remember creating Github's secret variables to reflect your AWS credentials:

```
AWS_ACCESS_KEY_ID=ABCDEDEDEDDDCCCBBAAA
AWS_SECRET_ACCESS_KEY=******
AWS_DEFAULT_REGION=us-west-2
AWS_ACCOUNT_ID=938748374387
```

Configure also subnets and other AWS' configurations in the file ```config.json```


## Manual Deploy

Create a group log in AWS CloudWatch named:

```
/ecs/first-run-task-definition
```

Configure the following environment variables replacing with values of your own:

```
$ export AWS_ACCESS_KEY_ID=ABCDEDEDEDDDCCCBBAAA
$ export AWS_SECRET_ACCESS_KEY=******
$ export AWS_DEFAULT_REGION=us-west-2
$ export AWS_ACCOUNT_ID=938748374387
$ export ENV=hml
```

Where ```hml``` is the stage parameter

Run the ```ci.sh``` script passing the stage as parameter:

```
$ sudo apt-get install -y jq
$ sudo pip3 install awscli
$ aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
$ aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
$ eval $( aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION )
$ bash ./infra/ci.sh "$ENV" "$AWS_ACCOUNT_ID" "$AWS_DEFAULT_REGION"
```
