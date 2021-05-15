from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import AccountManager


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Account(AbstractBaseUser):
    email                     = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username                  = models.CharField(max_length=10, unique=True)
    description               = models.TextField(max_length=60)
    #required fields
    date_joined               = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin                  = models.BooleanField(default=False)
    is_active                 = models.BooleanField(default=True)
    is_staff                  = models.BooleanField(default=False)
    is_superuser              = models.BooleanField(default=False)


    USERNAME_FIELD = 'email' #login field
    REQUIRED_FIELDS = [
        'username',
    ]


    objects = AccountManager()


    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        return self.is_admin


    def has_module_perms(self, app_label):
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)