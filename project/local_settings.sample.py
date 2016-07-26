# coding: utf-8
import os

DEBUG = False
SECRET_KEY = '123'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.abspath('/data'), 'db.sqlite3')

    }
}

ALLOWED_HOSTS = ['*']
