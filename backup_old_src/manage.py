#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
<<<<<<<< HEAD:backup_old_src/manage.py
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'B_EV.settings')

========
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
>>>>>>>> 0b52654533ecf9fcbf72db0f036853091f0262c0:venv/lib/python3.12/site-packages/django/conf/project_template/manage.py-tpl
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
