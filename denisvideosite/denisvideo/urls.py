from django.urls import path

from denisvideo import views

urlpatterns = [
    path('', views.index, name = 'index'),

]