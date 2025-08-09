from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from users.models import Channel


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2', 'email', 'photo')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email = email).exists():
            raise ValidationError('Пользователь с таким E-mail уже существует')
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('photo','username', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        old_email = self.instance.email
        if email == old_email or not get_user_model().objects.filter(email=email).exists():
            return email
        raise ValidationError('Пользователь с таким E-mail уже существует')


    def clean_username(self):
        username = self.cleaned_data['username']
        old_username = self.instance.username
        if old_username == username or not get_user_model().objects.filter(username=username).exists():
            return username
        raise ValidationError('Пользователь с таким именем уже существует')


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ('name', 'description')

    def clean_name(self):
        name = self.cleaned_data['name']
        if not self.instance and Channel.objects.filter(name=name).exists():
            raise ValidationError('Канал с таким названием уже существует')
        return name



