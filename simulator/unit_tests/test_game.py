import pytest

from ..classes import (
    Competition,
    NominationCeremony,
    VetoCeremony,
    EvictionCeremony,
    Finale,
    Week,
)
from ..models import (
    Game,
    Houseguest,
)
from ..factories import HouseguestFactory, GameFactory


class TestGame:
    @pytest.mark.django_db
    def test_initialization(self):

        # hgs = HouseguestFactory.create_batch(12)

        g = Game()
        g.save()

        hgs = HouseguestFactory.create_batch(12, game=g)

        data = g.serialize()

        assert data["id"] == g.id
        assert data["completed"] is False
        assert data["current_step"] == "Memory Wall"

    @pytest.mark.django_db
    def test_determine_jury_size(self):

        g = GameFactory.create()

        _ = HouseguestFactory.create_batch(2, game=g)

        assert g.determine_jury_size(5) == 3
        assert g.determine_jury_size(12) == 5
        assert g.determine_jury_size(16) == 9
        assert g.determine_jury_size(13) == 7

    @pytest.mark.django_db
    def test_setup_game(self):

        g = GameFactory.create()

        hgs = HouseguestFactory.create_batch(6, game=g)

        g.setup_game()

        assert g.jury_size == 3

    @pytest.mark.django_db
    def test_advance_from_setup_to_hoh(self):

        g = GameFactory.create()
        hgs = HouseguestFactory.create_batch(6, game=g)
        g.setup_game()

        data = g.advance_step()

        assert data['players'] == [x.serialize() for x in hgs]
        assert g.step == Game.HOH

    @pytest.mark.django_db
    def test_advance_from_hoh_to_noms(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        def mock_run_hoh_competition(obj, outgoing):
            assert outgoing == None
            obj.hoh = hgs[0]

        monkeypatch.setattr(Game, "run_hoh_competition", mock_run_hoh_competition)

        small_game.step = Game.HOH
        small_game.save()

        data = small_game.advance_step()

        assert data['hoh'] == hgs[0].serialize()
        assert small_game.step == Game.NOM

    @pytest.mark.django_db
    def test_advance_from_noms_to_pov(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        small_game.hoh = hgs[0]
        small_game.step = Game.NOM
        small_game.save()

        def mock_run_nom_ceremony(obj):
            obj.nominees.set([hgs[1], hgs[2]])

        monkeypatch.setattr(Game, "run_nomination_ceremony", mock_run_nom_ceremony)

        data = small_game.advance_step()

        assert data['nominees'] == [x.serialize() for x in [hgs[1], hgs[2]]]
        assert small_game.step == Game.POV

    @pytest.mark.django_db
    def test_advance_from_pov_to_veto_ceremony(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        def mock_run_veto_competition(obj, players):
            assert len(players) == 6
            obj.pov = hgs[5]
            print(obj.pov)

        small_game.hoh = hgs[0]
        small_game.nominees.set([hgs[1], hgs[2]])
        small_game.step = Game.POV
        small_game.save()

        monkeypatch.setattr(Game, "run_veto_competition", mock_run_veto_competition)

        data = small_game.advance_step()

        assert data['pov'] == hgs[5].serialize()
        assert small_game.step == Game.VETO_CEREMONY

    @pytest.mark.django_db
    def test_advance_from_veto_ceremony_to_eviction(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        small_game.hoh = hgs[0]
        small_game.nominees.set([hgs[1], hgs[2]])
        small_game.pov = hgs[2]
        small_game.step = Game.VETO_CEREMONY
        small_game.save()

        def mock_run_veto_ceremony(obj):
            obj.nominees.set([hgs[1], hgs[3]])
            return {
                "Decision": {"Using": True, "On": hgs[2]},
                "Final Nominees": [x.serialize() for x in [hgs[1], hgs[3]]]
            }

        monkeypatch.setattr(Game, "run_veto_ceremony", mock_run_veto_ceremony)

        data = small_game.advance_step()

        expected_data = {
            "Decision": {"Using": True, "On": hgs[2]},
            "Final Nominees": [x.serialize() for x in [hgs[1], hgs[3]]]
        }

        assert data['results'] == expected_data
        assert small_game.step == Game.EVICTION

    @pytest.mark.django_db
    def test_advance_from_eviction_to_memory_wall(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        def mock_run_eviction(obj):
            return {
                "HOH": hgs[0].serialize(),
                "Nominees": [x.serialize() for x in [hgs[1], hgs[2]]],
                "Evicted": hgs[2].serialize(),
                "Votes": [2, 1],
                 "Tied": False,
            }

        small_game.hoh = hgs[0]
        small_game.nominees.set([hgs[1], hgs[2]])
        small_game.step = Game.EVICTION
        small_game.save()

        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        data = small_game.advance_step()

        expected_data = {
            "HOH": hgs[0].serialize(),
            "Nominees": [x.serialize() for x in [hgs[1], hgs[2]]],
            "Evicted": hgs[2].serialize(),
            "Votes": [2, 1],
            "Tied": False,
        }

        assert data['results'] == expected_data
        assert small_game.step == Game.MEMORYWALL


    @pytest.mark.django_db
    def test_advance_from_eviction_to_finale(self, monkeypatch):

        g = GameFactory.create()

        hgs = HouseguestFactory.create_batch(4, game=g)

        def mock_run_eviction(obj):

            hgs[2].toggle_evicted(True)

            return {
                "HOH": hgs[0].serialize(),
                "Nominees": [x.serialize() for x in [hgs[1], hgs[2]]],
                "Evicted": hgs[2].serialize(),
                "Votes": [1, 0],
                 "Tied": False,
            }

        g.hoh = hgs[0]
        g.nominees.set([hgs[1], hgs[2]])
        g.step = Game.EVICTION
        g.save()

        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        data = g.advance_step()

        expected_data = {
            "HOH": hgs[0].serialize(),
            "Nominees": [x.serialize() for x in [hgs[1], hgs[2]]],
            "Evicted": hgs[2].serialize(),
            "Votes": [1, 0],
            "Tied": False,
        }

        assert data['results'] == expected_data
        assert g.step == Game.FINALE

    @pytest.mark.django_db
    def test_advance_from_finale(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        for hg in hgs[:3]:
            hg.toggle_evicted(True)

        small_game.jury.set(hgs[:3])
        small_game.step = Game.FINALE

        def mock_run_finale(obj):

            obj.winner = hgs[5]

            return { "mock": "data" }

        monkeypatch.setattr(Game, "run_finale", mock_run_finale)

        data = small_game.advance_step()

        assert data['results'] == { "mock": "data"}
        assert small_game.winner == hgs[5]
        assert small_game.completed == True

    @pytest.mark.django_db
    def test_run_hoh_competition(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        small_game.in_house = hgs
        small_game.current_hoh = None
        small_game.save()

        def mock_run_competition(obj):
            assert obj.participants == hgs
            obj.winner = hgs[1]

        monkeypatch.setattr(Competition, "run_competition", mock_run_competition)

        small_game.run_hoh_competition(None)

        assert small_game.hoh == hgs[1]
        assert hgs[1].competition_count == 1

    @pytest.mark.django_db
    def test_run_nomination_ceremony(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        # HOH: 2, Noms: 1, 3
        small_game.hoh = hgs[2]
        small_game.save()

        def mock_run_ceremony(obj):
            assert obj.hoh == hgs[2]
            assert obj.participants == hgs
            obj.nominees = [hgs[1], hgs[3]]

        monkeypatch.setattr(NominationCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_nomination_ceremony()

        assert set(small_game.nominees.all()) == set([hgs[1], hgs[3]])
        assert list(small_game.nominees.all())[0].nomination_count == 1
        assert list(small_game.nominees.all())[1].nomination_count == 1

    @pytest.mark.django_db
    def test_get_veto_players(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        # HOH: 2, Noms: 1, 3
        small_game.hoh = hgs[2]
        small_game.nominees.set([hgs[1], hgs[3]])
        small_game.save()

        picked_players = small_game.get_veto_players()

        assert set(picked_players) == set(hgs)

    @pytest.mark.django_db
    def test_run_veto_competition(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4
        hgs = list(small_game.players.all())
        small_game.hoh = hgs[2]
        small_game.nominees.set([hgs[1], hgs[3]])
        small_game.save()

        def mock_run_competition(obj):
            assert obj.participants == hgs
            obj.winner = hgs[4]

        monkeypatch.setattr(Competition, "run_competition", mock_run_competition)

        small_game.run_veto_competition(hgs)

        assert small_game.pov == hgs[4]
        assert hgs[4].competition_count == 1

    @pytest.mark.django_db
    def test_run_veto_ceremony(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5
        hgs = list(small_game.players.all())

        small_game.hoh = hgs[2]
        small_game.nominees.set([hgs[1], hgs[3]])
        small_game.pov = hgs[4]
        small_game.save()

        def mock_run_ceremony(obj):
            assert obj.hoh == hgs[2]
            obj.nominees = [hgs[3], hgs[5]]

        monkeypatch.setattr(VetoCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_veto_ceremony()

        assert set(small_game.nominees.all()) == set([hgs[3], hgs[5]])

    @pytest.mark.django_db
    def test_run_eviction(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5, 5 evicted
        hgs = list(small_game.players.all())

        for hg in hgs:
            hg.initialize_relationships(hgs)

        small_game.hoh = hgs[2]
        small_game.nominees.set([hgs[3], hgs[5]])
        small_game.save()

        def mock_run_ceremony(obj):
            assert obj.nominees == [hgs[3], hgs[5]]
            assert obj.hoh == hgs[2]
            obj.evicted = hgs[5]
            obj.vote_count = [2, 1]
            obj.tied = False

        monkeypatch.setattr(EvictionCeremony, "run_ceremony", mock_run_ceremony)

        data = small_game.run_eviction()

        assert data['Evicted'] == hgs[5].serialize()
        assert data['Votes'] == [2, 1]
        assert data['Tied'] is False

    @pytest.mark.django_db
    def test_run_finale(self, small_game, monkeypatch):

        hgs = list(small_game.players.all()).copy()

        jury = hgs[:3]
        finalists = hgs[3:]

        small_game.in_house = finalists
        small_game.jury.set(jury)

        def mock_run_finale(obj):
            obj.winner = hgs[5]
            obj.final_juror = hgs[3]

        monkeypatch.setattr(Finale, "run_finale", mock_run_finale)

        small_game.run_finale()

        assert small_game.winner == hgs[5]
