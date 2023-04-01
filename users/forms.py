from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    
    """
    A form for creating a new user, including all the required fields plus password confirmation.
    Inherits from the built-in UserCreationForm and adds customizations to the form fields.
    """

    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light', 
        'placeholder': 'Username'
        }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light', 
        'placeholder': 'Email'
        }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light', 
        'placeholder': 'First Name'
        }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light', 
        'placeholder': 'Last Name'
        }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light', 
        'type': 'password', 
        'placeholder': 'Password'
        }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light', 
        'type': 'password', 
        'placeholder': 'Confirm Password'
        }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)


class CustomUserLoginForm(AuthenticationForm):
    
    """
    A custom authentication form for CustomUser model.
    Inherits from AuthenticationForm which is the default Django form for authentication.
    """

    username = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder':'Enter Username'
                }))
    
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': "Password",
                }))

    class Meta:
        model = CustomUser
