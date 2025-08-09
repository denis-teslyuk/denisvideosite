from django.contrib.auth.models import AbstractUser
from django.db import models
from pytils.translit import slugify


# Create your models here.
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='users_photo', blank=True, null=True, verbose_name='Фото профиля')


class Channel(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    description = models.TextField(blank = True, verbose_name='Описание')
    slug = models.SlugField(unique=True)
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE,
                                related_name='channel', verbose_name='Пользователь')

    def __str__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        super().save()

