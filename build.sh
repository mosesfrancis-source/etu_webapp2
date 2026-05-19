#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='mojo').exists():
    u = User.objects.create_superuser('mojo', 'mosesfrancis783@gmail.com', 'Mojo2023@@@')
    u.role = 'admin'
    u.save(update_fields=['role'])
    print('Superuser created')
else:
    print('Superuser already exists')
"
