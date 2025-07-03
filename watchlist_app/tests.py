from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from watchlist_app.models import StreamPlatform, WatchList
# Create your tests here.

class StreamPlatformCreateTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_stream_platform(self):
        url = reverse('platforms-list')
        data = {
            'name': 'Test Platform',
            'about': 'This is a test platform.',
            'website': 'http://testplatform.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['name'], 'Test Platform')

class StreamPlatformListTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    def test_list_stream_platforms(self):
        url = reverse('platforms-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # You can add more assertions here to check the content of the response
        # For example, if you expect certain platforms to be listed:
        # self.assertGreater(len(response.data), 0)  # Check if there are any platforms listed

class StreamPlatformDetailTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        platform_data = {
            'name': 'Test Platform',
            'about': 'This is a test platform.',
            'website': 'http://testplatform.com'
        }
        self.platform = StreamPlatform.objects.create(**platform_data)


    def test_get_stream_platform_detail(self):
        detail_url = reverse('platforms-detail', args=[self.platform.id])

        response = self.client.get(detail_url, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.platform.name)

class WatchListTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.platform = StreamPlatform.objects.create(
            name='Test Platform',
            about='This is a test platform.',
            website='http://testplatform.com'
        )
        self.watchlist = WatchList.objects.create(
            title='Test Watchlist',
            storyline='This is a test watchlist.',
            active=True,
            platform=self.platform
        )
        
    def test_create_watchlist(self):
        url = reverse('watch-list')
        data = {
            'title': 'Test Watchlist',
            'platform': self.platform.id,
            'storyline': 'This is a test watchlist.',
            'active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data['title'], 'Test Watchlist')
    
    def test_list_watchlists(self):
        url = reverse('watch-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Check if there are any watchlists listed
    
    def test_watchlist_detail(self):
        detail_url = reverse('watch-list-detail', args=[self.watchlist.id])
        response = self.client.get(detail_url, format='json')
        print(type(response.data.get('data')))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('data')['title'], self.watchlist.title)


class ReviewTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.platform = StreamPlatform.objects.create(
            name='Test Platform',
            about='This is a test platform.',
            website='http://testplatform.com'
        )
        self.watchlist = WatchList.objects.create(
            title='Test Watchlist',
            storyline='This is a test watchlist.',
            active=True,
            platform=self.platform
        )
    
    def test_create_review(self):
        url = reverse('review-list', args=[self.watchlist.id])
        data = {
            'rating': 5.0,
            'description': 'Great watchlist!',
            'watchlist': self.watchlist.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], 5.0)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_reviews(self):
        url = reverse('review-list', args=[self.watchlist.id])
        # Create a review first
        data = {    
            'rating': 5.0,
            'description': 'Great watchlist!',
            'watchlist': self.watchlist.id
        }
        self.client.post(url, data, format='json')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        
