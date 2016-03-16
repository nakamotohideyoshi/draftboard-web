from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  'generate_replayer',
        #'USER': 'vagrant',      # by not specifying a user at all, it will not prompt for password
        #'HOST': 'localhost',    # default to localhost
        #'CONN_MAX_AGE': 60,
    }
}
