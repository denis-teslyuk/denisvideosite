from django.urls import path

from denisvideo import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('show_video/<slug:slug>/', views.show_video, name = 'show_video'),
    path('add_like_or_dislike/<slug:slug>/', views.add_like_or_dislike, name = 'add_like_or_dislike')
]