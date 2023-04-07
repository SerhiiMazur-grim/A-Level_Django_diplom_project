from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import Http404

from .models import Ticket
from .forms import TicketForm
from comments.models import Comment
from comments.forms import CommentForm

from .permissions import IsOwnerPermissions, IsOwnerOrAdminPermissions, IsAdminPermissions


class TicketCreateView(CreateView):
    
    """
    View for creating new tickets.
    """
    
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/create_ticket.html'
    success_url = reverse_lazy('tickets_list')
    context_object_name = 'ticket'

    def form_valid(self, form):
        """
        If the form is valid, sets the user of the new ticket to the current user and displays a success message.
        """
        form.instance.user = self.request.user
        messages.success(self.request, 'Ticket created successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        If the form is invalid, displays an error message.
        """
        messages.error(self.request, 'Ticket creation failed!')
        return super().form_invalid(form)


class TicketUpdateView(IsOwnerPermissions, UpdateView):
    
    """
    A view for updating a ticket.
    """
    
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/update_ticket.html'
    context_object_name = 'ticket'

    def get_success_url(self):
        """
        Gets the URL to redirect to upon successful form submission.
        """
        messages.success(self.request, 'Ticket updated successfully')
        return reverse_lazy('detail_ticket', kwargs={'pk': self.object.pk})

    def form_invalid(self, form):
        """
        Handles invalid form submission.
        """
        messages.error(self.request, 'Ticket update failed')
        return super().form_invalid(form)


class TicketDetailView(IsOwnerOrAdminPermissions, DetailView):
    
    """
    A view that displays the details of a single ticket object.
    """
    
    model = Ticket
    template_name = 'ticket/detail_ticket.html'
    context_object_name = 'ticket'


class TicketListView(ListView):
    
    """
    View for displaying a list of all tickets belonging to the current user.
    If the user is a superuser, all tickets will be displayed.
    """
    
    model = Ticket
    template_name = 'ticket/my_tickets_list.html'
    context_object_name = 'tickets'
    
    def get_queryset(self):
        """
        Returns the queryset of tickets to be displayed in the template.
        If the user is a superuser, all tickets will be included.
        Otherwise, only tickets belonging to the current user will be included,
        except for those that have been restored.
        """
        if self.request.user.is_staff:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(user=self.request.user).exclude(status=Ticket.STATUS_RESTORED)
        return queryset.order_by('-created_at')


class TicketFilterListView(ListView):
    
    """
    A view that displays a filtered list of tickets based on the status parameter in the URL.
    """
    
    model = Ticket
    template_name = 'ticket/filtered_ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        """
        Return a queryset of tickets filtered by the status parameter in the URL.
        """
        status = self.request.GET.get('status')
        valid_statuses = [choice[0] for choice in Ticket.STATUS_CHOICES]
        if status not in valid_statuses:
            raise Http404("Invalid status provided.")

        if self.request.user.is_staff:
            queryset = Ticket.objects.filter(status=status)
        else:
            queryset = Ticket.objects.filter(status=status, user=self.request.user)
        return queryset.order_by('-created_at')


class TicketRestoreView(IsOwnerPermissions, View):
    
    """
    View for changing the status of a ticket to 'Restored'.
    """
    
    def post(self, request, *args, **kwargs):
        """
    Handles the POST request to restore a rejected ticket.
    
    A redirect to either the rejected_tickets_list view if the user is admin,
    or to the tickets_list view if the user is not admin.
    """
        ticket = self.get_object()
        if ticket.status == Ticket.STATUS_REJECTED:
            ticket.restored()
            messages.success(self.request, 'Ticket restored successfully')
            return redirect('tickets_list')
        raise Http404

    def get_object(self):
        """
        Get the ticket object from the URL parameter.
        """
        try:
            ticket = Ticket.objects.get(pk=self.kwargs['pk'])
            return ticket
        except:
            raise Http404


class TicketInProgressView(IsAdminPermissions, View):
    
    """
    View for changing the status of a ticket to 'In progress'.
    """
    
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.status == Ticket.STATUS_RESTORED:
            ticket.in_progress()
            messages.success(self.request, 'Ticket restored successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        raise Http404

    def get_object(self):
        """
        Get the ticket object from the URL parameter.
        """
        try:
            return Ticket.objects.get(pk=self.kwargs['pk'])
        except:
            raise Http404


class TicketResolvedView(IsAdminPermissions, View):
    
    """
    View for changing the status of a ticket to 'Resolved'.
    """
    
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        if ticket.status == Ticket.STATUS_IN_PROGRESS:
            ticket.resolved()
            messages.success(self.request, 'Ticket resolved successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        raise Http404

    def get_object(self):
        """
        Get the ticket object from the URL parameter.
        """
        try:
            return Ticket.objects.get(pk=self.kwargs['pk'])
        except:
            raise Http404


class TicketRejectedView(IsAdminPermissions, CreateView):
    
    """
    A view for rejecting a ticket and adding a comment to it.
    """
    
    form_class = CommentForm
    model = Comment
    template_name = 'ticket/ticket_reject.html'
    
    def get_success_url(self):
        """
        Get the URL to redirect to after a successful form submission.
        """
        status = Ticket.STATUS_IN_PROGRESS
        url = reverse('filter_tickets_list')
        return f"{url}?status={status}"

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        if ticket.status == Ticket.STATUS_IN_PROGRESS or ticket.status == Ticket.STATUS_RESTORED:
            context['ticket'] = ticket
            return context
        raise Http404

    def form_valid(self, form):
        """
        Called when the form is successfully validated.
        """
        comment_text = form.cleaned_data.get('text')
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        if ticket.status == Ticket.STATUS_IN_PROGRESS or ticket.status == Ticket.STATUS_RESTORED:
            if not comment_text:
                form.add_error('text', 'Comment cannot be empty')
                return self.form_invalid(form)
        
            form.instance.author = self.request.user
            form.instance.ticket = ticket
            form.instance.text = comment_text

            ticket.rejected()
            messages.success(self.request, 'Ticket was successfully rejected')
            return super().form_valid(form)

        raise Http404