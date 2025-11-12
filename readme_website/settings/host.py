# This settings file is inherited for all contexts running on the production server (staging and prod)
# It inherits from base

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.dev.cmureadme.com'
]