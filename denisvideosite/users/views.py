from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import RegistrationForm, ProfileForm, ChannelForm
from users.models import Channel


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


class CreateChannel(LoginRequiredMixin, CreateView):
    form_class = ChannelForm
    extra_context = {'title':'Создание канала',}
    template_name = 'users/create_channel.html'

    def get(self, request, *args, **kwargs):
        if Channel.objects.filter(user = self.request.user).exists():
            raise Http404()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)