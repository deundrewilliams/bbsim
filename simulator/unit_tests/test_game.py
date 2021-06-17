import pytest

from ..classes import Competition, NominationCeremony
from ..models import (
    Game,
    VetoCeremony,
    EvictionCeremony,
    Finale,
    Houseguest,
)
from ..factories import HouseguestFactory, GameFactory, WeekFactory


class TestGame:
    @pytest.mark.django_db
    def test_initialization(self):

        # hgs = HouseguestFactory.create_batch(12)

        g = Game()
        g.save()

        hgs = HouseguestFactory.create_batch(12, game=g)

        data = g.serialize()

        assert data["id"] == g.id
        assert data["players"] == [x.serialize() for x in hgs]
        assert data["weeks"] == []
        assert data["winner"] is None
        assert data["prejury"] == []
        assert data["jury"] == []

    @pytest.mark.django_db
    def test_determine_jury_size(self):

        g = GameFactory.create()

        _ = HouseguestFactory.create_batch(2, game=g)

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
            assert obj.participants == hgs
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
            assert obj.participants == hgs
            obj.nominees = [hgs[1], hgs[3]]

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
            assert obj.participants == hgs
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

        for hg in hgs:
            hg.initialize_relationships(hgs)

        small_game.in_house = hgs
        small_game.current_hoh = hgs[2]
        small_game.current_nominees = [hgs[3], hgs[5]]
        small_game.save()

        def mock_run_ceremony(obj):
            assert list(obj.nominees.all()) == [hgs[3], hgs[5]]
            assert obj.hoh == hgs[2]
            obj.evicted = hgs[5]
            obj.vote_count = [2, 1]
            obj.tied = False

        monkeypatch.setattr(EvictionCeremony, "run_ceremony", mock_run_ceremony)

        small_game.run_eviction()

        assert small_game.evicted == hgs[5]
        assert small_game.eviction_votes == [2, 1]

    @pytest.mark.django_db
    def test_run_week_at_jury(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5, 5 evicted
        hgs = list(small_game.players.all())

        small_game.in_house = hgs.copy()
        small_game.jury_began = False
        small_game.current_hoh = None
        small_game.jury_size = (
            4  # wouldn't actually be 4, but tests the first cpl lines of code
        )

        def mock_run_hoh_competition(obj, outgoing_hoh):
            assert (
                obj.jury_began
            )  # Once here, jury began should've been changed to True

            assert outgoing_hoh is None
            obj.current_hoh = hgs[2]
            hgs[2].win_competition()

        def mock_run_nomination_ceremony(obj):
            obj.current_nominees = [hgs[1], hgs[3]]

        def mock_get_veto_players(obj):
            return hgs

        def mock_run_veto_competition(obj, players):
            obj.pov_holder = hgs[4]
            hgs[4].win_competition()

        def mock_run_veto_cerermony(obj):
            obj.current_nominees = [hgs[3], hgs[5]]

        def mock_run_eviction(obj):
            obj.evicted = hgs[5]
            obj.eviction_votes = [2, 1]
            obj.tied = False

        monkeypatch.setattr(Game, "run_hoh_competition", mock_run_hoh_competition)
        monkeypatch.setattr(
            Game, "run_nomination_ceremony", mock_run_nomination_ceremony
        )
        monkeypatch.setattr(Game, "get_veto_players", mock_get_veto_players)
        monkeypatch.setattr(Game, "run_veto_ceremony", mock_run_veto_cerermony)
        monkeypatch.setattr(Game, "run_veto_competition", mock_run_veto_competition)
        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        _ = small_game.run_week(1)
        assert list(small_game.jury.all()) == [hgs[5]]
        assert hgs[5] not in small_game.in_house

    @pytest.mark.django_db
    def test_run_week_before_jury(self, small_game, monkeypatch):

        # HOH: 2, Noms: 1, 3, POV: 4 use on 1, Final: 3 and 5, 5 evicted
        hgs = list(small_game.players.all())

        small_game.in_house = hgs.copy()
        small_game.jury_began = False
        small_game.current_hoh = None
        small_game.jury_size = (
            1  # wouldn't actually be 4, but tests the first cpl lines of code
        )

        def mock_run_hoh_competition(obj, outgoing_hoh):
            assert obj.jury_began is False  # Jury began should not be true

            assert outgoing_hoh is None
            obj.current_hoh = hgs[2]
            hgs[2].win_competition()

        def mock_run_nomination_ceremony(obj):
            obj.current_nominees = [hgs[1], hgs[3]]

        def mock_get_veto_players(obj):
            return hgs

        def mock_run_veto_competition(obj, players):
            obj.pov_holder = hgs[4]
            hgs[4].win_competition()

        def mock_run_veto_cerermony(obj):
            obj.current_nominees = [hgs[3], hgs[5]]

        def mock_run_eviction(obj):
            obj.evicted = hgs[5]
            obj.eviction_votes = [2, 1]
            obj.tied = True

        monkeypatch.setattr(Game, "run_hoh_competition", mock_run_hoh_competition)
        monkeypatch.setattr(
            Game, "run_nomination_ceremony", mock_run_nomination_ceremony
        )
        monkeypatch.setattr(Game, "get_veto_players", mock_get_veto_players)
        monkeypatch.setattr(Game, "run_veto_ceremony", mock_run_veto_cerermony)
        monkeypatch.setattr(Game, "run_veto_competition", mock_run_veto_competition)
        monkeypatch.setattr(Game, "run_eviction", mock_run_eviction)

        w_data = small_game.run_week(1)

        assert w_data["hoh"] == hgs[2].name
        assert w_data["vote_count"] == [2, 1]
        assert w_data["tied"]

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
        assert small_game.final_juror == hgs[3]

    @pytest.mark.django_db
    def test_run_game(self, small_game, monkeypatch):

        hgs = list(small_game.players.all())
        # Wk 1: HOH - 0, Nom - 2 and 3, POV - 4, Final 2 and 3, Evicted: 3
        # Wk 2: HOH - 2, Nom - 0 and 4, POV - 0, Final 4 and 1, Evicted: 4
        # Wk 3: HOH - 0, Nom - 2 and 1, POV - 2, Final 1 and 5, Evicted: 5
        # Final 3: 0, 1, 2

        wk1 = WeekFactory(
            number=1,
            hoh=hgs[0],
            initial_nominees=[hgs[2], hgs[3]],
            pov=hgs[4],
            final_nominees=[hgs[2], hgs[3]],
            evicted=hgs[3],
        )
        wk2 = WeekFactory(
            number=2,
            hoh=hgs[2],
            initial_nominees=[hgs[0], hgs[4]],
            pov=hgs[0],
            final_nominees=[hgs[4], hgs[1]],
            evicted=hgs[4],
        )
        wk3 = WeekFactory(
            number=3,
            hoh=hgs[0],
            initial_nominees=[hgs[2], hgs[1]],
            pov=hgs[2],
            final_nominees=[hgs[1], hgs[5]],
            evicted=hgs[5],
        )

        wks = [wk1, wk2, wk3]

        small_game.in_house = hgs.copy()

        def mock_run_week(obj, week_num):

            if week_num == 1:
                obj.in_house.remove(hgs[3])
                obj.jury.add(hgs[3])
                return wks[0]
            elif week_num == 2:
                obj.in_house.remove(hgs[4])
                obj.jury.add(hgs[4])
                return wks[1]
            elif week_num == 3:
                obj.in_house.remove(hgs[5])
                obj.jury.add(hgs[5])
                return wks[2]
            else:
                print(f"Week num is {week_num}")
                assert False

        def mock_run_finale(obj):
            obj.winner = hgs[0]
            obj.final_juror = hgs[2]

        monkeypatch.setattr(Game, "run_week", mock_run_week)
        monkeypatch.setattr(Game, "run_finale", mock_run_finale)

        small_game.run_game()

        assert small_game.winner == hgs[0]
        assert small_game.final_juror == hgs[2]

        saved_wks = list(small_game.weeks)

        assert set(saved_wks) == set(wks)

        # sm = small_game.summarize()

        # print(sm)

        # assert False

    @pytest.mark.django_db
    def test_full(self):

        g = Game()
        g.save()

        hgs = []
        hgs.append(HouseguestFactory(name="A", game=g))
        hgs.append(HouseguestFactory(name="B", game=g))
        hgs.append(HouseguestFactory(name="C", game=g))
        hgs.append(HouseguestFactory(name="D", game=g))
        hgs.append(HouseguestFactory(name="E", game=g))
        hgs.append(HouseguestFactory(name="F", game=g))

        g.run_game()

        assert isinstance(g.winner, Houseguest)
