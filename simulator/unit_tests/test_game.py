import pytest

from ..classes import (
    Competition,
    NominationCeremony,
    VetoCeremony,
    EvictionCeremony,
    Finale,
)
from ..models import (
    Game,
    Houseguest,
    Week,
    Contestant
)
from ..factories import HouseguestFactory, GameFactory, WeekFactory, ContestantFactory, UserFactory


class TestGame:
    @pytest.mark.django_db
    def test_initialization(self):

        # hgs = HouseguestFactory.create_batch(12)

        g = Game(user=UserFactory.create())
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
        assert len(g.weeks.all()) == 1

    @pytest.mark.django_db
    def test_advance_from_hoh_to_noms(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        def mock_run_hoh_competition(obj, outgoing):
            assert outgoing == None
            obj.hoh = hgs[0]

        monkeypatch.setattr(Game, "run_hoh_competition", mock_run_hoh_competition)

        small_game.step = Game.HOH
        small_game.save()

        week = WeekFactory(number=1)
        week.save()
        small_game.weeks.add(week)

        data = small_game.advance_step()

        assert data['hoh'] == hgs[0].serialize()
        assert small_game.step == Game.NOM
        assert small_game.weeks.all()[0].hoh == hgs[0]

    @pytest.mark.django_db
    def test_advance_from_noms_to_pov(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        small_game.hoh = hgs[0]
        small_game.step = Game.NOM
        small_game.save()

        week = WeekFactory(number=1)
        week.save()
        small_game.weeks.add(week)

        def mock_run_nom_ceremony(obj):
            obj.nominees.set([hgs[1], hgs[2]])

        monkeypatch.setattr(Game, "run_nomination_ceremony", mock_run_nom_ceremony)

        data = small_game.advance_step()

        assert data['nominees'] == [x.serialize() for x in [hgs[1], hgs[2]]]
        assert small_game.step == Game.POV
        assert list(small_game.weeks.all()[0].initial_nominees.all()) == [hgs[1], hgs[2]]

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

        week = WeekFactory(number=1)
        week.save()
        small_game.weeks.add(week)

        monkeypatch.setattr(Game, "run_veto_competition", mock_run_veto_competition)

        data = small_game.advance_step()

        assert data['pov'] == hgs[5].serialize()
        assert small_game.step == Game.VETO_CEREMONY
        assert small_game.weeks.all()[0].pov == hgs[5]

    @pytest.mark.django_db
    def test_advance_from_veto_ceremony_to_eviction(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        small_game.hoh = hgs[0]
        small_game.nominees.set([hgs[1], hgs[2]])
        small_game.pov = hgs[2]
        small_game.step = Game.VETO_CEREMONY
        small_game.save()

        week = WeekFactory(number=1)
        week.save()
        small_game.weeks.add(week)

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
        assert list(small_game.weeks.all()[0].final_nominees.all()) == [hgs[1], hgs[3]]

    @pytest.mark.django_db
    def test_advance_from_eviction_to_memory_wall(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        def mock_run_eviction(obj):

            evc = EvictionCeremony(hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=[])
            evc.vote_count = [2, 1]
            evc.evicted = hgs[2]
            evc.tied = False

            return evc

        small_game.hoh = hgs[0]
        small_game.nominees.set([hgs[1], hgs[2]])
        small_game.step = Game.EVICTION
        small_game.save()

        week = WeekFactory(number=1)
        week.save()
        small_game.weeks.add(week)

        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        data = small_game.advance_step()

        expected_data = {
            "hoh": hgs[0].serialize(),
            "nominees": [x.serialize() for x in [hgs[1], hgs[2]]],
            "evicted": hgs[2].serialize(),
            "votes": [2, 1],
            "tied": False,
        }

        assert data['results'] == expected_data
        assert small_game.step == Game.MEMORYWALL
        assert small_game.weeks.all()[0].evicted == hgs[2]


    @pytest.mark.django_db
    def test_advance_from_eviction_to_finale(self, monkeypatch):

        g = GameFactory.create()

        hgs = HouseguestFactory.create_batch(4, game=g)

        def mock_run_eviction(obj):

            hgs[2].toggle_evicted(True)
            evc = EvictionCeremony(hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=[])
            evc.vote_count = [1, 0]
            evc.evicted = hgs[2]
            evc.tied = False

            return evc


        g.hoh = hgs[0]
        g.nominees.set([hgs[1], hgs[2]])
        g.step = Game.EVICTION
        g.save()

        week = WeekFactory(number=1)
        week.save()
        g.weeks.add(week)

        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        data = g.advance_step()

        expected_data = {
            "hoh": hgs[0].serialize(),
            "nominees": [x.serialize() for x in [hgs[1], hgs[2]]],
            "evicted": hgs[2].serialize(),
            "votes": [1, 0],
            "tied": False,
        }

        assert data['results'] == expected_data
        assert g.step == Game.FINALE
        assert g.weeks.all()[0].evicted == hgs[2]
        assert g.week_number == 1

    @pytest.mark.django_db
    def test_advance_from_finale(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        for hg in hgs[:3]:
            hg.toggle_evicted(True)

        small_game.jury.set(hgs[:3])
        small_game.step = Game.FINALE

        week = WeekFactory(number=1)
        week.save()
        small_game.weeks.add(week)

        def mock_run_finale(obj):

            obj.winner = hgs[5]

            return { "mock": "data" }

        def mock_week_serialize(obj):
            return { "mock": "week" }

        monkeypatch.setattr(Game, "run_finale", mock_run_finale)
        monkeypatch.setattr(Week, "serialize", mock_week_serialize)

        data = small_game.advance_step()

        assert data['results']['finale'] == { "mock": "data"}
        assert data['results']['summary']['weeks'] == [{ "mock": "week"}]
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
    def test_run_veto_ceremony_at_final_four(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 1 use on 1, Final: 3 and 4
        hgs = list(small_game.players.all())

        hgs[4].toggle_evicted(True)
        hgs[5].toggle_evicted(True)

        small_game.hoh = hgs[1]
        small_game.nominees.set([hgs[0], hgs[2]])
        small_game.pov = hgs[0]
        small_game.save()

        def mock_run_ceremony(obj):

            assert obj.hoh == hgs[1]
            obj.nominees = [hgs[2], hgs[3]]

        monkeypatch.setattr(VetoCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_veto_ceremony()

        assert set(small_game.nominees.all()) == set([hgs[3], hgs[2]])

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

        assert data.evicted == hgs[5]
        assert data.vote_count == [2, 1]
        assert data.tied is False

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

    @pytest.mark.django_db
    def test_get_summary(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())

        def mock_serialize(obj):
            return "Serialized week"

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5, 5 evicted
        week_1 = WeekFactory.create(number=1)

        # HOH: 1, Noms: 2, 3 POV: 1, not used, Final: 2 and 3, 3 evicted
        week_2 = WeekFactory.create(number=2)

        small_game.weeks.set([week_1, week_2])

        finale_info = { "finale": "mock_info" }

        monkeypatch.setattr(Week, "serialize", mock_serialize)

        expected_data = {
            "weeks": [week_1.serialize(), week_2.serialize()],
            "finale": finale_info
        }

        assert expected_data == small_game.get_summary(finale_info)

    @pytest.mark.django_db
    def test_full_sim(self):

        game = Game(user=UserFactory.create())
        game.save()
        for c in ContestantFactory.create_batch(16):
            _ = c.create_houseguest_clone(game_obj=game)

        game.setup_game()
        game.save()

        while game.completed is False:
            _ = game.advance_step()
            game.save()

        assert game.completed is True

