"""
Test support harness to make setup.py test work.
"""

import sys

from django.conf import settings
settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
    },
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'fack'
    ],
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    ROOT_URLCONF='fack.urls',
    SITE_ID=1
)


def runtests():
    try:
        from django import setup
        setup()
    except ImportError:
        pass
    import django.test.utils
    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True)
    failures = test_runner.run_tests(['fack'])
    sys.exit(failures)
