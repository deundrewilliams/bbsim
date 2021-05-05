import pytest

from ..models import *
from ..factories import HouseguestFactory, GameFactory



class TestGame:

    @pytest.mark.django_db
    def test_initialization(self):

        hgs = HouseguestFactory.create_batch(12)

        g = Game()
        g.save()
        g.players.set(hgs)

        data = g.serialize()

        assert data['id'] == g.id
        assert data['Players'] == [x.serialize() for x in hgs]
        assert data['Weeks'] == []
        assert data['Winner'] == None
        assert data['Prejury'] == []
        assert data['Jury'] == []

    @pytest.mark.django_db
    def test_determine_jury_size(self):

        hgs = HouseguestFactory.create_batch(2)

        g = GameFactory.create(players=hgs)

        assert g.determine_jury_size(5) == 3
        assert g.determine_jury_size(12) == 5
        assert g.determine_jury_size(16) == 9
        assert g.determine_jury_size(13) == 7

    @pytest.mark.django_db
    def test_run_hoh_competition(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        small_game.in_house = hgs
        small_game.current_hoh = None
        small_game.save()

        def mock_run_competition(obj):
            assert list(obj.participants.all()) == hgs
            obj.winner = hgs[1]

        monkeypatch.setattr(Competition, "run_competition", mock_run_competition)

        small_game.run_hoh_competition(None)

        assert small_game.current_hoh == hgs[1]
        assert hgs[1].competition_count == 1

    @pytest.mark.django_db
    def test_run_nomination_ceremony(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        # HOH: 2, Noms: 1, 3
        small_game.in_house = hgs
        small_game.current_hoh = hgs[2]
        small_game.save()

        def mock_run_ceremony(obj):
            assert obj.hoh == hgs[2]
            assert list(obj.participants.all()) == hgs
            obj.nominees.set([hgs[1], hgs[3]])

        monkeypatch.setattr(NominationCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_nomination_ceremony()

        assert set(small_game.current_nominees) == set([hgs[1], hgs[3]])
        assert small_game.current_nominees[0].nomination_count == 1
        assert small_game.current_nominees[1].nomination_count == 1

    @pytest.mark.django_db
    def test_get_veto_players(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        # HOH: 2, Noms: 1, 3
        small_game.in_house = hgs
        small_game.current_hoh = hgs[2]
        small_game.current_nominees = [hgs[1], hgs[3]]
        small_game.save()

        picked_players = small_game.get_veto_players()

        assert set(picked_players) == set(hgs)

    @pytest.mark.django_db
    def test_run_veto_competition(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4
        hgs = list(small_game.players.all())
        small_game.in_house = hgs
        small_game.current_hoh = hgs[2]
        small_game.current_nominees = [hgs[1], hgs[3]]
        small_game.save()

        def mock_run_competition(obj):
            assert list(obj.participants.all()) == hgs
            obj.winner = hgs[4]

        monkeypatch.setattr(Competition, "run_competition", mock_run_competition)

        small_game.run_veto_competition(hgs)

        assert small_game.pov_holder == hgs[4]
        assert hgs[4].competition_count == 1

    @pytest.mark.django_db
    def test_run_veto_ceremony(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5
        hgs = list(small_game.players.all())

        small_game.in_house = hgs
        small_game.current_hoh = hgs[2]
        small_game.current_nominees = [hgs[1], hgs[3]]
        small_game.pov_holder = hgs[4]
        small_game.save()

        def mock_run_ceremony(obj):
            assert obj.hoh == hgs[2]
            obj.nominees.set([hgs[3], hgs[5]])

        monkeypatch.setattr(VetoCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_veto_ceremony()

        assert set(small_game.current_nominees) == set([hgs[3], hgs[5]])

    @pytest.mark.django_db
    def test_run_eviction(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5, 5 evicted
        hgs = list(small_game.players.all())

        small_game.in_house = hgs
        small_game.current_hoh = hgs[2]
        small_game.current_nominees = [hgs[3], hgs[5]]
        small_game.save()

        def mock_run_ceremony(obj):
            assert list(obj.nominees.all()) == [hgs[3], hgs[5]]
            assert obj.hoh == hgs[2]
            obj.evicted = hgs[5]

        monkeypatch.setattr(EvictionCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_eviction()

        assert small_game.evicted == hgs[5]

    @pytest.mark.django_db
    def test_run_week_at_jury(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5, 5 evicted
        hgs = list(small_game.players.all())

        small_game.in_house = hgs
        small_game.jury_began = False
        small_game.current_hoh = None
        small_game.jury_size = 4 # wouldn't actually be 4, but tests the first cpl lines of code

        def mock_run_hoh_competition(obj, outgoing_hoh):
            assert obj.jury_began # Once here, jury began should've been changed to True

            assert outgoing_hoh == None
            obj.current_hoh = hgs[2]
            hgs[2].win_competition()

        def mock_run_nomination_ceremony(obj):
            obj.current_nominees = [hgs[1], hgs[3]]

        def mock_get_veto_players(obj):
            return hgs

        def mock_run_veto_competition(obj):
            obj.pov_holder = hgs[4]
            hgs[4].win_competition()

        def mock_run_veto_cerermony(obj):
            obj.current_nominees = [hgs[3], hgs[5]]

        def mock_run_eviction(obj):
            obj.evicted = hgs[5]


        monkeypatch.setattr(Game, "run_hoh_competition", mock_run_hoh_competition)
        monkeypatch.setattr(Game, "run_nomination_ceremony", mock_run_nomination_ceremony)
        monkeypatch.setattr(Game, "get_veto_players", mock_get_veto_players)
        monkeypatch.setattr(Game, "run_veto_ceremony", mock_run_veto_cerermony)
        monkeypatch.setattr(Game, "run_veto_competition", mock_run_veto_competition)
        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        received_week = small_game.run_week(1)
        assert received_week.number == 1
        assert received_week.hoh == hgs[2]
        assert list(received_week.initial_nominees.all()) == [hgs[1], hgs[3]]
        assert received_week.pov == hgs[4]
        assert list(received_week.final_nominees.all()) == [hgs[3], hgs[5]]
        assert received_week.evicted == hgs[5]
