from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    
    """
    Serializer for Ticket model.
    """
    
    class Meta:
        model = Ticket
        fields = ('id', 'user', 'created_at', 'priority', 'status', 'subject', 'description')
