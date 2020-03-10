# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *  # noqa

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = "wPY7XuC0d415HKKiUUXUIGdeGwGv4yNwjaIAFDBFDsWBofHvfTytoC26DfInPN7p",

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_HOST = config.get('EMAIL_HOST')
EMAIL_HOST_USER = config.get('EMAIL_USERNAME')
EMAIL_HOST_PASSWORD = config.get('EMAIL_PASSWORD')
EMAIL_PORT = config.get('EMAIL_PORT')
DEFAULT_FROM_EMAIL = "Remote Printer <ad.remoteprinter@gmail.com>"
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# Your stuff...
# ------------------------------------------------------------------------------
