from django.contrib import admin

from denisvideo.models import Video, Tag

# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', )