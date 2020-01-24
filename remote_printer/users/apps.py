from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UsersConfig(AppConfig):
    name = f"{settings.APP_NAME}.users"
    verbose_name = _("Users")
