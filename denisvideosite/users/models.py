from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users_photo', blank=True, null=True, verbose_name='Фото профиля')

