from enum import Enum

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from .managers import CustomUserManager

class CustomUser(AbstractUser):

    class Gender(Enum):
        male = ('M', 'Male')
        female = ('F', 'Female')
        other = ('Ot', 'Other')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    username = None
    id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name=_('Email Address'), unique=True)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=10, choices=[x.value for x in Gender])
    date_Of_birth = models.DateField()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:

        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('users:profile')
