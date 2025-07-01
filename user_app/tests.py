from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

# Create your tests here.
class RegisterUserTestCase(APITestCase):
    def test_register_user(self):
        url = reverse('register_user')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'password2': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

class LoginUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
    def test_login_user(self):
        url = reverse('api_token_auth')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class LogoutUserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
    
    def test_logout_user(self):
        # First, log in to get the token
        login_url = reverse('api_token_auth')
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_response = self.client.post(login_url, login_data, format='json')
        token = login_response.data['token']
        
        # Now, log out using the token
        logout_url = reverse('logout_user')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(logout_url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)