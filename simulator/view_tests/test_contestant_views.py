from django.test import TestCase, Client
from ..models import Contestant
from ..factories import ContestantFactory

class ContestantViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_get_all_houseguests(self):

        cs = []
        cs.append(ContestantFactory(name="Joe"))
        cs.append(ContestantFactory(name="Kamala"))
        cs.append(ContestantFactory(name="Doug"))
        cs.append(ContestantFactory(name="Jill"))
        cs.append(ContestantFactory(name="Nancy"))
        cs.append(ContestantFactory(name="Alex"))

        response = self.client.get('/api/contestants/')

        self.assertEqual(response.status_code, 200)

        data = response.data

        self.assertEqual(data['response'], [x.serialize() for x in cs])

