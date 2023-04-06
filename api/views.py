from django.contrib.auth.hashers import make_password
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)
from djoser.views import TokenCreateView
from djoser import utils
from djoser.conf import settings

from users.models import CustomUser
from users.serializer import UserSerializer
from ticket.models import Ticket
from ticket.serializer import TicketSerializer
from comments.models import Comment
from comments.serializer import CommentSerializer

from .permissions import IsOwnerOrAdmin, IsOwner


class CustomTokenCreateView(TokenCreateView):
    
    """
    A view that overrides the default TokenCreateView to include additional functionality.
    """
    
    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        """
        Custom method that performs the token creation action and includes additional functionality.
        """
        token = utils.login_user(self.request, serializer.user)
        user = CustomUser.objects.get(pk=serializer.user.pk)
        user.cls_last_activity()
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_200_OK
        )


class UserCreateAPIView(CreateAPIView):
    
    """
    API view for creating a new user.
    """
    
    permission_classes = [permissions.AllowAny]
    # queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Creates a new user with the given data.
        """
        password = make_password(self.request.data['password'])
        serializer.save(password=password)


class UserTicketsListAPIView(ListAPIView):
    
    """
    API view to retrieve a list of tickets associated with the authenticated user.
    """
    
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        """
        Returns a queryset of tickets associated with the authenticated user.
        """
        if self.request.user.is_staff:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(user=self.request.user).exclude(status=Ticket.STATUS_RESTORED)
        return queryset.order_by('-created_at')


class UserFilterTicketsListAPIView(ListAPIView):
    
    """
    API view that returns a list of tickets filtered by status for a specific user.
    """
    
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        """
        Returns the queryset of tickets that should be displayed in the response.
        """
        status = self.request.GET.get('status')
        valid_statuses = [choice[0] for choice in Ticket.STATUS_CHOICES]
        if status not in valid_statuses:
            raise Http404("Invalid status provided.")
        
        if self.request.user.is_staff:
            queryset = Ticket.objects.filter(status=status)
        else:
            queryset = Ticket.objects.filter(user=self.request.user, status=status).exclude(status=Ticket.STATUS_RESTORED)
        return queryset.order_by('-created_at')


class TicketCreateAPIView(CreateAPIView):
    """
    API view to create a new ticket.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer


class TicketUpdateAPIView(RetrieveUpdateAPIView):
    
    """
    API view to retrieve and update a single ticket instance by the authenticated owner user.
    """
    
    serializer_class = TicketSerializer
    permission_classes = [IsOwner]
    
    def get_object(self):
        """
        Retrieves the ticket object with the given primary key.
        """
        try:
            obj = Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key.')
        return obj


class TicketDetailAPIView(RetrieveAPIView):
    
    """
    A view for retrieving details of a single ticket.
    """
    
    serializer_class = TicketSerializer
    permission_classes = [IsOwnerOrAdmin]
    
    def get_object(self):
        """
        Retrieves the ticket object with the given primary key.
        """
        try:
            obj = Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key.')
        return obj


class TicketRestoreAPIView(GenericAPIView):
    
    """
    API view for changing the status of a ticket to 'restored'.
    """
    
    serializer_class = TicketSerializer
    permission_classes = [IsOwner]

    def post(self, request, pk):
        """
        Changes the status of the ticket with the given primary key to 'restored'.
        """
        ticket = self.get_object()
        if ticket.status == Ticket.STATUS_REJECTED:
            ticket.restored()
            serializer = self.get_serializer(ticket)
            return Response(serializer.data)
        raise Http404('Can`t restore this ticket.')
        

    def get_object(self):
        """
        Retrieves the ticket object with the given primary key.
        """
        try:
            obj = Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key.')
        
        return obj


class TicketResolveAPIView(GenericAPIView):
    
    """
    API view for changing the status of a ticket to 'resolved'.
    """
    
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        """
        Changes the status of the ticket with the given primary key to 'resolved'.
        """
        ticket = self.get_object()
        if ticket.status == Ticket.STATUS_IN_PROGRESS:
            ticket.resolved()
            serializer = self.get_serializer(ticket)
            return Response(serializer.data)
        raise Http404

    def get_object(self):
        """
        Retrieves the ticket object with the given primary key.
        """
        try:
            obj = Ticket.objects.get(pk=self.kwargs['pk'])
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key.')
        
        return obj


class TicketInProgressAPIView(GenericAPIView):
    
    """
    API view for changing the status of a ticket to 'in progress'.
    """
    
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        """
        Changes the status of the ticket with the given primary key to 'in progress'.
        """
        ticket = self.get_object()
        ticket.in_progress()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    def get_object(self):
        """
        Retrieves the ticket object with the given primary key.
        """
        try:
            ticket = Ticket.objects.get(pk=self.kwargs['pk'], status=Ticket.STATUS_RESTORED)
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key or status.')
        return ticket


class TicketRejectAPIView(CreateAPIView):
    
    """
    API view for rejecting a ticket and adding a comment.
    """
    
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        Create a comment and reject a ticket.
        """
        comment_text = request.data.get('text', '')
        ticket = self.get_ticket()
        
        if not comment_text:
            return Response({'error': 'Comment cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, ticket=ticket)

        ticket.rejected()
        return Response(serializer.data)

    def get_ticket(self):
        """
        Helper method to get the ticket object.
        """
        try:
            ticket = Ticket.objects.get(pk=self.kwargs['pk'], status=Ticket.STATUS_IN_PROGRESS)
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key or status.')
        return ticket


class CommentListAPIView(ListAPIView):
    
    """
    API view that returns a list of comments for a specific ticket.
    """
    
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        try:
            comments = Comment.objects.filter(ticket=self.kwargs['pk'])
        except Comment.DoesNotExist:
            raise Http404('No objects with the given primary key.')
        return comments.order_by('-created_date')


class CommentCreateAPIView(CreateAPIView):
    
    """
    API view to create a comment on a ticket.
    """
    
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrAdmin]
    
    def get_object(self):
        try:
            ticket = Ticket.objects.get(pk=self.kwargs['pk'], status=Ticket.STATUS_IN_PROGRESS)
        except Ticket.DoesNotExist:
            raise Http404('No object with the given primary key or status.')
        return ticket
