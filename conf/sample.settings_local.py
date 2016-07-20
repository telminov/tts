import os
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '123'

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.abspath('/data'), 'db.sqlite3')

    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/static/'
WAV_TMP_DIR = 'wavs_tmp'

WAV_STORAGE_DIR = 'generated_wav/%d-%m-%Y/'