# This settings file is for local dev use only
# It inherits from base

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

STATICFILES_DIRS = [BASE_DIR / "static/"]
