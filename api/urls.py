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
    path('api/auth/token/login/', CustomTokenCreateView.as_view(), name='api_login'),
    path('api/auth/token/logout/', TokenDestroyView.as_view(), name='api_logout'),
    
    path('api/users/', UserViewSet.as_view(), name='api_users_list'),
    path('api/user/create/', UserCreateAPIView.as_view(), name='api_create_user'),
    
    path('api/user/tickets/', UserTicketsListAPIView.as_view(), name='api_ticket_list'),
    path('api/user/tickets/filter/', UserFilterTicketsListAPIView.as_view(), name='api_filter_ticket_list'),
    
    path('api/ticket/create/', TicketCreateAPIView.as_view(), name='api_create_ticket'),
    path('api/ticket/<pk>/update/', TicketUpdateAPIView.as_view(), name='api_update_ticket'),
    path('api/ticket/<pk>/detail/', TicketDetailAPIView.as_view(), name='api_detail_ticket'),
    path('api/ticket/<pk>/in_progress/', TicketInProgressAPIView.as_view(), name='api_ticket_in_progress'),
    path('api/ticket/<pk>/restore/', TicketRestoreAPIView.as_view(), name='api_ticket_restored'),
    path('api/ticket/<pk>/resolve/', TicketResolveAPIView.as_view(), name='api_ticket_resolved'),
    path('api/ticket/<pk>/reject/', TicketRejectAPIView.as_view(), name='api_ticket_rejected'),
    
    path('api/ticket/<pk>/comments/', CommentListAPIView.as_view(), name='api_comment_list'),
    path('api/ticket/<pk>/comment/create/', CommentCreateAPIView.as_view(), name='api_create_comment'),
]
