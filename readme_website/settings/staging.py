# This settings file is for the hosted dev staging website
# It inherits from host (which inherits from base)

from .host import *

# https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [".dev.cmureadme.com"]

CSRF_TRUSTED_ORIGINS = ["https://dev.cmureadme.com"]
