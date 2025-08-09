from django.urls import path

from denisvideo import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('show_video/<slug:slug>/', views.show_video, name = 'show_video'),
    path('add_like_or_dislike/<slug:slug>/', views.add_like_or_dislike, name = 'add_like_or_dislike'),
    path('search/', views.search, name='search'),
    path('video_by_using_type/', views.video_by_using_type, name='video_by_using_type'),
    path('video_by_tag/<slug:slug>/', views.video_by_tag, name='video_by_tag'),
    path('add_watch_later/<slug:slug>/', views.add_watch_later, name='add_watch_later'),
    path('add_video/', views.add_video, name='add_video'),
    path('update_video/<slug:slug>/', views.update_video, name='update_video'),
    path('delete_video/<slug:slug>/', views.delete_video, name='delete_video'),
    path('my_videos/', views.show_my_videos, name='my_videos'),
    path('channel/<slug:slug>/', views.show_channel, name='channel'),
    path('subscribes_content/', views.show_subscribes, name='subscribes_content'),
]