from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(required=True, label="Username", widget=forms.TextInput(attrs={
        'class': 'form-control bg-secondary', 
        'placeholder': 'Username'
        }))
    email = forms.EmailField(required=True, label="Email", widget=forms.TextInput(attrs={
        'class': 'form-control bg-secondary', 
        'placeholder': 'Email'
        }))
    first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={
        'class': 'form-control bg-secondary', 
        'placeholder': 'First Name'
        }))
    last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={
        'class': 'form-control bg-secondary', 
        'placeholder': 'Last Name'
        }))
    password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-secondary', 
        'type': 'password', 
        'placeholder': 'Password'
        }))
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-secondary', 
        'type': 'password', 
        'placeholder': 'Confirm Password'
        }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class CustomUserLoginForm(AuthenticationForm):

    username = forms.CharField(label='Enter username', widget=forms.TextInput(attrs={
                'class': 'form-control bg-secondary',
                'id': 'username',
                'placeholder':'Enter Username'
                }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control bg-secondary',
                'id': "password",
                'placeholder': "Password",
                }))
    class Meta:
        model = CustomUser