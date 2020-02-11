import datetime
import os
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

    class UserType(Enum):

        staff = (1, 'Staff')
        client = (2, 'Client')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    DEFAULT_PROFILE_IMAGE = 'nopic.jpg'

    def profile_pic_path(self, filename):
        if filename != self.DEFAULT_PROFILE_IMAGE:
            basefilename, file_extension = os.path.splitext(filename)
            randomstr = datetime.datetime.now().strftime('%d-%m-%Y_%I:%M:%S,%f')
            return 'profile_pics/{userid}/{basename}_{randomstring}{ext}'.format(
                userid=self.id, basename=basefilename, randomstring=randomstr, ext=file_extension)
        return self.DEFAULT_PROFILE_IMAGE

    username = None
    id = models.BigAutoField(primary_key=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=10, choices=[x.value for x in Gender])
    date_Of_birth = models.DateField()
    profile_pic = models.ImageField(default=DEFAULT_PROFILE_IMAGE, upload_to=profile_pic_path)
    user_type = models.IntegerField(choices=[x.value for x in UserType])

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
