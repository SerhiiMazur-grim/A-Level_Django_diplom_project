from rest_framework import serializers

from .models import Comment
from ticket.models import Ticket


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'ticket']
        read_only_fields = ['author', 'ticket']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        ticket_pk = self.context['view'].kwargs['pk']
        ticket = Ticket.objects.get(pk=ticket_pk)
        validated_data['ticket'] = ticket
        return super().create(validated_data)
