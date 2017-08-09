# Pipeline apps should be based off of staging settings.
from .staging import *

ALLOWED_HOSTS = ['*']

ENVIRONMENT_NAME = "PIPELINE APP"
ENVIRONMENT_COLOR = "#9ea548"


DEFAULT_FROM_EMAIL = 'support+PIPELINE@draftboard.com'
