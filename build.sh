#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser --noinput || true

# create superuser automatically
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="shazin").exists():
    User.objects.create_superuser("shazinlk", "admin@gmail.com", "slk123")
END