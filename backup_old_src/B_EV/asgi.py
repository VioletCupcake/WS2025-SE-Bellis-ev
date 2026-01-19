"""
<<<<<<<< HEAD:backup_old_src/B_EV/asgi.py
ASGI config for B_EV project.
========
ASGI config for {{ project_name }} project.
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/project_name/asgi.py-tpl

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<<< HEAD:backup_old_src/B_EV/asgi.py
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
========
https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/asgi/
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/project_name/asgi.py-tpl
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<<< HEAD:backup_old_src/B_EV/asgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'B_EV.settings')
========
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/project_name/asgi.py-tpl

application = get_asgi_application()
