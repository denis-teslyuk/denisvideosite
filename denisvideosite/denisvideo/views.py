import random

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.forms import model_to_dict
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta

from denisvideo.forms import VideoForm
from denisvideo.models import View, Video, Tag
from denisvideo.utils import create_view, increment_view_count, get_side_videos
from users.models import Channel


# Create your views here.
def index(request):
    videos = []
    NUM_VID_PER_PAGE = 10
    if request.user.is_authenticated:
        user_views = View.objects.filter(user=request.user, time_create__gt = datetime.now() - timedelta(days=30))
        views_by_tag =  user_views.values('video__tags__pk').annotate(count = Count('pk'))
        total = 0
        for tag in views_by_tag:
            total += tag['count']

        count__vid_by_tag = {tag['video__tags__pk']: int(tag['count'] / total * NUM_VID_PER_PAGE) for tag in views_by_tag}

        for tag_pk, count in count__vid_by_tag.items():
            video_list = list(Video.objects.filter(tags__pk = tag_pk,time_create__gt = datetime.now() - timedelta(days=60)))
            count = len(video_list) if count > len(video_list) else count
            videos.extend(random.sample(video_list, k=count))

    video_list = Video.objects.all()
    while len(videos) != NUM_VID_PER_PAGE and len(videos) < len(video_list):
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

