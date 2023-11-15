#!/bin/sh
gunicorn api_proveedores.wsgi:application --bind 0.0.0.0:8000
