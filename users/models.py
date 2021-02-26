from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator
from django.db import models
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from subscriptions.models import UserSubscription

from . import managers


class User(auth_models.AbstractUser):
    username = None

    first_name = models.CharField(max_length=30, verbose_name=_('First name'), validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=150, verbose_name=_('Last name'), validators=[MinLengthValidator(2)])
    email = models.EmailField(unique=True, verbose_name=_('Email address'))

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(verbose_name=_('Date joined'), auto_now_add=True)

    subscription = models.OneToOneField('subscriptions.UserSubscription', on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name',)

    objects = managers.CustomUserManager()

    def __str__(self) -> str:
        return self.full_username

    def save(self, *args, **kwargs):
        if not self.email:
            with transaction.atomic():
                super().save(*args, **kwargs)
                subscription = UserSubscription(user=self)
                self.subscription = subscription
                subscription.save()
        return super().save(*args, **kwargs)


    @property
    def full_username(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"
