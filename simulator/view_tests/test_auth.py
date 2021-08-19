from django.test import TestCase, Client
from django.contrib.auth.models import User

class ContestantViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_login(self):

        user = User.objects.create_user('user', 'mail@me.com', 'pass')

        response = self.client.post('/login/', {'username': 'user', 'password': 'pass'})

        self.assertTrue(response.data['success'])
        self.assertTrue(user.is_authenticated)

    def test_signup(self):

        response = self.client.post('/signup/', {'username': 'testuser', 'password': 'testpass', 'email': 'testemail'})

        self.assertTrue(response.data['success'])

    def test_invalid_signup(self):

        response = self.client.post('/signup/', {'username': 'testuser', 'password': 'testpass'})

        self.assertFalse(response.data['success'])
