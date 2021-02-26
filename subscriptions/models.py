from django.db import models
from django.utils import timezone


class UserSubscription(models.Model):
    client_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255, blank=True, null=True)
    subscribed_until = models.DateTimeField(null=True, blank=True)

    @property
    def is_premium(self) -> bool:
        return bool(self.subscribed_until and self.subscribed_until > timezone.now())
