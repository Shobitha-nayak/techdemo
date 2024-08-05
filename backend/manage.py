# manage.py

import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockmonitoring.settings')
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if 'runserver' in sys.argv:
        from backend.scheduler import start_scheduler
        start_scheduler()

if __name__ == '__main__':
    main()