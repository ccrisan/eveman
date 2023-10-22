
## About

A small demo project to manage events. It allows:
 - user registration
 - user login
 - event creation, listing & editing
 - event attendance

The project is built with Django 4.2 and runs well on Python 3.11.

The rest API functionality (HTTP requests/responses/endpoints, serialization) is written using Django Rest Framework.

The Authentication mechanism is designed around JWT tokens and is built with `djangorestframework-simplejwt`.

API schema generation and documentation is built with `drf-spectacular`, including Open API 3.0 specs, Swagger and Redoc.

Most of the codebase (including models, logic, serializers, etc) is structured in a Django app called `api`.


## Install

Developed & tested with python 3.11. run the following commands:

    git clone https://github.com/ccrisan/eveman.git
    cd eveman
    virtualenv .venv && source .venv/bin/activate
    pip install -r requirements.txt


## Setup DB

The database used in this demo is a simple Sqlite3 file.

Create initial DB structure:

    touch eveman.sqlite3
    ./manage.py makemigrations
    ./manage.py migrate

Optionally, create a default admin user (use your desired password):

    ./manage.py createsuperuser --email admin@example.com --username admin


## Run Server

    ./manage.py runserver 0.0.0.0:8000


## API Calls

Use the following commands to test the various available API calls.

### Register User

    curl -X POST -H "Content-Type: application/json" \
         -d '{"username": "user1", "password": "deadbeef", "password2": "deadbeef", "first_name": "User", "last_name": "One", "email": "user1@example.com"}' \
        http://localhost:8000/api/register/ | jq

### Login

    curl -X POST -H "Content-Type: application/json" \
         -d '{"username": "user1", "password": "deadbeef"}' \
        http://localhost:8000/api/token/ | jq

### Refresh Token

    curl -X POST -H "Content-Type: application/json" \
         -d '{"refresh":"<refresh_token_from_above>"}' \
         http://localhost:8000/api/token/refresh/ | jq

### Create Event

    curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" \
         -d '{"name": "event1", "description": "description1", "moment": "2008-09-10T11:12:13"}' \
         http://localhost:8000/api/events/ | jq

### Edit Event

    curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" \
         -d '{"description": "updated description1"}' \
         http://localhost:8000/api/events/1/

### List All Events

    curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/ | jq

### List My Events

    curl -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/my/ | jq

### Register Attendance

    curl -X PUT -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/1/attendance/

### Unregister Attendance

    curl -X DELETE -H "Authorization: Bearer <access_token>" http://localhost:8000/api/events/1/attendance/


## Running Tests

To run the tests, simply do:

    ./manage.py test
