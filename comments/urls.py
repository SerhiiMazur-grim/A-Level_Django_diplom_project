from django.urls import path

from .views import CommentCreateView

urlpatterns = [
    path('comment/<pk>/create/', CommentCreateView.as_view(), name='comment_create'),
    # path('ticket/<pk>/restore/', TicketRestoreView.as_view(), name='ticket_restore'),
]
