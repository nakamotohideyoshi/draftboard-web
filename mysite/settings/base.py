from datetime import timedelta
from os import environ, path
from sys import stdout

from django.conf.locale.en import formats as en_formats
from unipath import Path

# Django constants
# ----------------------------------------------------------

SITE = 'www.draftboard.com'
ALLOWED_HOSTS = ['.draftboard.com', '*.draftboard.com']
INTERNAL_IPS = ()

ENVIRONMENT_NAME = "Probably Local"
ENVIRONMENT_COLOR = "#a505a4"

# Folder locations
PROJECT_ROOT = Path(__file__).ancestor(3)
STATIC_ROOT = PROJECT_ROOT.child('collected_static')
BASE_DIR = path.dirname(path.dirname(__file__))
SITE_ROOT = path.dirname(path.realpath(__file__))
FIXTURES_DIR = (path.join(BASE_DIR, 'test/fixtures'),)  # for $> manage.py test
STATICFILES_DIRS = (
    PROJECT_ROOT.child('static').child('build'),
    PROJECT_ROOT.child('mysite').child('static'),
)

# Auth and admin
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/contests/'

# Testing mode by default
DEBUG = True

# session uses redis and postgres to create cached db
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Static assets, served via django-whitenoise
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/build/'
PLAYER_IMAGES_URL = '//static-players.draftboard.com'

# Redirects to same URL with end slash if it can't find the page
APPEND_SLASH = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9^1kzl5mo3pfgy1f402)27s*jz=s00^#rtznm_2)i!tkz7s-ed'

# Where to start looking for URL definitions
ROOT_URLCONF = 'mysite.urls'

# CORS requests for OAuth
CORS_ORIGIN_ALLOW_ALL = True

# locale
LANGUAGE_CODE = 'en-us'

# locale
ENCODE_SECRET_KEY = 'jro-1&fb#hv_yye22'

# using 'America/New_York' will make the admin
# display times in EST, however, in code
# the models (because of the server!) will
# have datetimes stored in UTC. This is quite useful!
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
en_formats.DATETIME_FORMAT = "D, M d P o"  # [ "m/d/Y h:i:s P", "l m.d.Y  @  P" ]

# for the editing/display format of time objects in the admin
TIME_INPUT_FORMATS = [
    '%H:%M',  # '14:30'
    '%H:%M:%S',  # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
]

# Django installs

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # CSRF token masking
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

# django (>= 1.9) template settings
INSTALLED_APPS = (
    # django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_celery_beat',
    'rest_framework',  # for api stuff
    'braces',
    'django_extensions',  # shell_plus
    # TODO: Enable Cachalot... maybe.
    # --- removed for testing only ---
    # 'cachalot',  # caching models
    'pipeline',  # minifying/compressing static assets
    # draftboard specific apps below here #
    'account',
    'account.gidx',
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
    'dataden',  # DataDen/MongoDB triggers
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
    'scoring.baseball',  # generate stat-strings
    'roster',
    'rakepaid',
    'test',
    'salary',
    'draftgroup',
    'frontend',  # front end styles, layout, etc
    'mysite',  # just for management command access
    'replayer',
    'pp',  # our implementation of a few required paypal apis
    'lobby',
    'raven.contrib.django.raven_compat',  # sentry
    'statscom',  # STATS.com api parsers, models, projections, etc...
    'swish',  # Swish Analytics
    'rest_framework_swagger',
)
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        path.join(BASE_DIR, 'templates'),
        path.join(BASE_DIR, 'account/templates'),
        path.join(BASE_DIR, 'prize/templates'),
        path.join(BASE_DIR, 'salary/templates'),
        path.join(BASE_DIR, 'sports/templates'),
        path.join(BASE_DIR, 'contest/schedule'),
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
            'mysite.context_processors.from_settings',

        ],
        'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]),
        ],

        'debug': DEBUG,  # set the template debug to the same as global settings debug
    },
}]

# Custom global constants
# ----------------------------------------------------------

# Time shifting is the key in the cache for the delta seconds timeshift on timezone.now()
# Normally we have local settings here, but don't want to chance this, so dont change in base.py,
# change to True in local.py, etc...
DATETIME_DELTA_ENABLE = False
DATETIME_DELTA_SECONDS_KEY = 'DATETIME_DELTA_SECONDS_KEY'

# Cash - Withdrawal Rules
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT = 100.00
DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO = 600.00

# Used to cache bust localStorage on frontend
GIT_COMMIT_UUID = environ.get('GIT_COMMIT_UUID', 'LOCAL')

# Master user
USERNAME_DRAFTBOARD = "draftboard"
USERNAME_ESCROW = "escrow"
BONUS_CASH_RAKE_PERCENTAGE = .4

# custom test runner by default does not require sudo privileges
INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO = False

# disable recording by default
# turn this on in your own dev settings when generating replayer
DISABLE_REPLAYER_UPDATE_RECORDING = False

# for testing purposes, defaults to None, unless otherwise specified in child settings file
TEST_SETUP = None

# Allow Slack notifications for various events.
# Defaults to false, though we made turn this on with environment variables.
SLACK_UPDATES = False
slack_updates = environ.get('SLACK_UPDATES', None)
if slack_updates is not None and 't' in str(slack_updates).lower():
    SLACK_UPDATES = True

REDIS_URL = 'redis://redis-server:6379'  # for live stats, defaults to local vagrant

# defaults to use the default cache, but
# if server has Heroku Redis add-on should be set to
# the named cache that uses the heroku redis instance
API_CACHE_NAME = 'default'

# Third party credentials - defaults to test mode
# ----------------------------------------------------------

# DataDen - license key for account: devs@draftboard.com
DATADEN_LICENSE_KEY = '20491e2a4feda595b7347708915b200b'
DATADEN_ASYNC_UPDATES = True  # uses celery for signaling stat updates from triggers

# Sparkpost Mail
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.sparkpostmail.com'
EMAIL_HOST_USER = 'SMTP_Injection'
EMAIL_HOST_PASSWORD = 'ce8b35bc66edb33f9094733687c05343b12521a9'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'support@draftboard.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Live Mongo Connection settings (we use live for everything, no local instance)
MONGO_SERVER_ADDRESS = 'ds015781-a0.mlab.com'
MONGO_AUTH_DB = 'admin'
MONGO_USER = 'django_readonly'
MONGO_PASSWORD = '7GZAG3wrtppzgWCfGdLBTcvDFazpNxsmL4rH9NE8'
MONGO_PORT = 15781  # default port may be the actual port
MONGO_HOST = 'mongodb://%s:%s@%s:%s/%s' % (
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_SERVER_ADDRESS,
    MONGO_PORT,
    MONGO_AUTH_DB)

# Pusher - pbp-stats-linking-dev
PUSHER_APP_ID = '179543'
PUSHER_KEY = '3e6ac7a6d8d8ec16e6d3'
PUSHER_SECRET = '498b39ae3744d83be7d9'
PUSHER_CHANNEL_PREFIX = ''  # prepends any Pusher channel, useful for silo-ing calls per dev
# if Pusher will actually send objects its told to send()
PUSHER_ENABLED = 't' in environ.get('PUSHER_ENABLED', 'true')
# If enabled, pusher events will also be written to a local text file.
# This can be used with the export_game_pbp management command to dump out all pusher events
# from a specific game.
PUSHER_OUTPUT_TO_FILE = False

# Paypal - test
PAYPAL_REST_API_BASE = 'https://api.sandbox.paypal.com'
PAYPAL_CLIENT_ID = 'ARqP3lkXhhR_jmm6NkyoKQfuOcBsn1KBYtlzZGHEvGDCQ-ajNoxpQD2mDScpT6tkgsI7qFgVJ-KgzpFE'
PAYPAL_SECRET = 'EOKSd-HCNfWE17mu8e7uyjs2egSla2yXs7joweXCLdimCY8yv-FcCx7LeP1do0gMb9vExJSmjyw9hwRu'

# Sandbox Account:  paypal-facilitator@draftboard.com
# Access Token:     access_token$sandbox$c6yfbzrdmyjqbf6k$4218ebe110f341437affed2f726cd6fa
# Expiry Date:      01 Aug 2026
VZERO_ACCESS_TOKEN = 'access_token$sandbox$c6yfbzrdmyjqbf6k$4218ebe110f341437affed2f726cd6fa'

# stats.com credentials for api usage
STATSCOM_URL_BASE = 'http://api.stats.com/v1'
STATSCOM_KEYS = {
    'api_key': 'htkfzjjc6ja73gpz5sgqv2yr',
    'secret': 'bS74caTFtx',
}

# RotoWire API Key
ROTOWIRE_API_KEY = 'mg9meedahh812af5sfgl'

# Swish analytics
SWISH_API_KEY = 'e7ec4ca5fca54a01ac0038205b8235e9'

# Third party settings
# ----------------------------------------------------------

# Cachalot cache
CACHALOT_CACHE = 'cachalot'

# JWT Settings
JWT_AUTH = {
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=30),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=30)
}

# REST currently defaulting to session authentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),

    # 'DEFAULT_PAGINATION_CLASS': None
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

# Use Pipeline for static asset management
STATICFILES_STORAGE = 'mysite.storage.WhitenoisePipelineStorage'

PIPELINE = {
    'PIPELINE_JS_COMPRESSOR': 'pipeline.compressors.jsmin.JSMinCompressor',
    'PIPELINE_JS': {}
}

# Django-lockdown until launch
USE_LOCKDOWN = environ.get('USE_LOCKDOWN', 'False') == 'True'
if USE_LOCKDOWN:
    INSTALLED_APPS += ('lockdown',)
    MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware',)
    LOCKDOWN_PASSWORDS = (environ.get('LOCKDOWN_PASSWORD', 'False'),)
    LOCKDOWN_URL_EXCEPTIONS = (
        r'^/api/',
        r'^/api-token-auth/',
        r'^/api-token-refresh/',
        r'^/static/',
    )

# Django Logging
# ----------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(pathname)s:%(lineno)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(pathname)s:%(lineno)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': stdout,
            'formatter': 'simple'
        },
    },
    'loggers': {
        # A catch-all logger.
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# GETIPNET settings
# ----------------------------------------------------------
GETIPNET_DEFAULT_SUBDOMAIN = "check"
GETIPNET_SUBDOMAIN = "runfdv4kure0vjqfmdl8hba"
GETIPNET_CONTACT = "devs@draftboard.com"
GETIPNET_NORMAL = 0.99

# GEOIP settings
# ----------------------------------------------------------
GEOIP_PATH = path.join(BASE_DIR, '../geoip')

# Inactive users
INACTIVE_USERS_EMAILS = []
# Who will recieve flagged identity emails. (this can be empty)
FLAGGED_IDENTITY_EMAIL_RECIPIENTS = ['dan@draftboard.com', 'devs@draftboard.com']
SITE_ADMIN_EMAIL = ['dan@draftboard.com', 'zach@draftboard.com', 'ryan@draftboard.com']

# Sentry Config
RAVEN_CONFIG = {
    'dsn': environ.get('SENTRY_DSN')
}
# This is the Sentry client key "DSN (Public)" to be used on the web client.
# It is different than the RAVEN_CONFIG one above. Any staging/production environments should
# have this set via environment variable, if none it set, default to this one which
# is for the "Draftboard - Local" Sentry app.
SENTRY_PUBLIC_DSN = environ.get('SENTRY_PUBLIC_DSN', 'https://bbae8e8654e34a80b02999b5ade6fd81@sentry.io/72241')


# access domain
COOKIE_ACCESS_DOMAIN = '.draftboard.com'

# ANALYTICS settings
# ----------------------------------------------------------
# Don't track any pageviews on non-production sites
KISS_ANALYTICS_CODE = ''
GOOGLE_ANALYTICS_CODE = ''


# Trusted sources for swish update
TRUSTED_SOURCES = ['usatoday', 'rotoworld', 'rotowire']


# once limits applied, residents of specific states will not be able to increase
# this limit for days respectively.
LIMIT_DAYS_RESTRAINT = {'MA': 90}

# Sandbox gidx credentials
# NOTE: The API_URL is different for prod + testing
GIDX_API_URL = 'https://api.gidx-service.in'
GIDX_API_KEY = 'k2m9yX4Tl0WXuz8Ahc5muA'
GIDX_MERCHANT_ID = 'Q2wprL4aKEKEj-dzTu44BA'
# Gets appended to customer ID's to show they are testing IDs.
GIDX_CUSTOMER_ID_PREFIX = 'TEST--'
# This is is a prefix to enable testing mode on the client-side of things.
# GIDX_MERCHANT_SESSION_ID_PREFIX = 'GIDXSB_'
# An empty prefix disables testing mode.
GIDX_MERCHANT_SESSION_ID_PREFIX = ''
GIDX_PRODUCT_ID = 'iiXXab0LtUCUdZ_6vcdtvQ'
GIDX_ACTIVITY_ID = 'FyP1fg_WkU60JnuIarfOQw'
GIDX_DEVICE_ID = '2bDPorOkPkepDd8-6Fydtw'
# Should we allow previously claimed ID's to be verified?
# This should ONLY be True for testing.
GIDX_ALLOW_PREVIOUSLY_CLAIMED_ID = False
