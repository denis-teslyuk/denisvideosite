from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse, reverse_lazy

from users import views

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html',
                                     extra_context={'title':'Вход',}), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationUser.as_view(), name='registration'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('create_channel/', views.CreateChannel.as_view(), name='create_channel'),

    path('password-change/', PasswordChangeView.as_view(template_name = 'users/password_change.html',
                                                        success_url = reverse_lazy('users:password_change_done')),
                                                        name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name = 'users/password_change_done.html'),
                                                                 name='password_change_done'),

    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset_fORm.html',
                                                      success_url=reverse_lazy('users:password_reset_done'),
                                                      email_template_name='users/password_reset_email.html'),
                                                      name='password_reset'),
    path('password-reset-done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
                                                               name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
                     PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                      success_url=reverse_lazy('users:password_reset_complete')),
                                                      name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
                                                                       name='password_reset_complete'),
]