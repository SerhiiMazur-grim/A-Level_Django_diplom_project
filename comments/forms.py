from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-light', 'id': 'comment-text', 'rows': '3', 'name': 'comment_text'}))
    
    class Meta:
        model = Comment
        fields = ['text']
