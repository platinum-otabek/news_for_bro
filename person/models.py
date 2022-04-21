import datetime

# Create your models here.
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)

from person.managers import MyUserManager


class CustomeUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150, default='')
    last_name = models.CharField(max_length=150, default='')
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=datetime.datetime.now())
    is_active = models.BooleanField(default=True)

    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'
        verbose_name = 'user'

    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class ResetPasswordModel(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=127, default='')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reset_password'


