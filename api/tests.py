from rest_framework.test import (
    APITestCase,
    APIClient,
)
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse

from users.models import CustomUser
from ticket.models import Ticket
from ticket.serializer import TicketSerializer
from comments.models import Comment


class UserCreateTests(APITestCase):
    def setUp(self):
        self.data = {
            'username': 'test_api_user',
            'email': 'test_api_user@gmail.com',
            'first_name': 'test_api',
            'last_name': 'test_api',
            'password': '791357so',
        }
        self.data2 = {
            'username': 'test_api_user',
            'email': 'test_api_usergmail.com',
            'first_name': 'test_api',
            'last_name': 'test_api',
            'password': '791357so',
        }
        self.url = reverse('api_create_user')
        
    def test_create_user_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'test_api_user')
    
    def test_create_user_with_same_data(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().username, 'test_api_user')
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_user_failure(self):
        response = self.client.post(self.url, self.data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )

        self.url = reverse('api_login')
        self.data = {
            'username': 'testuser',
            'password': 'testpass'
        }
        self.data2 = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
    def test_login_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('auth_token', response.data)
    
    def test_login_failure(self):
        response = self.client.post(self.url, self.data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email= 'test_api_user@gmail.com',
            first_name= 'test_api',
            last_name= 'test_api',
            password='testpass',
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.url = reverse('api_logout')

    def test_user_logout(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TicketCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.url = reverse('api_create_ticket')
        self.data = {
            'subject': 'Test Ticket',
            'description': 'This is a test ticket.',
            'priority': Ticket.PRIORITY_HIGH,
        }
        self.bad_data = {
            'description': 'This is a test ticket.',
            'priority': Ticket.PRIORITY_HIGH,
        }
    
    def test_create_ticket_with_bad_data(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.bad_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_ticket_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['subject'], self.data['subject'])
        self.assertEqual(response.data['description'], self.data['description'])
        self.assertEqual(response.data['priority'], self.data['priority'])
        self.assertEqual(response.data['user'], self.user.pk)
        
        ticket = Ticket.objects.get(pk=response.data['id'])
        self.assertEqual(ticket.subject, self.data['subject'])
        self.assertEqual(ticket.description, self.data['description'])
        self.assertEqual(ticket.priority, self.data['priority'])
        self.assertEqual(ticket.user, self.user)
    
    def test_create_ticket_unauthenticated_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TicketDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass',
        )
        self.user2 = CustomUser.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpass',
        )
        self.ticket = Ticket.objects.create(
            user=self.user,
            subject='Test Ticket',
            description='This is a test ticket',
            priority= Ticket.PRIORITY_HIGH,
        )
        self.url = reverse('api_detail_ticket', kwargs={'pk': self.ticket.pk})
        self.bad_url = reverse('api_detail_ticket', kwargs={'pk': 666})
    
    def test_get_non_existent_ticket_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.bad_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_ticket_detail_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_ticket_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('subject'), 'Test Ticket')
        self.assertEqual(response.data.get('description'), 'This is a test ticket')
    
    def test_get_ticket_detail_by_not_owner(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TicketUpdateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email= 'test_api_user@gmail.com',
            first_name= 'test_api',
            last_name= 'test_api',
            password='testpass',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.ticket = Ticket.objects.create(
            subject='Test Ticket',
            description='Test Description',
            user=self.user,
            priority= Ticket.PRIORITY_HIGH,
        )

    def test_ticket_update_by_owner(self):
        url = reverse('api_update_ticket', kwargs={'pk': self.ticket.pk})
        data = {'subject': 'Updated Ticket', 'description': 'Updated Description'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.subject, 'Updated Ticket')
        self.assertEqual(self.ticket.description, 'Updated Description')

    def test_ticket_update_by_non_owner(self):
        user2 = CustomUser.objects.create_user(
            username='testuser2',
            email= 'test_api_user2@gmail.com',
            first_name= 'test_api2',
            last_name= 'test_api2',
            password='testpass',
        )
        self.client.force_authenticate(user=user2)
        url = reverse('api_update_ticket', kwargs={'pk': self.ticket.pk})
        data = {'subject': 'Updated Ticket', 'description': 'Updated Description'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.subject, 'Test Ticket')
        self.assertEqual(self.ticket.description, 'Test Description')

    def test_ticket_update_non_existent_ticket(self):
        url = reverse('api_update_ticket', kwargs={'pk': 100})
        data = {'subject': 'Updated Ticket', 'description': 'Updated Description'}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserTicketsListAPIViewTest(APITestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass',
            is_staff=True,
        )
        self.ticket_1 = Ticket.objects.create(
            user=self.user,
            subject='Ticket 1',
            description='Description 1',
            priority= Ticket.PRIORITY_HIGH,
        )
        self.ticket_2 = Ticket.objects.create(
            user=self.user,
            subject='Ticket 2',
            description='Description 2',
            priority= Ticket.PRIORITY_HIGH,
        )
        self.ticket_3 = Ticket.objects.create(
            user=self.admin,
            subject='Ticket 3',
            description='Description 3',
            priority= Ticket.PRIORITY_HIGH,
        )

    def test_authenticated_user_can_view_own_tickets(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('api_ticket_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['subject'], 'Ticket 2')
        self.assertEqual(response.data[1]['subject'], 'Ticket 1')

    def test_admin_can_view_all_tickets(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('api_ticket_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['subject'], 'Ticket 3')
        self.assertEqual(response.data[1]['subject'], 'Ticket 2')
        self.assertEqual(response.data[2]['subject'], 'Ticket 1')

    def test_unauthenticated_user_cannot_view_tickets(self):
        url = reverse('api_ticket_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserFilterTicketsListAPIViewTestCase(APITestCase):

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
        self.url = reverse('api_filter_ticket_list')

    def test_filter_tickets_by_status_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url, {'status': Ticket.STATUS_IN_PROGRESS})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TicketSerializer(Ticket.objects.filter(status=Ticket.STATUS_IN_PROGRESS), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_filter_tickets_by_status_as_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'status': Ticket.STATUS_IN_PROGRESS})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TicketSerializer(Ticket.objects.filter(user=self.user, status=Ticket.STATUS_IN_PROGRESS), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_filter_tickets_by_status_as_unauthenticated_user(self):
        response = self.client.get(self.url, {'status': Ticket.STATUS_IN_PROGRESS})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_tickets_by_invalid_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {'status': 'invalid_status'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TicketRestoreAPIViewTestCase(APITestCase):
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
        self.url1 = reverse('api_ticket_restored', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('api_ticket_restored', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_cannot_restore_other_user_ticket(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
    
    def test_staff_user_cant_restore_any_ticket(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
    
    def test_authenticated_user_can_restore_own_ticket(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_RESTORED)
    
    def test_authenticated_user_cant_restore_own_ticket(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_IN_PROGRESS)


class TicketResolveAPIViewTestCase(APITestCase):
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
        self.url1 = reverse('api_ticket_resolved', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('api_ticket_resolved', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_IN_PROGRESS)

    def test_admin_user(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_RESOLVED)

    def test_admin_user_cannot_resolve_not_in_progress_status(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)


class TicketInProgressAPIViewTestCase(APITestCase):
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
        self.url1 = reverse('api_ticket_in_progress', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('api_ticket_in_progress', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_RESTORED)

    def test_admin_user_can_change_ticket_status_to_in_progress(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_IN_PROGRESS)

    def test_admin_user_cannot_change_ticket_status_to_in_progress_if_not_restored(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_REJECTED)


class TicketRejectAPIViewTestCase(APITestCase):
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
        self.url1 = reverse('api_ticket_rejected', kwargs={'pk': self.ticket1.pk})
        self.url2 = reverse('api_ticket_rejected', kwargs={'pk': self.ticket2.pk})

    def test_unauthenticated_user(self):
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_IN_PROGRESS)
    
    def test_admin_user_cannot_reject_ticket_if_not_comment_data(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_IN_PROGRESS)

    def test_admin_user_can_reject_ticket(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url1, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ticket1.refresh_from_db()
        self.assertEqual(self.ticket1.status, Ticket.STATUS_REJECTED)
        comment = Comment.objects.last()
        self.assertEqual(comment.text, self.comment_data['text'])
        self.assertEqual(comment.author, self.admin)
        self.assertEqual(comment.ticket, self.ticket1)

    def test_admin_user_cannot_reject_ticket_if_not_in_progress(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url2, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.ticket2.refresh_from_db()
        self.assertEqual(self.ticket2.status, Ticket.STATUS_REJECTED)


class CommentListAPIViewTestCase(APITestCase):
    def setUp(self):
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
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.ticket = Ticket.objects.create(
            pk=1,
            subject='Test ticket 1',
            user=self.user,
            status=Ticket.STATUS_IN_PROGRESS,
            description='Test description 1'
        )
        self.comment1 = Comment.objects.create(
            author=self.user,
            ticket=self.ticket,
            text='Test comment 1'
        )
        self.comment2 = Comment.objects.create(
            author=self.admin,
            ticket=self.ticket,
            text='Test comment 2'
        )
        self.url = reverse('api_comment_list', kwargs={'pk': self.ticket.pk})

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_user_can_see_their_own_comments(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'], 'Test comment 2')
        self.assertEqual(response.data[1]['text'], 'Test comment 1')

    def test_admin_user_can_see_all_comments(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['text'], 'Test comment 2')
        self.assertEqual(response.data[1]['text'], 'Test comment 1')
    
    def test_non_admin_user_cant_see_comments_not_own_ticket(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentCreateAPIViewTestCase(APITestCase):
    def setUp(self):
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
        self.admin = CustomUser.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpassword',
            is_staff=True
        )
        self.ticket = Ticket.objects.create(
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
        self.url = reverse('api_create_comment', kwargs={'pk': self.ticket.pk})
        self.url2 = reverse('api_create_comment', kwargs={'pk': self.ticket2.pk})
        self.data = {'text': 'Test comment'}

    def test_unauthenticated_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_non_admin_user_can_create_comment_on_own_ticket(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Test comment')
        
    def test_non_admin_user_cant_create_comment_on_other_ticket(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Comment.objects.filter(text='Test comment').exists())
        
    def test_user_cant_create_comment_for_non_in_progress_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url2, self.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Comment.objects.filter(text='Test comment').exists())
        
    def test_admin_user_can_create_comment_on_any_ticket(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'Test comment')
