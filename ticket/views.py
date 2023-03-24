from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy

from .models import Ticket




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
        if self.request.user.is_authenticated:
            queryset = Ticket.objects.filter(user=self.request.user)
        else:
            queryset = Ticket.objects.none()
        return queryset


class TicketLowPriorityListView(ListView):
    model = Ticket
    template_name = 'ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(priority='low')


class TicketMediumPriorityListView(ListView):
    model = Ticket
    template_name = 'ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(priority='Medium')


class TicketHighPriorityListView(ListView):
    model = Ticket
    template_name = 'ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        return Ticket.objects.filter(priority='High')
