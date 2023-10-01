#!/bin/sh

gunicorn ljj_muebles.wsgi:application --bind 0.0.0.0:8000
