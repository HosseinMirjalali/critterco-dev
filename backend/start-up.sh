#!/bin/bash

python3 manage.py migrate --no-input

while true; do
    python3 manage.py runserver 0.0.0.0:8000
    sleep 5s
done