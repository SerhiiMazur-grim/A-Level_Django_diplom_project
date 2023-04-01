from django.db import models

from users.models import CustomUser
from ticket.models import Ticket


class Comment(models.Model):
    
    """
    Model representing a comment on a ticket.
    """
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
