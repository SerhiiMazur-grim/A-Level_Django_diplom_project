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
)


urlpatterns = [
    path('api/auth/', include('rest_framework.urls')),
    
    path('api/users/', UserViewSet.as_view()),
    path('api/users/create/', UserCreateAPIView.as_view()),
    
    path('api/user/tickets/', UserTicketsListAPIView.as_view()),
    path('api/in_progress/tickets/', TicketsInProgressListAPIView.as_view()),
    path('api/resolved/tickets/', TicketsResolvedListAPIView.as_view()),
    path('api/rejected/tickets/', TicketsRejectedListAPIView.as_view()),
    path('api/tickets/create/', TicketCreateAPIView.as_view()),
    path('api/tickets/<pk>/update/', TicketUpdateAPIView.as_view()),
    path('api/tickets/<pk>/detail/', TicketDetailAPIView.as_view()),
    path('api/tickets/<pk>/restore/', TicketRestoreAPIView.as_view()),
    path('api/tickets/<pk>/resolve/', TicketResolveAPIView.as_view()),
    path('api/tickets/<pk>/reject/', TicketRejectAPIView.as_view()),
    
    path('api/ticket/<pk>/comments/', CommentListAPIView.as_view()),
    path('api/ticket/<pk>/comments/create/', CommentCreateAPIView.as_view()),
]