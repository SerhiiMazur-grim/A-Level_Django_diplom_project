from django.contrib.auth.hashers import make_password
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveAPIView,
    GenericAPIView,
)
from rest_framework.response import Response
from rest_framework import status, serializers, permissions

from djoser.views import TokenCreateView
from djoser import utils
from djoser.conf import settings

from users.models import CustomUser
from users.serializer import UserSerializer
from ticket.models import Ticket
from ticket.serializer import TicketSerializer
from comments.models import Comment
from comments.serializer import CommentSerializer

from .permissions import IsOwnerOrReadOnly


class CustomTokenCreateView(TokenCreateView):
    serializer_class = settings.SERIALIZERS.token_create
    permission_classes = settings.PERMISSIONS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        user = CustomUser.objects.get(pk=serializer.user.pk)
        user.cls_last_activity()
        print(serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data, status=status.HTTP_200_OK
        )

class UserViewSet(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    # queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)


class UserTicketsListAPIView(ListAPIView):
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        print(self.request.user)
        return Ticket.objects.filter(user=self.request.user)


class TicketCreateAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TicketSerializer

class TicketUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = TicketSerializer
    
    def get_object(self):
        obj = Ticket.objects.get(pk=self.kwargs['pk'])
        return obj


class TicketDetailAPIView(RetrieveAPIView):
    serializer_class = TicketSerializer
    
    def get_object(self):
        obj = Ticket.objects.get(pk=self.kwargs['pk'])
        return obj


class TicketRestoreAPIView(GenericAPIView):
    serializer_class = TicketSerializer

    def post(self, request, pk):
        ticket = self.get_object()
        ticket.restored()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    def get_object(self):
        obj = Ticket.objects.get(pk=self.kwargs['pk'])
        return obj


class TicketResolveAPIView(GenericAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        ticket = self.get_object()
        ticket.resolved()
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    def get_object(self):
        obj = Ticket.objects.get(pk=self.kwargs['pk'])
        return obj


class TicketRejectAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
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
        ticket = Ticket.objects.get(pk=self.kwargs['pk'])
        return ticket


class TicketsInProgressListAPIView(ListAPIView):
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='In progress')
        else:
            queryset = Ticket.objects.filter(status='In progress', user=self.request.user)
        return queryset.order_by('-created_at')


class TicketsResolvedListAPIView(ListAPIView):
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='Resolved')
        else:
            queryset = Ticket.objects.filter(status='Resolved', user=self.request.user)
        return queryset.order_by('-created_at')


class TicketsRejectedListAPIView(ListAPIView):
    serializer_class = TicketSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Ticket.objects.filter(status='Rejected')
        else:
            queryset = Ticket.objects.filter(status='Rejected', user=self.request.user)
        return queryset.order_by('-created_at')


class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        comments = Comment.objects.filter(ticket=self.kwargs['pk'])
        return comments


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
