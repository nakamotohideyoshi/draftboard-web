from os import environ
from sys import stdout
from unipath import Path

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)


# Application constants
# ----------------------------------------------------------

# Constant definitions
PROJECT_ROOT = Path(__file__).ancestor(3)
STATIC_ROOT = PROJECT_ROOT.child('collected_static')
INTERNAL_IPS = ()

import os

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT   = os.path.dirname(os.path.realpath(__file__))

from os.path import join

#
# Django 1.8 removed TEMPLATE_DIRS. It is now TEMPLATES = {}
# https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/
# TEMPLATE_DIRS = ( PROJECT_ROOT.child('templates'), )
TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [
            join(BASE_DIR, 'account/templates'),
            join(BASE_DIR, 'prize/templates'),
            join(BASE_DIR, 'salary/templates'),
            join(BASE_DIR,  'mysite/templates'),
        ],
        'APP_DIRS': True, # defaults to False
        'OPTIONS' : {
            'context_processors' : (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request',
                'cash.withdraw.context_processors.model_badges',
            )
        }
    },
]

# Folder locations
STATICFILES_DIRS = (
    PROJECT_ROOT.child('static'),
)

# Templates
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Testing mode by default
DEBUG = True
# Match template debugging to what environment debug is
TEMPLATE_DEBUG = DEBUG

# session uses redis and postgres to create cached db
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Static assets, served via django-whitenoise
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/'

# Redirects to same URL with end slash if it can't find the page
APPEND_SLASH = True

# Only allow site to be hosted on our domain
ALLOWED_HOSTS = ['.rio-dfs.herokuapp.com', '*.rio-dfs.herokuapp.com', ]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9^1kzl5mo3pfgy1f402)27s*jz=s00^#rtznm_2)i!tkz7s-ed'

# Where to start looking for URL definitions
ROOT_URLCONF = 'mysite.urls'

# CORS requests for OAuth
CORS_ORIGIN_ALLOW_ALL = True


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
# ----------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Third party settings
# ----------------------------------------------------------

# cachalot cache
CACHALOT_CACHE = 'cachalot'

# Use Pipeline for static asset management
STATICFILES_STORAGE = 'mysite.storage.WhitenoisePipelineStorage'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_JS = {
    # 'lib': {
    #     'source_filenames': (
    #         'js/lib/moment.js',
    #         'js/lib/jsnlog.js',
    #         'js/lib/modernizr-2.8.3.js',
    #         'js/lib/pagedown/Markdown.Converter.js',
    #         'js/lib/pagedown/Markdown.Sanitizer.js',
    #         'js/lib/pagedown/Markdown.Editor.js',
    #         'js/lib/angular/angular.js',
    #         'js/lib/angular/angular-animate.min.js',
    #         'js/lib/angular/angular-route.min.js',
    #         'js/lib/angular/angular-resource.min.js',
    #         'js/lib/angular/angular-cookies.min.js',
    #         'js/lib/rioplayer/rioplayer.1.0.0.js',
    #         'js/lib/ui-bootstrap/ui-bootstrap-modal-0.10.0.js',
    #         'js/lib/ui-bootstrap/ui-bootstrap-modal-tpls-0.10.0.js',
    #         'js/lib/socket.io.js',
    #     ),
    #     'output_filename': 'js/lib.js',
    # },
}

#
##########################################################################
#        cash -Withdrawal Rules
##########################################################################
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT          = 100.00
DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO      = 750.00

#
##########################################################################
#        django_braintree
##########################################################################
import braintree
BRAINTREE_MERCHANT      = 'xh2x3fhngf3nnkk5'
BRAINTREE_PUBLIC_KEY    = 'th4fw4rpz3rhn8bq'
BRAINTREE_PRIVATE_KEY   = '9122b2a8557887e27a6de0da7221a7d7'
BRAINTREE_MODE          = braintree.Environment.Sandbox
from braintree import Configuration, Environment

Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT,     # sandbox BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

# REST currently defaulting to session authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    #     # 'rest_framework.renderers.BrowsableAPIRenderer',  # use for testing by browser
    # ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE' : 50,

}


# Django installs
# ----------------------------------------------------------
INSTALLED_APPS = (
    # heroku installs
    'raven.contrib.django.raven_compat',

    #'suit',

    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # testing this out
    #'django_toolbar',

    'djcelery',

    # 3rd party installs
    'rest_framework',   # for api stuff
    'braces',

    'django_extensions',      # shell_plus

    # --- removed for testing only ---
    #'cachalot',              # caching models
    'pipeline',               # minifying/compressing static assets


    #
    ####################################
    # rio-dfs specific apps below here #
    ####################################
    'account',
    'dfslog',
    'transaction',
    'cash',
    'cash.withdraw',
    'cash.tax',
    'ticket',
    'fpp',
    'promocode',
    'promocode.bonuscash',

    'keyprefix', # cache namespace
    'dataden',   # DataDen/MongoDB triggers

    'sports',
    'sports.mlb',
    'sports.nba',
    'sports.nhl',
    'sports.nfl',

    'prize',
    'scoring',
    'salary',
    'roster',
    'test',
)

MIDDLEWARE_CLASSES = (
    # CSRF token masking
    'debreach.middleware.CSRFCryptMiddleware',

    # GZIP and security protection for it
    'django.middleware.gzip.GZipMiddleware',
    'debreach.middleware.RandomCommentMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',

    # CSRF token masking
    'debreach.context_processors.csrf',
)


# Django Logging
# ----------------------------------------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
