from django.urls import path

from .views import (
    TicketListView,
    TicketCreateView,
    TicketUpdateView,
    TicketDetailView,
    TicketRestoreView,
    TicketInProgressView,
    TicketResolvedView,
    TicketRejectedView,
    TicketFilterListView,
)


urlpatterns = [
    path('', TicketListView.as_view(), name='tickets_list'),
    path('tickets_list/', TicketListView.as_view(), name='tickets_list'),
    path('tickets_list/filtered/', TicketFilterListView.as_view(), name='filter_tickets_list'),
    path('<pk>/detail_ticket/', TicketDetailView.as_view(), name='detail_ticket'),
    
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('<pk>/update_ticket/', TicketUpdateView.as_view(), name='update_ticket'),
    path('ticket/<pk>/resolve/', TicketResolvedView.as_view(), name='ticket_resolve'),
    path('ticket/<pk>/reject/', TicketRejectedView.as_view(), name='ticket_reject'),
    path('ticket/<pk>/restore/', TicketRestoreView.as_view(), name='ticket_restore'),
    path('ticket/<pk>/in_progress/', TicketInProgressView.as_view(), name='ticket_in_progress'),
]
