from django.test import TestCase, Client
from ..models import Game
from ..factories import GameFactory, HouseguestFactory, ContestantFactory
from django.contrib.auth.models import User


class GameViewTest(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = Client()

    def test_get_game_valid(self):

        g = GameFactory.create()

        valid_id = g.id

        response = self.client.get(f"/api/game/{valid_id}")

        data = response.data

        self.assertEqual(data, g.serialize())

    def test_get_game_invalid(self):

        response = self.client.get("/api/game/3")

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

        u = User.objects.create_user(username="test", password="test")
        self.client.force_login(u)

        response = self.client.post("/api/create-game", {"contestants": ids})

        rec_id = response.data["id"]

        g = Game.objects.get(id=rec_id)

        # Check that created houseguests have the same names as the contestants
        for i in range(len(list(g.players.all()))):
            self.assertEqual(list(g.players.all())[i].name, contestant_objs[i].name)

    def test_create_game_with_custom_hgs(self):

        contestant_objs = ContestantFactory.create_batch(6)

        ids = [x.id for x in contestant_objs]

        custom_names = ["Joe", "Kamala", "Doug", "Jill"]

        u = User.objects.create_user(username="test", password="test")
        self.client.force_login(u)

        response = self.client.post("/api/create-game", {"contestants": ids, "houseguests": custom_names})

        print(response.data)

        rec_id = response.data["id"]

        g = Game.objects.get(id=rec_id)

        # Check that created houseguests have the same names as the contestants
        all_names = [x.name for x in contestant_objs] + custom_names

        self.assertEqual([x.name for x in g.players.all()], all_names)


    def test_sim_game(self):

        g = GameFactory()

        hg_objs = []
        hg_objs.append(HouseguestFactory(name="A", game=g))
        hg_objs.append(HouseguestFactory(name="B", game=g))
        hg_objs.append(HouseguestFactory(name="C", game=g))
        hg_objs.append(HouseguestFactory(name="D", game=g))
        hg_objs.append(HouseguestFactory(name="E", game=g))
        hg_objs.append(HouseguestFactory(name="F", game=g))

        response = self.client.post("/api/simulate", {"id": g.id})

        self.assertEqual(len(response.data['players']), 6)
