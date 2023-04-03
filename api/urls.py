from django.urls import path, include
from .views import (
    UserViewSet,
    UserCreateAPIView,
    UserTicketsListAPIView,
    TicketCreateAPIView,
    TicketUpdateAPIView,
    TicketDetailAPIView,
    TicketRestoreAPIView,
    TicketResolveAPIView,
    TicketRejectAPIView,
    TicketsInProgressListAPIView,
    TicketsResolvedListAPIView,
    TicketsRejectedListAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
    CustomTokenCreateView,
)


urlpatterns = [
    path('api/api/auth/token/login/', CustomTokenCreateView.as_view()),
    
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    
    path('api/users/', UserViewSet.as_view()),
    path('api/users/create/', UserCreateAPIView.as_view()),
    
    path('api/user/tickets/', UserTicketsListAPIView.as_view()),
    path('api/in_progress/tickets/', TicketsInProgressListAPIView.as_view()),
    path('api/resolved/tickets/', TicketsResolvedListAPIView.as_view()),
    path('api/rejected/tickets/', TicketsRejectedListAPIView.as_view()),
    
    path('api/ticket/create/', TicketCreateAPIView.as_view()),
    path('api/ticket/<pk>/update/', TicketUpdateAPIView.as_view()),
    path('api/ticket/<pk>/detail/', TicketDetailAPIView.as_view()),
    path('api/ticket/<pk>/restore/', TicketRestoreAPIView.as_view()),
    path('api/ticket/<pk>/resolve/', TicketResolveAPIView.as_view()),
    path('api/ticket/<pk>/reject/', TicketRejectAPIView.as_view()),
    
    path('api/ticket/<pk>/comments/', CommentListAPIView.as_view()),
    path('api/ticket/<pk>/comments/create/', CommentCreateAPIView.as_view()),
]