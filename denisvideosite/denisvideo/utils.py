import random
from datetime import datetime, timedelta

from django.db.models import Count, Q
from django.http import Http404

from denisvideo.models import View, Video


def create_view(request, video):
    if request.user.is_authenticated:
        View.objects.filter(user = request.user, video=video).delete()
        View.objects.create(user = request.user, video = video)


def increment_view_count(video):
    views = video.views_count + 1
    video.views_count = views
    video.save()


def get_side_videos(video):
    side_videos = list(Video.objects.filter(tags__in=video.tags.all()).select_related('user', 'user__channel'))
    return random.choices(side_videos, k=10) if side_videos else []


def get_recommended_videos(request, num_vid_per_page):
    videos = []

    count_vid_by_tag = get_count_vid_by_tag(request, num_vid_per_page)

    return get_videos_by_watch_tag(request, count_vid_by_tag, videos)


def get_count_vid_by_tag(request, num_vid_per_page):
    user_views = View.objects.filter(user=request.user, time_create__gt=datetime.now() - timedelta(days=30))
    total = user_views.aggregate(Count('pk'))['pk__count']
    views_by_tag = user_views.values('video__tags__pk').annotate(count=Count('pk'))

    return {tag['video__tags__pk']: int(tag['count'] / total * num_vid_per_page) for tag in views_by_tag}


def get_videos_by_watch_tag(request, count_vid_by_tag, videos):
    for tag_pk, count in count_vid_by_tag.items():
        video_list = list(Video.objects.filter(~Q(views__user=request.user),
                                               tags__pk=tag_pk,
                                               time_create__gt=datetime.now() - timedelta(days=60)).select_related('user', 'user__channel'))
        count = len(video_list) if count > len(video_list) else count
        videos.extend(random.sample(video_list, k=count))
    return videos


def add_videos_to_needs_num(videos, num_vid_per_page):
    video_list = Video.objects.all().select_related('user', 'user__channel')
    while len(videos) != num_vid_per_page and len(videos) < len(video_list):
        vid = random.choice(video_list)
        if vid not in videos and vid:
            videos.append(vid)
    return videos


def get_videos_by_type(request):
    if request.GET.get('type') in ('liked_videos', 'later_videos'):
        return getattr(request.user, request.GET.get('type')).all()[::-1]
    elif request.GET.get('type') == 'views':
        return Video.objects.filter(views__user = request.user).order_by('-views__time_create')
    else:
        raise Http404()


def mark_video(request, video):
    type = request.GET.get('type')
    if type in ('likers', 'dislikers'):
        if request.user in getattr(video, type).all():
            getattr(video, type).remove(request.user)
        else:
            getattr(video, type).add(request.user)