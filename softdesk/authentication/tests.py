from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status

# Create your tests here.

User = get_user_model()


class UserSerializationTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', email='testuser@gmail.com',
                                                  password='testpassword')
        self.create_url = reverse('user-create')

    def test_create_user(self):
        data = {
            'username': 'foobar',
            'email': 'foobar@gmail.com',
            'password': 'somepassword'
        }
        response = self.client.post(self.create_url, data, format='json')
        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)
