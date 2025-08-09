from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from pytils.translit import slugify


# Create your models here.
class Video(models.Model):
    file = models.FileField(upload_to='videos',
                            validators =[FileExtensionValidator(allowed_extensions=['mp4','avi','mkv','mov','wmv','webm','html5','mpeg'])],
                            verbose_name='Видео файл')
    name = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(unique=True)
    preview = models.ImageField(upload_to='previews', verbose_name='Превью')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='videos', verbose_name='Автор')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True)
    likers = models.ManyToManyField(get_user_model(), blank=True, related_name='liked_videos')
    dislikers = models.ManyToManyField(get_user_model(),blank=True, related_name='disliked_videos')
    watch_later_users = models.ManyToManyField(get_user_model(),blank=True, related_name='later_videos')
    tags = models.ManyToManyField('Tag', blank = True, related_name='videos', verbose_name='Теги')
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class View(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='views',
                             verbose_name='Пользователь')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='views', verbose_name='Видео')
    time_create = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название тега')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)