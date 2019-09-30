#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# This is needed to be able to use blender modules
# Example -> blender --background --python /app/manage.py shell

# global_python_modules = [
#     '/app',
#     '/usr/lib/python3.7 ./blender',
#     '/usr/local/lib/python37.zip',
#     '/usr/local/lib/python3.7',
#     '/usr/local/lib/python3.7/lib-dynload',
#     '/usr/local/lib/python3.7/site-packages',
# ]

# sys.path.extend(global_python_modules)

# Taking out not known blender parameters
sys.argv = [arg for arg in sys.argv if arg not in ['blender', '--background', '--python']]


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vortex.settings')
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
