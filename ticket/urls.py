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
    TicketToRestoreListView,
    TicketInProgressListView,
    TicketResolvedListView,
    TicketRejectedListView,
)


urlpatterns = [
    path('', TicketListView.as_view(), name='tickets_list'),
    path('tickets_list/', TicketListView.as_view(), name='tickets_list'),
    path('in_progress_tickets_list/', TicketInProgressListView.as_view(), name='in_progress_tickets_list'),
    path('resolved_tickets_list/', TicketResolvedListView.as_view(), name='resolved_tickets_list'),
    path('rejected_tickets_list/', TicketRejectedListView.as_view(), name='rejected_tickets_list'),
    path('restore_list/', TicketToRestoreListView.as_view(), name='restore_list'),
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('<pk>/update_ticket/', TicketUpdateView.as_view(), name='update_ticket'),
    path('<pk>/detail_ticket/', TicketDetailView.as_view(), name='detail_ticket'),
    path('ticket/<pk>/restore/', TicketRestoreView.as_view(), name='ticket_restore'),
    path('ticket/<pk>/in_progress/', TicketInProgressView.as_view(), name='ticket_in_progress'),
    path('ticket/<pk>/resolve/', TicketResolvedView.as_view(), name='ticket_resolve'),
    path('ticket/<pk>/reject/', TicketRejectedView.as_view(), name='ticket_reject'),
]
