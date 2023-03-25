from django.urls import path

from .views import (
    TicketListView,
    TicketCreateView,
    TicketUpdateView,
    TicketDetailView,
    TicketRestoreView
)


urlpatterns = [
    path('', TicketListView.as_view(), name='tickets_list'),
    path('tickets_list/', TicketListView.as_view(), name='tickets_list'),
    path('create_ticket/', TicketCreateView.as_view(), name='create_ticket'),
    path('<pk>/update_ticket/', TicketUpdateView.as_view(), name='update_ticket'),
    path('<pk>/detail_ticket/', TicketDetailView.as_view(), name='detail_ticket'),
    path('ticket/<pk>/restore/', TicketRestoreView.as_view(), name='ticket_restore'),
]
