#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py populate_math_courses
python manage.py createsuperuser --noinput || true
python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); u=User.objects.filter(username='mojo').first(); u.set_password('Mojo2023@@@') or u.save() if u else None; print('Password reset!' if u else 'User not found')"
