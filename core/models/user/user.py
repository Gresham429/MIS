from django.db import models
from django.contrib.auth.models import User


class OrdinaryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    photo = models.URLField(blank=True, null=True, max_length=256)

    class Meta:
        verbose_name_plural = "OrdinaryUser"
