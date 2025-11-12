# This settings file is inherited for all contexts running on the production server (staging and prod)
# It inherits from base

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Copy all static files to /static with collectstatic
STATIC_ROOT = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static/"
]