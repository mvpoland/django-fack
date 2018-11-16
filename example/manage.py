#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

try:
    import fack
except ImportError:
    sys.stderr.write("django-fack isn't installed; trying to use a source checkout in ../fack.")
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\n"
                     "You'll have to run django-admin.py, passing it your settings module.\n"
                     "(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
