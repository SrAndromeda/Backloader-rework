#!/bin/sh

if [ ! -f "database/db.sqlite3" ]; then
    echo "Error: 'db.sqlite3' not found, creating new one...."
    touch db.sqlite3
    python3 manage.py migrate
fi

nginx && daphne backloader.asgi:application --port 8000 --bind 0.0.0.0
