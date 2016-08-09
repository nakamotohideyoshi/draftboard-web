from django.conf.locale.en import formats as en_formats
from django.core.exceptions import ImproperlyConfigured
from os import environ
from os.path import join
from sys import stdout
from unipath import Path
import datetime
import os

en_formats.DATETIME_FORMAT = "l, M d P"             # [ "m/d/Y h:i:s P", "l m.d.Y  @  P" ]

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

SITE = 'www.draftboard.com'

PROJECT_ROOT = Path(__file__).ancestor(3)
STATIC_ROOT = PROJECT_ROOT.child('collected_static')
INTERNAL_IPS = ()

#
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

# fixtures directory: /PATH/TO/BASE_PROJECT_DIR/test/fixtures
FIXTURES_DIR = (os.path.join(BASE_DIR, 'test/fixtures'),)  # for $> manage.py test

#
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/contests/'

# Testing mode by default
DEBUG = False

# django (>= 1.9) template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(BASE_DIR, 'templates'),
            join(BASE_DIR, 'account/templates'),
            join(BASE_DIR, 'prize/templates'),
            join(BASE_DIR, 'salary/templates'),
            join(BASE_DIR, 'sports/templates'),
            join(BASE_DIR, 'contest/schedule'),
        ],
        # 'APP_DIRS': True, # defaults to False
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.request',
                'cash.withdraw.context_processors.model_badges',
                'mysite.context_processors.pusher_key',
                'mysite.context_processors.pusher_channel_prefix',
                'mysite.context_processors.delta_now_prefix',
                'mysite.context_processors.player_images_url',
                'mysite.context_processors.git_commit_uuid',
                'mysite.context_processors.js_loglevel',

                # testing this here... had to move it in here in django 1.9
                'debreach.context_processors.csrf',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],

            'debug': DEBUG,  # set the template debug to the same as global settings debug
        }
    },
]

# Folder locations
STATICFILES_DIRS = (
    PROJECT_ROOT.child('static').child('build'),
)

# session uses redis and postgres to create cached db
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Static assets, served via django-whitenoise
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/build/'
PLAYER_IMAGES_URL = '//static-players.draftboard.com'

# Redirects to same URL with end slash if it can't find the page
APPEND_SLASH = True

# Only allow site to be hosted on our domain
ALLOWED_HOSTS = ['.draftboard.com', '*.draftboard.com']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9^1kzl5mo3pfgy1f402)27s*jz=s00^#rtznm_2)i!tkz7s-ed'

# Where to start looking for URL definitions
ROOT_URLCONF = 'mysite.urls'

# CORS requests for OAuth
CORS_ORIGIN_ALLOW_ALL = True

# locale
LANGUAGE_CODE = 'en-us'

# using 'America/New_York' will make the admin
# display times in EST, however, in code
# the models (because of the server!) will
# have datetimes stored in UTC. This is quite useful!
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# for the editing/display format of time objects in the admin
TIME_INPUT_FORMATS = [
    '%H:%M',        # '14:30'
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
]

# cachalot cache
CACHALOT_CACHE = 'cachalot'

# Use Pipeline for static asset management
STATICFILES_STORAGE = 'mysite.storage.WhitenoisePipelineStorage'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE_JS = {}

#
##########################################################################
#        cash -Withdrawal Rules
##########################################################################
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT = 100.00
DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO = 600.00

#
##########################################################################
#        pusher - LIVE
##########################################################################
PUSHER_APP_ID = '144195'
PUSHER_KEY = '9754d03a7816e43abb64'
PUSHER_SECRET = 'fcbe16f4bf9e8c0b2b51'

#
# our own prefix to globally apply to pusher channels.
# this should be an empty string for production,
# but locally you may wish to override it for testing.
PUSHER_CHANNEL_PREFIX = ''  # *** MUST REMAIN EMPTY IN PRODUCTION ***

#
# default: True.  whether Pusher will actually send objects its told to send()
PUSHER_ENABLED = True

#
##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_CLIENT_ID = None
PAYPAL_SECRET = None

#
##########################################################################
# paypal vzero minimal deposit server access_token
##########################################################################
VZERO_ACCESS_TOKEN = None

# REST currently defaulting to session authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # use for testing by browser
    ),

    # 'DEFAULT_PAGINATION_CLASS': None
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

# JWT Settings
JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30)
}

# Django installs
INSTALLED_APPS = (
    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # testing this out
    # 'django_toolbar',

    'djcelery',
    # 3rd party installs
    'rest_framework',   # for api stuff
    'braces',

    'django_extensions',      # shell_plus

    # --- removed for testing only ---
    # 'cachalot',              # caching models
    'pipeline',               # minifying/compressing static assets

    #
    #######################################
    # draftboard specific apps below here #
    #######################################
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
    'keyprefix',
    'dataden',              # DataDen/MongoDB triggers
    'sports',
    'sports.mlb',
    'sports.nba',
    'sports.nhl',
    'sports.nfl',
    'lineup',
    'prize',
    'push',
    'contest',
    'contest.payout',
    'contest.buyin',
    'contest.refund',
    'contest.schedule',
    'scoring',
    'scoring.baseball',     # generate stat-strings
    'roster',
    'rakepaid',
    'test',
    'salary',
    'draftgroup',
    'frontend',             # front end styles, layout, etc
    'mysite',               # just for management command access
    'replayer',
    'pp',                   # our implementation of a few required paypal apis
    'lobby',
    'rest_framework_swagger',
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'devs@draftboard.com'
EMAIL_HOST_PASSWORD = 'bfNdCw7LpBD4UUrYG91YVw'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'support@draftboard.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

MIDDLEWARE_CLASSES = (
    # CSRF token masking
    'debreach.middleware.CSRFCryptMiddleware',

    # GZIP and security protection for it
    'django.middleware.gzip.GZipMiddleware',
    'debreach.middleware.RandomCommentMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Django Logging
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
        'mysite': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# GLOBAL CONSTANTS
USERNAME_DRAFTBOARD = "draftboard"
USERNAME_ESCROW = "escrow"
BONUS_CASH_RAKE_PERCENTAGE = .4

# used to cache version localStorage on frontend
GIT_COMMIT_UUID = os.environ.get('GIT_COMMIT_UUID', 'LOCAL')

#
# DataDen license key for account: devs@draftboard.com
DATADEN_LICENSE_KEY = '20491e2a4feda595b7347708915b200b'
DATADEN_ASYNC_UPDATES = True  # uses celery for signaling stat updates from triggers

#
# DATETIME_DELTA_SECONDS_KEY is the key in the cache for the delta seconds timeshift on timezone.now()
DATETIME_DELTA_ENABLE = False    # dont change in base.py,   change to True in local.py, etc...
DATETIME_DELTA_SECONDS_KEY = 'DATETIME_DELTA_SECONDS_KEY'


# Set django-lockdown to run on heroku for now
USE_LOCKDOWN = os.environ.get('USE_LOCKDOWN', 'False') == 'True'
if USE_LOCKDOWN:
    INSTALLED_APPS += ('lockdown',)
    MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware',)
    LOCKDOWN_PASSWORDS = (os.environ.get('LOCKDOWN_PASSWORD', 'False'),)
    LOCKDOWN_URL_EXCEPTIONS = (
        r'^/api/',
        r'^/api-token-auth/',
        r'^/api-token-refresh/',
        r'^/static/',
    )

#
# custom test runner by default does not require sudo privileges
INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO = False

#
# disable recording
DISABLE_REPLAYER_UPDATE_RECORDING = False

#
# for testing purposes, defaults to None, unless otherwise specified in child settings file
TEST_SETUP = None

# defaults to false, though we made turn this on in production.py
SLACK_UPDATES = False

# heroku redis url - used for caching pages/views
HEROKU_REDIS_URL = None

# defaults to use the default cache, but
# if server has Heroku Redis add-on should be set to
# the named cache that uses the heroku redis instance
API_CACHE_NAME = 'default'

