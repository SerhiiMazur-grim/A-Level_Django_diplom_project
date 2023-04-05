from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class CustomLoginViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login_dj')
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')

    def test_login_redirect_admin(self):
        self.user.is_staff = True
        self.user.save()

        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('tickets_list') + 'filtered/?status=In progress')

    def test_login_redirect_non_admin(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass'})
        self.assertRedirects(response, reverse('tickets_list'))
