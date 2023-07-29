from django.db import models
from django.contrib.auth.models import User


class OrdinaryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatar/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "ordinaryuser"
