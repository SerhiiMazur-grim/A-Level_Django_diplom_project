from django.urls import path, include
from .views import (
    UserViewSet,
    UserCreateAPIView,
    UserTicketsListAPIView,
    UserFilterTicketsListAPIView,
    TicketCreateAPIView,
    TicketUpdateAPIView,
    TicketDetailAPIView,
    TicketInProgressAPIView,
    TicketRestoreAPIView,
    TicketResolveAPIView,
    TicketRejectAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
    CustomTokenCreateView,
)
from djoser.views import TokenDestroyView


urlpatterns = [
    path('api/auth/token/login/', CustomTokenCreateView.as_view()),
    path('api/auth/token/logout/', TokenDestroyView.as_view()),
    
    path('api/users/', UserViewSet.as_view()),
    path('api/user/create/', UserCreateAPIView.as_view()),
    
    path('api/user/tickets/', UserTicketsListAPIView.as_view()),
    path('api/user/tickets/filter/', UserFilterTicketsListAPIView.as_view()),
    
    path('api/ticket/create/', TicketCreateAPIView.as_view()),
    path('api/ticket/<pk>/update/', TicketUpdateAPIView.as_view()),
    path('api/ticket/<pk>/detail/', TicketDetailAPIView.as_view()),
    path('api/ticket/<pk>/in_progress/', TicketInProgressAPIView.as_view()),
    path('api/ticket/<pk>/restore/', TicketRestoreAPIView.as_view()),
    path('api/ticket/<pk>/resolve/', TicketResolveAPIView.as_view()),
    path('api/ticket/<pk>/reject/', TicketRejectAPIView.as_view()),
    
    path('api/ticket/<pk>/comments/', CommentListAPIView.as_view()),
    path('api/ticket/<pk>/comment/create/', CommentCreateAPIView.as_view()),
]