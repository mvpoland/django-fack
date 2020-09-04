#
# A minimal settings file that ought to work out of the box for just about
# anyone trying this project. It's deliberately missing most settings to keep
# everything simple.
#
# A real app would have a lot more settings. The only important bit as far as
# django-FAQ is concerned is to have `faq` in INSTALLED_APPS.
#

import os

PROJECT_DIR = os.path.dirname(__file__)
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory;',
    }
}

SITE_ID = 1
SECRET_KEY = 'c#zi(mv^n+4te_sy$hpb*zdo7#f7ccmp9ro84yz9bmmfqj9y*c'
ROOT_URLCONF = 'example.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug': DEBUG,
        },
    }
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'fack',
)

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
