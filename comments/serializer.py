from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    
    """
    Serializer for the Comment model.
    """
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'ticket', 'text', 'created_date']
