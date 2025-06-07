import os
from .settings import *  # noqa: F403



DEBUG = True

INSTALLED_APPS += [  # noqa: F405
    'debug_toolbar',
]
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa: F405

ROOT_URLCONF = 'foodgram.dev_urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa: F405
    }
}

if os.getenv('IS_TEST', '').lower() not in ('true', '1'):
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (  # noqa: F405
        'rest_framework.authentication.SessionAuthentication',
    )

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: True,
}
