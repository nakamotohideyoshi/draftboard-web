"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

#
# the admin account password for dev is: admin
#

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import braintree
BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT   = os.path.dirname(os.path.realpath(__file__))

from os.path import join
TEMPLATE_DIRS = (
    join(BASE_DIR, 'account/templates'),
    join(BASE_DIR,  'mysite/templates'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9^1kzl5mo3pfgy1f402)27s*jz=s00^#rtznm_2)i!tkz7s-ed'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',   # for api stuff
    'braces',
    #
    ####################################
    # rio-dfs specific apps below here #
    ####################################
    'account',
    'dfslog',
    'transaction',
    'cash',
    'test',
)
#
##########################################################################
#        django_braintree
##########################################################################
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
#        cash -Withdrawal Rules
##########################################################################
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT          = 100.00
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_DAILY_FREQ      = 2
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_WEEKLY_FREQ     = 3
DFS_CASH_WITHDRAWAL_APPROVAL_REQ_MONTHLY_FREQ    = 6
DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO      = 750.00


#
##########################################################################
#        rest_framework
##########################################################################
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql_psycopg2',
        'NAME'      : 'dfs',               # name of the database
        #'USER'      : 'postgres',           # superuser
        #'PASSWORD'  : '',
        #'HOST'      : 'localhost'           # for dev, the postgres db is on same server
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

#
# for djangorestframework (api creator/helper)
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.

    #
    # COMMENTED OUT FOR REST_FRAMEWORK TUTORIAL
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ]

    #
    # for pagination
    #'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination'
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE' : 50,
}