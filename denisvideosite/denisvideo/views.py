import random

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta
from denisvideo.models import View, Video


# Create your views here.
def index(request):
    videos = []
    num_vid_per_page = 10
    if request.user.is_authenticated:
        user_views = View.objects.filter(user=request.user, time_create__gt = datetime.now() - timedelta(days=30))
        views_by_tag =  user_views.values('video__tags__pk').annotate(count = Count('pk'))
        total = 0
        for tag in views_by_tag:
            total += tag['count']

        count__vid_by_tag = {tag['video__tags__pk']: int(tag['count'] / total * num_vid_per_page) for tag in views_by_tag}


        for tag_pk, count in count__vid_by_tag.items():
            video_list = list(Video.objects.filter(tags__pk = tag_pk,time_create__gt = datetime.now() - timedelta(days=60)))
            count = len(video_list) if count > len(video_list) else count
            videos.extend(random.sample(video_list, k=count))

    video_list = Video.objects.all()
    while len(videos) != num_vid_per_page and len(videos) < len(video_list):
        vid = random.choice(video_list)
        if vid not in videos:
            videos.append(vid)

    data = {
        'title': 'Домашняя страница',
        'videos': videos,
    }

    return render(request, 'denisvideo/index.html', data)


def show_video(request, slug):
    video = get_object_or_404(Video, slug = slug)

    side_videos = list(Video.objects.filter(tags__in = video.tags.all()))
    if side_videos:
        side_videos = random.choices(side_videos, k=10)

    data = {
        'title': video.name,
        'video': video,
        'side_videos': side_videos,
    }

    return render(request, 'denisvideo/show_video.html', data)