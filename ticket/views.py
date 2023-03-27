from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .models import Ticket
from comments.models import Comment


class TicketCreateView(CreateView):
    model = Ticket
    fields = ['priority', 'subject', 'description']
    template_name = 'ticket/create_ticket.html'
    success_url = reverse_lazy('tickets_list')
    context_object_name = 'ticket'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ['priority', 'subject', 'description']
    template_name = 'ticket/update_ticket.html'
    success_url = reverse_lazy('tickets_list')
    context_object_name = 'ticket'


class TicketDetailView(DetailView):
    model = Ticket
    template_name = 'ticket/detail_ticket.html'
    context_object_name = 'ticket'


class TicketListView(ListView):
    model = Ticket
    template_name = 'ticket/my_tickets.html'
    context_object_name = 'tickets'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status=Ticket.STATUS_IN_PROGRESS)
        else:
            queryset = Ticket.objects.filter(user=self.request.user).exclude(status=Ticket.STATUS_RESTORED)
        return queryset.order_by('-created_at')


class TicketRestoreView(View):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.restored()
        return redirect('tickets_list')

    def get_object(self):
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketResolvedView(View):
    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.resolved()
        return redirect('tickets_list')

    def get_object(self):
        return Ticket.objects.get(pk=self.kwargs['pk'])


class TicketRejectedView(CreateView):
    model = Comment
    template_name = 'ticket/ticket_reject.html'
    fields = ['text']
    success_url = reverse_lazy('tickets_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))
        context['ticket'] = ticket
        return context

    def form_valid(self, form):
        comment_text = form.cleaned_data.get('text')
        ticket = Ticket.objects.get(pk=self.kwargs.get('pk'))

        if not comment_text:
            form.add_error('text', 'Comment cannot be empty')
            return self.form_invalid(form)

        form.instance.author = self.request.user
        form.instance.ticket = ticket
        form.instance.text = comment_text

        ticket.rejected()
        return super().form_valid(form)


class TicketToRestoreListView(ListView):
    model = Ticket
    template_name = 'ticket/restore_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        queryset = Ticket.objects.filter(status='Restored')
        return queryset.order_by('-created_at')


class TicketInProgressListView(ListView):
    model = Ticket
    template_name = 'ticket/in_progress_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='In progress')
        else:
            queryset = Ticket.objects.filter(status='In progress', user=self.request.user)
        return queryset.order_by('-created_at')


class TicketResolvedListView(ListView):
    model = Ticket
    template_name = 'ticket/resolved_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='Resolved')
        else:
            queryset = Ticket.objects.filter(status='Resolved', user=self.request.user)
        return queryset.order_by('-created_at')


class TicketRejectedListView(ListView):
    model = Ticket
    template_name = 'ticket/rejected_tickets.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='Rejected')
        else:
            queryset = Ticket.objects.filter(status='Rejected', user=self.request.user)
        return queryset.order_by('-created_at')
