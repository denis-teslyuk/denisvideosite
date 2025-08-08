from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', 'photo']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email = email).exists():
            raise ValidationError('Пользователь с таким E-mail уже существует')
        return email