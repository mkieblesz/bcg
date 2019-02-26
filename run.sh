#!/bin/bash

if [ "$DEBUG" = "True" ]; then
    # ensure postgres is started
    exec ./wait_for_db.sh python manage.py runserver 0.0.0.0:8001
    echo "Django development server started"
else
    # ensure postgres is started
    exec ./wait_for_db.sh uwsgi --ini uwsgi.ini
    echo "Uwsgi server started"
fi
