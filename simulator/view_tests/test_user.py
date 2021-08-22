from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from simulator.factories import GameFactory, HouseguestFactory

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

    def test_home_no_games(self):

        user = User.objects.create_user('fakeuser', 'fake@mail.com', 'pass')

        self.client.force_login(user)

        response = self.client.get('/api/home')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['games'], [])
        self.assertEqual(response.data['username'], user.username)

    def test_home_with_games(self):

        u = User.objects.create_user('fakeuser', 'fakemail', 'pass')

        g_1 = GameFactory.create(user=u)
        hgs_1 = HouseguestFactory.create_batch(6, game=g_1)
        hgs_1[3].toggle_evicted(True)

        g_2 = GameFactory.create(user=u)
        hgs_2 = HouseguestFactory.create_batch(4, game=g_2)
        hgs_2[2].toggle_evicted(True)

        self.client.force_login(u)

        response = self.client.get('/api/home')

        games = response.data["games"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['games']), 2)
        self.assertEqual(games[0]["id"], g_1.id)
        self.assertEqual(games[0]["players_left"], 5)
        self.assertEqual(games[0]["total_players"], 6)
