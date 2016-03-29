DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
}

INSTALLED_APPS = [
    'anonymizer',
    'anonymizer.tests',
]

SECRET_KEY = 'foo bar baz'
