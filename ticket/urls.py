from django.urls import path

from .views import (
    TicketListView,
    TicketCreateView,
    TicketUpdateView,
    TicketDetailView,
    TicketRestoreView,
    TicketResolvedView,
    TicketRejectedView,
    TicketToRestoreListView,
)


urlpatterns = [
    path('', TicketListView.as_view(), name='tickets_list'),
    path('tickets_list/', TicketListView.as_view(), name='tickets_list'),
    path('restore_list/', TicketToRestoreListView.as_view(), name='restore_list'),
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('<pk>/update_ticket/', TicketUpdateView.as_view(), name='update_ticket'),
    path('<pk>/detail_ticket/', TicketDetailView.as_view(), name='detail_ticket'),
    path('ticket/<pk>/restore/', TicketRestoreView.as_view(), name='ticket_restore'),
    path('ticket/<pk>/resolve/', TicketResolvedView.as_view(), name='ticket_resolve'),
    path('ticket/<pk>/reject/', TicketRejectedView.as_view(), name='ticket_reject'),
]
