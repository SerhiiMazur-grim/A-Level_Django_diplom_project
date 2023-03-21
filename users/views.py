from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserLoginForm, CustomUserCreationForm


class CustomLoginView(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('home')
    template_name = 'users/login.html'
    
    def get_success_url(self):
        return self.success_url


class CustomUserCreateView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/registration.html'



class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def get_next_page(self):
        return self.next_page