from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse

from users.models import CustomUser
from comments.models import Comment
from .models import Ticket


class TicketCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass',
        )
        self.data = {
            'subject': 'Test Ticket',
            'description': 'Test Description',
            'priority': 'low',
        }
        self.url = reverse('create_ticket')
    
    def test_create_ticket(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tickets_list'))
        ticket = Ticket.objects.last()
        self.assertEqual(ticket.subject, self.data['subject'])
        self.assertEqual(ticket.description, self.data['description'])
        self.assertEqual(ticket.priority, self.data['priority'])
        self.assertEqual(ticket.user, self.user)

    def test_create_ticket_not_auth_user(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/accounts/login/?next=/create_ticket/')
        self.assertEqual(Ticket.objects.count(), 0)


class TicketUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass',
        )
        self.user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@gmail.com',
            password='testpass',
        )
        self.ticket=Ticket.objects.create(
            user = self.user,
            pk= 1,
            subject= 'Test Title',
            description= 'Test Description',
            priority= 'low',
        )
        self.url = reverse('update_ticket', kwargs={'pk': self.ticket.pk})
        self.data = {
            'subject': 'Test Title',
            'description': 'New Test Description',
            'priority': 'low',
        }
    
    def test_update_ticket_as_non_owner(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.pk).subject, 'Test Title')
        self.assertEqual(Ticket.objects.get(pk=self.ticket.pk).description, 'Test Description')
        self.assertEqual(Ticket.objects.get(pk=self.ticket.pk).priority, 'low')

    def test_update_ticket_as_owner(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.get(pk=self.ticket.pk).subject, 'Test Title')
        self.assertEqual(Ticket.objects.get(pk=self.ticket.pk).description, 'New Test Description')
        self.assertEqual(Ticket.objects.get(pk=self.ticket.pk).priority, 'low')


class TicketDetailViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass',
        )
        self.user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@gmail.com',
            password='testpass',
        )
        self.ticket=Ticket.objects.create(
            user = self.user,
            pk= 1,
            subject= 'Test Title',
            description= 'Test Description',
            priority= 'low',
        )
        self.url = reverse('detail_ticket', kwargs={'pk': self.ticket.pk})
    
    def test_detail_ticket_as_owner(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_ticket_as_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_ticket_as_not_owner(self):
        self.client.force_login(self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TicketListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpass',
        )
        self.ticket=Ticket.objects.create(
            user = self.user,
            pk= 1,
            subject= 'Test Title',
            description= 'Test Description',
            priority= 'low',
        )
        self.ticket=Ticket.objects.create(
            user = self.user,
            pk= 2,
            subject= 'Test Title 2',
            description= 'Test Description 2',
            priority= 'low',
        )
        self.ticket=Ticket.objects.create(
            user = self.admin,
            pk= 3,
            subject= 'Test Title 3',
            description= 'Test Description 3',
            priority= 'low',
        )
        self.url = reverse('tickets_list')
    
    def test_ticket_list_as_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['tickets']), 2)
    
    def test_ticket_list_as_admin(self):
        self.client.force_login(self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['tickets']), 3)
        
    def test_ticket_list_not_login_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/accounts/login/?next=/tickets_list/')


class TicketFilterListViewTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpassword',
        )
        self.ticket1 = Ticket.objects.create(
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_IN_PROGRESS,
            description='Test description 1'
        )
        self.ticket2 = Ticket.objects.create(
            subject='Test ticket 2',
            user=self.user,
            status=Ticket.STATUS_RESOLVED,
            description='Test description 2'
        )
        self.ticket3 = Ticket.objects.create(
            subject='Test ticket 3', 
            user=self.user, 
            status=Ticket.STATUS_REJECTED,
            description='Test description 3'
        )
        self.ticket4 = Ticket.objects.create(
            subject='Test ticket 4', 
            user=self.user, 
            status=Ticket.STATUS_RESTORED,
            description='Test description 4'
        )
        self.url = reverse('filter_tickets_list')

    def test_filter_tickets_by_status_as_admin(self):
        self.client.force_login(user=self.admin)
        response = self.client.get(self.url, {'status': Ticket.STATUS_IN_PROGRESS})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['tickets']), 1)
        self.assertEqual(response.context['tickets'][0].status, Ticket.STATUS_IN_PROGRESS)

    def test_filter_tickets_by_status_as_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'status': Ticket.STATUS_IN_PROGRESS})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.context['tickets']), 1)
        self.assertEqual(response.context['tickets'][0].status, Ticket.STATUS_IN_PROGRESS)

    def test_filter_tickets_by_status_as_unauthenticated_user(self):
        response = self.client.get(self.url, {'status': Ticket.STATUS_IN_PROGRESS})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/accounts/login/?next=/tickets_list/filtered/%3Fstatus%3DIn%2Bprogress')

    def test_filter_tickets_by_invalid_status(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url, {'status': 'invalid_status'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
class TicketRejectViewTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpassword',
        )
        self.ticket1 = Ticket.objects.create(
            pk=1,
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_IN_PROGRESS,
            description='Test description 1'
        )
        self.ticket2 = Ticket.objects.create(
            pk=2,
            subject='Test ticket 2',
            user=self.user,
            status=Ticket.STATUS_REJECTED,
            description='Test description 2'
        )
        self.comment_data = {
            'text': 'Test comment'
        }
        self.url1 = reverse('ticket_reject', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('ticket_reject', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_non_admin_user(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_IN_PROGRESS)
    
    def test_admin_user_cannot_reject_ticket_if_not_comment_data(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_IN_PROGRESS)

    def test_admin_user_can_reject_ticket(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url1, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
        comment = Comment.objects.last()
        self.assertEqual(comment.text, self.comment_data['text'])
        self.assertEqual(comment.author, self.admin)
        self.assertEqual(comment.ticket, self.ticket1)

    def test_admin_user_cannot_reject_ticket_if_not_in_progress(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url2, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_REJECTED)


class TicketRestoreViewTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpassword',
        )
        self.user2 = CustomUser.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpassword',
        )
        self.ticket1 = Ticket.objects.create(
            pk = 1,
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_REJECTED,
            description='Test description 1'
        )
        self.ticket2 = Ticket.objects.create(
            pk = 2,
            subject='Test ticket 2',
            user=self.user,
            status=Ticket.STATUS_IN_PROGRESS,
            description='Test description 2'
        )
        self.url1 = reverse('ticket_restore', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('ticket_restore', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_authenticated_user_cannot_restore_other_user_ticket(self):
        self.client.force_login(user=self.user2)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
    
    def test_staff_user_cant_restore_any_ticket(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
    
    def test_authenticated_user_can_restore_own_ticket(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_RESTORED)
    
    def test_authenticated_user_cant_restore_own_ticket(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_IN_PROGRESS)


class TicketInProgressViewTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpassword',
        )
        self.ticket1 = Ticket.objects.create(
            pk=1,
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_RESTORED,
            description='Test description 1'
        )
        self.ticket2 = Ticket.objects.create(
            pk=2,
            subject='Test ticket 2',
            user=self.user,
            status=Ticket.STATUS_REJECTED,
            description='Test description 2'
        )
        self.url = reverse('detail_ticket', kwargs={'pk': self.ticket1.pk})
        self.url1 = reverse('ticket_in_progress', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('ticket_in_progress', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_non_admin_user(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_RESTORED)

    def test_admin_user_can_change_ticket_status_to_in_progress(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url1, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_IN_PROGRESS)

    def test_admin_user_cannot_change_ticket_status_to_in_progress_if_not_restored(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_REJECTED)


class TicketResolvedViewTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username='user',
            email='user@example.com',
            password='testpassword',
        )
        self.ticket1 = Ticket.objects.create(
            pk = 1,
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_REJECTED,
            description='Test description 1'
        )
        self.ticket2 = Ticket.objects.create(
            pk = 2,
            subject='Test ticket 2',
            user=self.user,
            status=Ticket.STATUS_IN_PROGRESS,
            description='Test description 2'
        )
        self.url = reverse('detail_ticket', kwargs={'pk': self.ticket1.pk})
        self.url1 = reverse('ticket_resolve', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('ticket_resolve', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_non_admin_user(self):
        self.client.force_login(user=self.user)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_IN_PROGRESS)

    def test_admin_user(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url2, HTTP_REFERER=self.url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_RESOLVED)

    def test_admin_user_cannot_resolve_not_in_progress_status(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
