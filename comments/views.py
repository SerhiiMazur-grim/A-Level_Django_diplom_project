from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404

from .models import Comment
from ticket.models import Ticket


class CommentCreateView(View):
    
    """
    A view for creating comments on a ticket.
    """
    
    def post(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key.')
        comment_text = request.POST.get('comment_text')

        if not comment_text:
            messages.error(request, 'Comment cannot be empty')
            return redirect(request.META.get('HTTP_REFERER'))

        comment = Comment.objects.create(
            author=request.user,
            ticket=ticket,
            text=comment_text
        )
        messages.success(request, 'Comment added successfully')
        return redirect(request.META.get('HTTP_REFERER'))
