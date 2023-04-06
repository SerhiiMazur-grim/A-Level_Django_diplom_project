from django.test import TestCase
from rest_framework import status
from django.urls import reverse

from ticket.models import Ticket
from users.models import CustomUser
from .models import Comment


class CommentCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpassword',
        )
        self.ticket = Ticket.objects.create(
            pk=1,
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_IN_PROGRESS,
            description='Test description 1'
        )
        self.url = reverse('comment_create', kwargs={'pk': self.ticket.pk})
        self.data = {'comment_text': 'Test comment'}
        self.data2 = {'comment_text': ''}
        
    def test_comment_create_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'Test comment')

    def test_comment_create_failed(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data2, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_comment_create_by_not_auth_user(self):
        response = self.client.post(self.url, self.data, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(Comment.objects.count(), 0)

