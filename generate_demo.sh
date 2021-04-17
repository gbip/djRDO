#!/bin/sh
python manage.py dumpdata --natural-foreign --exclude=auth.permission --exclude=contenttypes --indent=4 > demo.json
