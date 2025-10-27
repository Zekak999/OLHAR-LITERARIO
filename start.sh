#!/bin/bash
cd olhar_literario_django
exec gunicorn olhar_literario_django.wsgi:application --bind 0.0.0.0:$PORT
