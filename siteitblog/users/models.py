from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name="Аватарка")
    status = models.CharField(max_length=50, blank=True, null=True, verbose_name="Статус профиля")
    key_skills = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ключевые навыки") # заменить на ListField при подключение PostgreSql

