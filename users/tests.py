from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse

from .models import CustomUser
from comments.models import Comment
from ticket.models import Ticket


class CustomUserCreateViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('registration_dj')

        self.data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'first_name': 'test_user_f_name',
            'last_name': 'test_user_l_name',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        self.invalid_data = {
            'username': 'testuser',
            'email': 'testuserexample.com',
            'first_name': 'test_user_f_name',
            'last_name': 'test_user_l_name',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
    def test_register_user(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(CustomUser.objects.filter(username=self.data['username']).exists())
        self.assertEqual(len(CustomUser.objects.all()), 1)
    
    def test_register_2_users_with_same_data(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(CustomUser.objects.all()), 1)
    
    def test_register_user_without_data(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(CustomUser.objects.all()), 0)
    
    def test_register_user_with_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(CustomUser.objects.all()), 0)


class CustomLoginViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'testuser',
            email = 'testuser@example.com',
            password = 'testpass'
        )
        self.admin = CustomUser.objects.create_user(
            username = 'adminuser',
            email = 'adminuser@example.com',
            password = 'testpass',
            is_staff = True
        )
        self.url = reverse('login_dj')

    def test_login_admin(self):
        response = self.client.post(self.url, {'username': 'adminuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, '/tickets_list/filtered/?status=In+progress')

    def test_login_regular_user(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, reverse('tickets_list'))


class CustomLogoutViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username = 'testuser',
            email = 'testuser@example.com',
            password = 'testpass'
        )
        self.logout_url = reverse('logout_dj')
        self.login_url = reverse('login_dj')

    def test_logout_view(self):
        self.client.force_login(self.user)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        session = self.client.session
        self.assertIsNone(session.get('_auth_user_id'))
        self.assertRedirects(response, self.login_url, fetch_redirect_response=False)
