from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Ticket
from .forms import TicketForm
from comments.models import Comment
from comments.forms import CommentForm


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


class TicketUpdateView(UpdateView):
    
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


class TicketDetailView(DetailView):
    
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
    template_name = 'ticket/my_tickets.html'
    context_object_name = 'tickets'
    
    def get_queryset(self):
        """
        Returns the queryset of tickets to be displayed in the template.
        If the user is a superuser, all tickets will be included.
        Otherwise, only tickets belonging to the current user will be included,
        except for those that have been restored.
        """
        if self.request.user.is_superuser:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(user=self.request.user).exclude(status=Ticket.STATUS_RESTORED)
        return queryset.order_by('-created_at')


class TicketRestoreView(View):
    
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
        ticket.restored()
        messages.success(self.request, 'Ticket restored successfully')
        if self.request.user.is_staff:
            return redirect('rejected_tickets_list')
        else:
            return redirect('tickets_list')

    def get_object(self):
        """
        Get the ticket object from the URL parameter.
        """
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketInProgressView(View):
    
    """
    View for changing the status of a ticket to 'In progress'.
    """
    
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.in_progress()
        messages.success(self.request, 'Ticket restored successfully')
        return redirect(request.META.get('HTTP_REFERER'))

    def get_object(self):
        """
        Get the ticket object from the URL parameter.
        """
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketResolvedView(View):
    
    """
    View for changing the status of a ticket to 'Resolved'.
    """
    
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.resolved()
        messages.success(self.request, 'Ticket resolved successfully')
        return redirect(request.META.get('HTTP_REFERER'))

    def get_object(self):
        """
        Get the ticket object from the URL parameter.
        """
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketRejectedView(CreateView):
    
    """
    A view for rejecting a ticket and adding a comment to it.
    """
    
    form_class = CommentForm
    model = Comment
    template_name = 'ticket/ticket_reject.html'
    success_url = reverse_lazy('in_progress_tickets_list')

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.
        """
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        context['ticket'] = ticket
        return context

    def form_valid(self, form):
        """
        Called when the form is successfully validated.
        """
        comment_text = form.cleaned_data.get('text')
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))

        if not comment_text:
            form.add_error('text', 'Comment cannot be empty')
            return self.form_invalid(form)

        form.instance.author = self.request.user
        form.instance.ticket = ticket
        form.instance.text = comment_text

        ticket.rejected()
        messages.success(self.request, 'Ticket was successfully rejected')
        return super().form_valid(form)


class TicketToRestoreListView(ListView):
    
    """
    A view for displaying a list of tickets in 'Restored' status.
    """
    
    model = Ticket
    template_name = 'ticket/restore_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        """
        Get the queryset for the list of tickets to display.
        """
        queryset = Ticket.objects.filter(status='Restored')
        return queryset.order_by('-created_at')


class TicketInProgressListView(ListView):
    
    """
    A view that displays a list of tickets that are in progress.
    
    If the requesting user is a superuser, it displays all in progress tickets.
    If the requesting user is not a superuser, it displays only their in progress tickets.
    """
    
    model = Ticket
    template_name = 'ticket/in_progress_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        """
        Return a queryset of in progress tickets.
        
        If the user is a superuser, all 'in progress' tickets are returned. Otherwise,
        only the 'in progress' tickets created by the current user are returned.
        """
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='In progress')
        else:
            queryset = Ticket.objects.filter(status='In progress', user=self.request.user)
        return queryset.order_by('-created_at')


class TicketResolvedListView(ListView):
    
    """
    View for displaying a list of resolved tickets.

    If the user is a superuser, all 'resolved' tickets are displayed. Otherwise,
    only the 'resolved' tickets created by the current user are displayed.
    """
    
    model = Ticket
    template_name = 'ticket/resolved_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        """
        Returns the resolved tickets queryset.

        If the user is a superuser, all resolved tickets are returned. Otherwise,
        only the resolved tickets created by the current user are returned.
        """
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='Resolved')
        else:
            queryset = Ticket.objects.filter(status='Resolved', user=self.request.user)
        return queryset.order_by('-created_at')


class TicketRejectedListView(ListView):
    
    """
    A view that displays a list of rejected tickets.

    If the current user is a superuser, all rejected tickets will be displayed.
    Otherwise, only the rejected tickets created by the current user will be displayed.
    """
    
    model = Ticket
    template_name = 'ticket/rejected_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        """
        Returns the queryset of tickets to be displayed in the view.

        If the current user is a superuser, all 'rejected' tickets will be returned.
        Otherwise, only the 'rejected' tickets created by the current user will be returned.
        """
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='Rejected')
        else:
            queryset = Ticket.objects.filter(status='Rejected', user=self.request.user)
        return queryset.order_by('-created_at')
