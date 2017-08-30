# Pipeline apps should be based off of staging settings.
from .staging import *

ALLOWED_HOSTS = ['*']

ENVIRONMENT_NAME = "PIPELINE APP"
ENVIRONMENT_COLOR = "#9ea548"


DEFAULT_FROM_EMAIL = 'support+PIPELINE@draftboard.com'

PUSHER_CHANNEL_PREFIX = 'pipeline_app__'

# On our staging + prod apps celery has it's own redis DB but it's not possible to create
# DBs programmatically so just use the same DB for both of these.
REDIS_URL = environ.get('REDISCLOUD_URL')
REDIS_URL_CELERY = environ.get('REDISCLOUD_URL')
