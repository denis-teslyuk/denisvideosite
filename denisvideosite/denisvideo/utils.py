import random

from denisvideo.models import View, Video


def create_view(request, video):
    if request.user.is_authenticated:
        View.objects.filter(user = request.user, video=video).delete()
        View.objects.create(user=request.user, video = video)


def increment_view_count(video):
    views = video.views_count + 1
    video.views_count = views
    video.save()


def get_side_videos(video):
    side_videos = list(Video.objects.filter(tags__in=video.tags.all()))
    return random.choices(side_videos, k=10) if side_videos else []
