from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(max_length=32, unique=True, null=True, blank=True, verbose_name='چت آی دی تلگرام')
