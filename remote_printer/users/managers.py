from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class CustomUserManager(BaseUserManager):

    """
    Overriding BaseUserManager in order to allow users to register and authenticate
    by using email instead of username.
    """

    def _create_user(self, email, password, is_staff, is_superuser, **kwargs):
        if not email:
            raise ValueError(_('Users must have an email address'))
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        kwargs.update({'mobile':0, 'gender':'', 'date_Of_birth':'1951-01-01', 'user_type':'1'})
        return self._create_user(email, password, False, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.update({'mobile':0, 'gender':'', 'date_Of_birth':'1951-01-01', 'user_type':'1'})
        user = self._create_user(email, password, True, True, **kwargs)
        return user
