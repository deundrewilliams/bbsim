from django.test import TestCase, Client
from ..models import Game
from ..factories import GameFactory, HouseguestFactory, ContestantFactory

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

        contestant_objs = []
        contestant_objs.append(ContestantFactory(name="A"))
        contestant_objs.append(ContestantFactory(name="B"))
        contestant_objs.append(ContestantFactory(name="C"))
        contestant_objs.append(ContestantFactory(name="D"))
        contestant_objs.append(ContestantFactory(name="E"))
        contestant_objs.append(ContestantFactory(name="F"))

        ids = [x.id for x in contestant_objs]

        response = self.client.post(f'/api/create-game', {"contestants": ids})

        rec_id = response.data['id']

        g = Game.objects.get(id=rec_id)

        # Check that created houseguests have the same names as the contestants
        for i in range(len(list(g.players.all()))):
            self.assertEqual(list(g.players.all())[i].name, contestant_objs[i].name)

    def test_sim_game(self):

        g = GameFactory()

        hg_objs = []
        hg_objs.append(HouseguestFactory(name="A", game=g))
        hg_objs.append(HouseguestFactory(name="B", game=g))
        hg_objs.append(HouseguestFactory(name="C", game=g))
        hg_objs.append(HouseguestFactory(name="D", game=g))
        hg_objs.append(HouseguestFactory(name="E", game=g))
        hg_objs.append(HouseguestFactory(name="F", game=g))

        response = self.client.post(f'/api/sim-game', {"id": g.id})

        self.assertTrue('winner' in response.data)
