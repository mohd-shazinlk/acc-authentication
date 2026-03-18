#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# create superuser automatically
python manage.py shell << END
from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.create_superuser('shazin', 'admin@gmail.com', 'slk123')
END