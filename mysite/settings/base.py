from os import environ
from sys import stdout
from unipath import Path
import datetime

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return environ[var_name]
    except KeyError:
        error_msg = "Set the %s env variable" % var_name
        raise ImproperlyConfigured(error_msg)

#
#
SITE = 'www.draftboard.com'

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

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/lobby/'

#
# Django 1.8 removed TEMPLATE_DIRS. It is now TEMPLATES = {}
# https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/
# TEMPLATE_DIRS = ( PROJECT_ROOT.child('templates'), )
TEMPLATES = [
    {
        'BACKEND' : 'django.template.backends.django.DjangoTemplates',
        'DIRS'    : [
            join(BASE_DIR, 'templates'),
            join(BASE_DIR, 'account/templates'),
            join(BASE_DIR, 'prize/templates'),
            join(BASE_DIR, 'salary/templates'),
            join(BASE_DIR, 'sports/templates')
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
                'mysite.context_processors.pusher_key',
                'mysite.context_processors.pusher_channel_prefix',
                'mysite.context_processors.delta_now_prefix',
            )
        }
    },
]

# Folder locations
STATICFILES_DIRS = (
    PROJECT_ROOT.child('static'),
    PROJECT_ROOT.child('static').child('build')
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
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/build/'

# Redirects to same URL with end slash if it can't find the page
APPEND_SLASH = True

# Only allow site to be hosted on our domain
ALLOWED_HOSTS = ['.draftboard-staging.herokuapp.com', '*.draftboard-staging.herokuapp.com', ]

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
#
# using 'America/New_York' will make the admin
# display times in EST, however, in code
# the models (because of the server!) will
# have datetimes stored in UTC. This is quite useful!
TIME_ZONE = 'America/New_York'
# TIME_ZONE = 'UTC'
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
#        pusher - LIVE
##########################################################################
PUSHER_APP_ID   = '144195'
PUSHER_KEY      = '9754d03a7816e43abb64'
PUSHER_SECRET   = 'fcbe16f4bf9e8c0b2b51'
#
# our own prefix to globally apply to pusher channels.
# this should be an empty string for production,
# but locally you may wish to override it for testing.
PUSHER_CHANNEL_PREFIX = ''     #   *** MUST REMAIN EMPTY IN PRODUCTION ***

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

#
##########################################################################
#       OPTIMAL payments
##########################################################################
OPTIMAL_ENVIRONMENT             = 'TEST' # 'LIVE'
OPTIMAL_API_KEY                 = '18643-1000031963'   # api key is actually API_KEY +':'+API_PASSWORD
OPTIMAL_API_PASSWORD            = 'B-qa2-0-55660e4b-0-302d021500882760fb4ae1dbf19ff320ee1c35ed7f61f0dcc302141a7c49c9b7333e87f429cba3a6ad4d6b7c7b2a7c'
OPTIMAL_ACCOUNT_NUMBER          = '1000031963'

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

    #'DEFAULT_PAGINATION_CLASS': None
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
# ----------------------------------------------------------
INSTALLED_APPS = (
    'suit',
    #
    # # django defaults
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
    'keyprefix', # cache namespace
    'dataden',   # DataDen/MongoDB triggers
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
    'roster',
    'rakepaid',
    'test',
    'salary',
    'draftgroup',
    'frontend', # front end styles, layout, etc
    'mysite', # just for management command access
    'replayer',

    'optimal_payments',

    'lobby',
    'rest_framework_swagger',
)

#
# Mandrill settings
# MANDRILL_API_KEY    = 'W5fUepyUtAf7U4l1-K4Y7g'
# EMAIL_BACKEND       = 'djrill.mail.backends.djrill.DjrillBackend'
# DEFAULT_FROM_EMAIL  = 'support@draftboard.com'

EMAIL_USE_TLS       = True
EMAIL_HOST          = 'smtp.mandrillapp.com'
EMAIL_HOST_USER     = 'devs@draftboard.com'
EMAIL_HOST_PASSWORD = 'bfNdCw7LpBD4UUrYG91YVw'
EMAIL_PORT          = 587
DEFAULT_FROM_EMAIL  = 'support@draftboard.com'
SERVER_EMAIL        = DEFAULT_FROM_EMAIL

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

SUIT_CONFIG = {
    'MENU': (

        # # To reorder existing apps use following definition
        {'app':'sites', 'label': 'Sites'},
        {'app':'auth', 'label': 'Accounts'},

        {'app':'account', 'label': 'Notifications'},
        {'app':'cash', 'label': 'Bank'},
        {'app':'contest', 'label': 'Contest'},
        {'app':'finance', 'label': 'Test'},
        {'app':'fpp', 'label': 'FPP'},
        {'app':'lobby', 'label': 'Lobby Banners'},

        {'app':'prize', 'label': 'Prize',
            'models':[
                {'label': 'Prize Structures', 'url':'/admin/prize/prizestructure/'},
                {'label': 'Cash Prize Structure Creator', 'url':'/api/prize/generator/'},
                {'label': 'Cash Prize Structure Creator (Flat)', 'url':'/api/prize/flat/'},
                {'label': 'Ticket Prize Structure Creator', 'url':'/api/prize/ticket/'},
            ]
         },
        # /api/prize/flat/
        # /api/prize/ticket/
        # /api/prize/generator/

        {'app':'salary', 'label': 'Salary'},

        {'app':'schedule', 'label': 'Contest Scheduler'},


        #{'app':'sports', 'label': 'Sports'},
        {'app':'nfl', 'label': 'NFL'},
        {'app':'nba', 'label': 'NBA'},
        {'app':'nhl', 'label': 'NHL'},
        {'app':'mlb', 'label': 'MLB'},
        {'app':'ticket', 'label': 'Ticket',
            'models':[
                 {'label': 'Prize', 'url':'/admin/ticket/ticketamount/'},
            ],
         },
        {'app':'rakepaid', 'label': 'Loyalty Program'},

        # #
        # # # If you want to link app models from different app use full name:
        # # ('sites', ('auth.user', 'auth.group')),
        #
        # # To add custom item, define it as tuple or list:
        # # For parent: (Name, Link, Icon, Permission) - Last two are optional
        # # For child: (Name, Link, Permission) - Last one is optional
        # # You can also mix custom and native apps and models
        # # Link can be absolute url or url name
        # # Permission can be string or tuple/list for multiple
        # # If MENU_OPEN_FIRST_CHILD=True and children exists, you can leave parent link blank
        #
        # # Example:
        # (('Prize Structure Creator', '/api/prize/generator/', 'icon-cog', ('auth.add_group',)),
        #     (
        #         ('Cash',     '/api/prize/generator/',    'auth.add_user'),
        #         ('Ticket',   '/api/prize/ticket/',       'auth.add_user'),
        #         ('Flat',     '/api/prize/flat/',         'auth.add_user'),
        #     )
        # )
    ) # end MENU_ORDER
} # end SUIT_CONFIG

# GLOBAL CONSTANTS
USERNAME_DRAFTBOARD = "draftboard"
USERNAME_ESCROW = "escrow"
BONUS_CASH_RAKE_PERCENTAGE = .4

#
# DataDen license key for account: devs@draftboard.com
DATADEN_LICENSE_KEY     = '20491e2a4feda595b7347708915b200b'
DATADEN_ASYNC_UPDATES   = True  # uses celery for signaling stat updates from triggers

#
# DATETIME_DELTA_SECONDS_KEY is the key in the cache for the delta seconds timeshift on timezone.now()
DATETIME_DELTA_ENABLE       = False    # dont change in base.py,   change to True in local.py, etc...
DATETIME_DELTA_SECONDS_KEY  = 'DATETIME_DELTA_SECONDS_KEY'


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
    )
