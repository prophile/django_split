from django import setup
from django.conf import settings
from django.core.management import call_command

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_split',
        'tests',
    ),
)

setup()

call_command('migrate')
