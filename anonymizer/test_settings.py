from __future__ import unicode_literals

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
}

INSTALLED_APPS = [
    'anonymizer',
    'anonymizer.tests',
]

SECRET_KEY = "x"
