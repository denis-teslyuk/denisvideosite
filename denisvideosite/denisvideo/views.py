import random

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta

from denisvideo.forms import VideoForm
from denisvideo.models import Video, Tag
from denisvideo.utils import create_view, increment_view_count, get_side_videos, get_recommended_videos, \
    add_videos_to_needs_num
from users.models import Channel


# Create your views here.
def index(request):
    videos = []
    num_vid_per_page = 10
    if request.user.is_authenticated:
        videos = get_recommended_videos(request, num_vid_per_page)

    videos = add_videos_to_needs_num(videos, num_vid_per_page)

    data = {
        'title': 'Домашняя страница',
        'videos': videos,
    }

    return render(request, 'denisvideo/index.html', data)


def show_video(request, slug):
    try:
        video = Video.objects.select_related('user').get(slug = slug)
    except ObjectDoesNotExist:
        raise Http404()
    side_videos = get_side_videos(video)

    create_view(request, video)
    increment_view_count(video)

    likes_count = video.likers.count()
    dislikes_count = video.dislikers.count()

    data = {
        'title': video.name,
        'video': video,
        'side_videos': side_videos,
        'likes_count': likes_count,
        'dislikes_count':dislikes_count,
        'subed': request.user in video.user.channel.subscribers.all(),
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
        videos = Video.objects.filter(views__user = request.user).order_by('-views__time_create')
    else:
        raise Http404()

    paginator = Paginator(videos, 10)
    page = paginator.get_page(request.GET.get('page', 1))

    data = {
        'title':'Список видео',
        'page':page,
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
    if not Channel.objects.filter(user=request.user).exists():
        return redirect('users:create_channel')
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
        'button_text': 'Загрузить',
    }

    return render(request, 'denisvideo/add_video.html', data)


@login_required
def show_my_videos(request):
    if not Channel.objects.filter(user=request.user).exists():
        return redirect('users:create_channel')
    videos = Video.objects.filter(user = request.user)

    data = {'title':'Мои видео',
            'videos':videos,}

    return render(request, 'denisvideo/my_videos.html', data)


def show_channel(request, slug):
    channel = get_object_or_404(Channel, slug=slug)
    videos = Video.objects.filter(user__channel = channel)

    data = {
        'title':channel.name,
        'videos':videos,
        'channel':channel,
        'subed': request.user in channel.subscribers.all(),
    }

    return render(request, 'denisvideo/channel.html', data)


@login_required
def show_subscribes(request):
    channels = request.user.subscribes.all()
    videos = Video.objects.filter(user__channel__in = channels).order_by('-time_create')

    data ={
        'title':'Подписки',
        'channels':channels,
        'videos': videos,
    }

    return render(request, 'denisvideo/subscribes.html',data)


@login_required
def update_video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if video.user != request.user:
        raise Http404()

    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('my_videos')
    else:
        form = VideoForm(instance=video)

    data = {
        'title':'Изменить видео',
        'form': form,
        'button_text': 'Изменить',
    }

    return render(request, 'denisvideo/add_video.html', data)


@login_required
def delete_video(request, slug):
    video = get_object_or_404(Video, slug=slug)
    if request.user != video.user:
        raise Http404()
    video.delete()
    return redirect('my_videos')

