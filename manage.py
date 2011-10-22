#!/usr/bin/env python
from django.core.management import execute_manager
import imp
import sys
import os



# assume 'apps' is a directory with same parent directory as us 
APPS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'apps'))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

try:
    from mainsite import settings
except ImportError:
    sys.stderr.write("Error: Can't load python module 'mainsite.settings' from the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


if __name__ == "__main__":
    execute_manager(settings)
