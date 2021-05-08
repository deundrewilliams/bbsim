from django.test import TestCase, Client
from ..models import Game
from ..factories import GameFactory, HouseguestFactory

class GameViewTest(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_get_game_valid(self):

        g = GameFactory.create()

        valid_id = g.id

        response = self.client.get(f'/api/game/{valid_id}')

        data = response.data

        self.assertEqual(data, g.serialize())

    def test_get_game_invalid(self):

        response = self.client.get(f'/api/game/3')

        self.assertEqual(response.status_code, 400)

    def test_create_game_valid(self):

        hg_objs = []
        hg_objs.append(HouseguestFactory(name="A"))
        hg_objs.append(HouseguestFactory(name="B"))
        hg_objs.append(HouseguestFactory(name="C"))
        hg_objs.append(HouseguestFactory(name="D"))
        hg_objs.append(HouseguestFactory(name="E"))
        hg_objs.append(HouseguestFactory(name="F"))

        ids = [x.id for x in hg_objs]

        response = self.client.post(f'/api/create-game', {"houseguests": ids})

        # print(response.data)

        rec_id = response.data['id']

        g = Game.objects.get(id=rec_id)

        self.assertEqual(list(g.players.all()), hg_objs)
