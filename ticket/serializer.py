from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'priority', 'status', 'subject', 'description', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
