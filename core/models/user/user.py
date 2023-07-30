from django.db import models
from django.contrib.auth.models import User


class OrdinaryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar/', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    signature = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "ordinaryuser"
