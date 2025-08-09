from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from denisvideo.models import Video
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
    extra_context = {'title':'Создание канала','button_text':'Создать',}
    template_name = 'users/manipulate_channel.html'

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


class UpdateChannel(LoginRequiredMixin, UpdateView):
    form_class = ChannelForm
    extra_context = {'title': 'Изменение канала', 'button_text':'Обновить',}
    template_name = 'users/manipulate_channel.html'

    def get_object(self, queryset=None):
        try:
            return Channel.objects.get(user = self.request.user)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('users:create_channel'))

    def get_success_url(self):
        return reverse_lazy('users:profile')


class DeleteChannel(LoginRequiredMixin, DeleteView):
    model = Channel
    extra_context = {'title': 'Удаление канала', 'button_text': 'Удалить', }
    template_name = 'users/manipulate_channel.html'

    def get_object(self, queryset=None):
        try:
            return Channel.objects.get(user = self.request.user)
        except ObjectDoesNotExist:
            return redirect(reverse_lazy('users:create_channel'))

    def get_success_url(self):
        return reverse_lazy('users:profile')


class Subscribe(LoginRequiredMixin, View):
    def get(self,request, slug, *args, **kwargs):
        channel = get_object_or_404(Channel, slug = slug)
        if channel.user == request.user:
            redirect(request.META.get('HTTP_REFERER'))
        if self.request.user in channel.subscribers.all():
            channel.subscribers.remove(self.request.user)
        else:
            channel.subscribers.add(self.request.user)
        return redirect(request.META.get('HTTP_REFERER'))