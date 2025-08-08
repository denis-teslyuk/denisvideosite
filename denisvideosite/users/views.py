from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegistrationForm


# Create your views here.
class RegistrationUser(CreateView):
    form_class = RegistrationForm
    extra_context = {'title': 'Регистрация',}
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse_lazy('users:login')

