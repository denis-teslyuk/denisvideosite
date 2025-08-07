from django.urls import path

from denisvideo import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('show_video/<slug:slug>/', views.show_video, name = 'show_video'),
]