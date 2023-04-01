from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):
    
    """
    A form used to create or update a ticket.
    """
    
    class Meta:
        model = Ticket
        fields = ['priority', 'subject', 'description']
        widgets = {
            'priority': forms.Select(attrs={'class': 'form-control bg-dark text-light'}),
            'subject': forms.TextInput(attrs={'class': 'form-control bg-dark text-light'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-dark text-light', 'rows': 5}),
        }
