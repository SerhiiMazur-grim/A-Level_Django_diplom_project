from django.urls import path, include
from .views import UserViewSet


urlpatterns = [
    path('api/users/', UserViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]