from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Comment
from ticket.models import Ticket


class CommentCreateView(View):
    def post(self, request, pk):
        ticket = Ticket.objects.get(pk=pk)
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
