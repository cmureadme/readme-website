# This settings file is for the production website
# It inherits from host (which inherits from base)

from .host import *

# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    '.cmureadme.com'
]

CSRF_TRUSTED_ORIGINS = [
    "https://cmureadme.com"
]