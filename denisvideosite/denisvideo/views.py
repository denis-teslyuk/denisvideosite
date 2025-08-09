import random

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta

from denisvideo.forms import VideoForm
from denisvideo.models import View, Video, Tag


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

    if request.user.is_authenticated:
        View.objects.filter(user = request.user, video=video).delete()
        View.objects.create(user=request.user, video = video)

    views = video.views_count + 1
    video.views_count = views
    video.save()

    side_videos = list(Video.objects.filter(tags__in = video.tags.all()))
    if side_videos:
        side_videos = random.choices(side_videos, k=10)

    likes_count = video.likers.count()
    dislikes_count = video.dislikers.count()

    data = {
        'title': video.name,
        'video': video,
        'side_videos': side_videos,
        'likes_count': likes_count,
        'dislikes_count':dislikes_count,
    }

    return render(request, 'denisvideo/show_video.html', data)


@login_required
def add_like_or_dislike(request, slug):
    video = get_object_or_404(Video, slug=slug)

    if request.GET.get('type') in ('likers', 'dislikers'):
        if request.user in getattr(video, request.GET['type']).all():
            getattr(video, request.GET['type']).remove(request.user)
        else:
            getattr(video, request.GET['type']).add(request.user)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def add_watch_later(request, slug):
    video = get_object_or_404(Video, slug=slug)
    video.watch_later_users.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


def search(request):
    search_string = request.GET.get('find', '')
    video_list = Video.objects.filter(
        Q(name__contains = search_string) | Q(description__contains = search_string))
    data = {
        'title':'Поиск',
        'video_list':video_list,
    }

    return render(request, 'denisvideo/search.html', data)


@login_required
def video_by_using_type(request):
    if request.GET.get('type') in ('liked_videos', 'later_videos'):
        videos = getattr(request.user, request.GET.get('type')).all()[::-1]
    elif request.GET.get('type') == 'views':
        videos = Video.objects.filter(views__user = request.user).order_by('-time_create')
    else:
        raise Http404()

    data = {
        'title':'Список видео',
        'videos':videos,
    }

    return render(request, 'denisvideo/video_by_using_type.html', data)


def video_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug = slug)
    videos = Video.objects.filter(tags = tag)

    data = {
        'title': f'Видео по теме: {tag.name}',
        'videos':videos,
    }

    return render(request, 'denisvideo/index.html', data)


@login_required
def add_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('my_videos')
    else:
        form = VideoForm()

    data = {
        'title': 'Загрузка видео',
        'form': form,
    }
    return render(request, 'denisvideo/add_video.html', data)


def show_my_videos(request):
    videos = Video.objects.filter(user = request.user)

    data = {'title':'Мои видео',
            'videos':videos,}

    return render(request, 'denisvideo/video_by_using_type.html', data)