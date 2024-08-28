#!/bin/sh

python manage.py migrate

# collects all static files in our app and puts it in the STATIC_ROOT
python manage.py collectstatic --noinput

daphne -b 0.0.0.0 -p 8000 feed.asgi:application