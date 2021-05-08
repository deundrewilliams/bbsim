from django.test import TestCase, Client
from ..models import Houseguest
from ..factories import HouseguestFactory

class HouseguestViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_get_all_houseguests(self):

        hgs = []
        hgs.append(HouseguestFactory(name="Joe"))
        hgs.append(HouseguestFactory(name="Kamala"))
        hgs.append(HouseguestFactory(name="Doug"))
        hgs.append(HouseguestFactory(name="Jill"))
        hgs.append(HouseguestFactory(name="Nancy"))
        hgs.append(HouseguestFactory(name="Alex"))

        response = self.client.get('/api/houseguests/')

        self.assertEqual(response.status_code, 200)

        data = response.data

        self.assertEqual(data['response'], [x.serialize() for x in hgs])

