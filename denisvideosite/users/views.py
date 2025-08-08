from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import RegistrationForm, ProfileForm


# Create your views here.
class RegistrationUser(CreateView):
    form_class = RegistrationForm
    extra_context = {'title': 'Регистрация',}
    template_name = 'users/registration.html'

    def get_success_url(self):
        return reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = data['object']
        return data

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk = self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('users:profile')

