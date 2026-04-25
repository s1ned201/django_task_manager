#!/bin/sh

set -e

python src/manage.py migrate

python src/manage.py runserver