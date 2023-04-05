from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CustomUserLoginForm, CustomUserCreationForm


class CustomLoginView(LoginView):
    
    """
    A custom view for user authentication.

    The user is redirected to different URLs depending on whether they are an admin or a regular user.
    """
    
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('tickets_list')
    template_name = 'users/login.html'
    
    def get_success_url(self):
        
        """
        Returns the appropriate success URL based on whether the user is an admin or a regular user.
        """
        
        if self.request.user.is_staff:
            return self.success_url + 'filtered/?status=In progress'
        else:
            return self.success_url


class CustomUserCreateView(CreateView):
    
    """
    View for user registration.
    """
    
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login_dj')
    template_name = 'users/registration.html'


@method_decorator(login_required, name='dispatch')
class CustomLogoutView(LogoutView):
    
    """
    A view that logs out the current user and redirects to the login page.
    """

    next_page = reverse_lazy('login_dj')

    def get_next_page(self):
        """
        Returns the URL to redirect to after logout.

        This method is used to override the `next_page` attribute so that it
        can be constructed dynamically from the URL name.
        """
        return self.next_page
