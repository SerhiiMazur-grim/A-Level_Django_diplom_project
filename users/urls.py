from django.urls import path

from .views import CustomLoginView, CustomUserCreateView, CustomLogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('registration/', CustomUserCreateView.as_view(), name='registration'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
