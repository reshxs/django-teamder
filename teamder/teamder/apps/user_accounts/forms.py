from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ConfigurationForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "placeholder": "Никнейм",
        "class": "form-control"
    }))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Имя',
        "class": "form-control"
    }))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'placeholder': 'Фамилия',
        "class": "form-control"
    }))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={
        'placeholder': 'Email',
        "class": "form-control"
    }))
    bio = forms.CharField(max_length=300, widget=forms.Textarea(attrs={
        'placeholder': 'О себе',
        "class": "form-control",
        "rows": "3"
    }))

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'bio')
