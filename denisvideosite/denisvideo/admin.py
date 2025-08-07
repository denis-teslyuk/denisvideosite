from django.contrib import admin

from denisvideo.models import Video, Tag, View


# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = ('slug', )


admin.site.register(View)
