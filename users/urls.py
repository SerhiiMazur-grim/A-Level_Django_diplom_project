from django.urls import path

from .views import CustomLoginView, CustomUserCreateView, CustomLogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login_dj'),
    path('registration/', CustomUserCreateView.as_view(), name='registration_dj'),
    path('logout/', CustomLogoutView.as_view(), name='logout_dj'),
]
