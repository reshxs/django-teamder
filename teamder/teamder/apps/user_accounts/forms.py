from django import forms
from django.contrib.auth.models import User
from .models import UserAccount


class RegistrationForm(forms.Form):
    login = forms.CharField(label='Никнейм', max_length=20)
    email = forms.EmailField(label='Почта')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_repeated = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    first_name = forms.CharField(label='Имя', max_length=25)
    last_name = forms.CharField(label='Фамилия', max_length=25)
    bio = forms.CharField(label='О себе', widget=forms.TextInput)

    class Meta:
        fields = ('login', 'email', 'first_name', 'last_name', 'bio', 'password', 'password_repeated',)
