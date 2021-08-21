from django.test import TestCase, Client
from django.contrib.auth.models import User, Group

class ContestantViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()
        Group.objects.create(name='Simulator User')

    def test_login(self):

        user = User.objects.create_user('user', 'mail@me.com', 'pass')

        response = self.client.post('/api/login', {'username': 'user', 'password': 'pass'})

        self.assertTrue(response.data['success'])
        self.assertTrue(user.is_authenticated)

    def test_login_invalid_password(self):

        user = User.objects.create_user('user', 'mail@me.com', 'pass')

        response = self.client.post('/api/login', {'username': 'user', 'password': 'wrong'})

        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['error'], 'Invalid Username/Password combination')

    def test_signup(self):

        response = self.client.post('/api/signup', {'username': 'testuser', 'password': 'testpass', 'email': 'testemail'})

        self.assertTrue(response.data['success'])


