from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserLoginForm, CustomUserCreationForm


class CustomLoginView(LoginView):
    form_class = CustomUserLoginForm
    user_success_url = reverse_lazy('tickets_list')
    admin_success_url = reverse_lazy('in_progress_tickets_list')
    template_name = 'users/login.html'
    
    def get_success_url(self):
        if self.request.user.is_staff:
            return self.admin_success_url
        else:
            return self.user_success_url


class CustomUserCreateView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login_dj')
    template_name = 'users/registration.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login_dj')

    def get_next_page(self):
        return self.next_page
