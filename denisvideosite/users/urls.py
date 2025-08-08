from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     extra_context={'title':'Вход',}), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationUser.as_view(), name='registration')
]