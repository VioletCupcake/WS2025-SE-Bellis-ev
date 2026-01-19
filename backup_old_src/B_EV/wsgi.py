"""
<<<<<<<< HEAD:backup_old_src/B_EV/wsgi.py
WSGI config for B_EV project.
========
WSGI config for {{ project_name }} project.
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/project_name/wsgi.py-tpl

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<<< HEAD:backup_old_src/B_EV/wsgi.py
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
========
https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/wsgi/
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/project_name/wsgi.py-tpl
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<<< HEAD:backup_old_src/B_EV/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'B_EV.settings')
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/project_name/wsgi.py-tpl

application = get_wsgi_application()
