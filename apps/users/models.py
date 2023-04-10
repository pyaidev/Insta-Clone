from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from ..common.models import TimeStampedModel


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    first_name = models.CharField(
        max_length=50, verbose_name='Name',
    )
    last_name = models.CharField(
        max_length=50, verbose_name='Surname',
    )
    username = models.CharField(
        max_length=255, blank=True, null=True, unique=True, verbose_name='Username',
    )
    phone_number = PhoneNumberField(
        region='UZ', unique=True, verbose_name='Phone number', blank=True, null=True,
    )
    email = models.EmailField(
        max_length=255, unique=True, verbose_name='Email',
    )
    is_superuser = models.BooleanField(default=False, verbose_name='Superuser')
    is_staff = models.BooleanField(default=False, verbose_name='Admin')
    is_active = models.BooleanField(default=True)
    date_login = models.DateTimeField(auto_now=True, verbose_name='Date login')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
