#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
# python manage.py collectstatic   收集静态文件
# nohup gunicorn root.asgi:application --workers 2 --worker-class uvicorn.workers.UvicornWorker -b 127.0.0.1:8000 > template.out 2>&1 &


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed and "
                          "available on your PYTHONPATH environment variable? Did you "
                          "forget to activate a virtual environment?") from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
