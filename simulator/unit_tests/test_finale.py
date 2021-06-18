import pytest

from ..classes import Competition, EvictionCeremony, Finale
from ..factories import HouseguestFactory
import random


class TestFinale:
    @pytest.mark.django_db
    def test_initialization(self):

        hgs = HouseguestFactory.create_batch(9)

        finalists = hgs[:3]
        jury = hgs[3:]

        fn = Finale(finalists=finalists, jury=jury)

        data = fn.serialize()

        assert data["finalists"] == [x.serialize() for x in finalists]
        assert data["jury"] == [x.serialize() for x in jury]
        assert data["winner"] is None
        assert data["final_hoh"] is None
        assert data["final_juror"] is None
        assert data["votes"] is None

    @pytest.mark.django_db
    def test_run_voting(self, monkeypatch):
        finalists = HouseguestFactory.create_batch(2)
        jurors = HouseguestFactory.create_batch(5)

        f = Finale(finalists=finalists, jury=jurors)

        def mock_get_vote(obj, voter, votee, vals):
            if voter == jurors[0] or voter == jurors[1]:
                return finalists[0]
            else:
                return finalists[1]

        monkeypatch.setattr(Finale, "get_vote", mock_get_vote)

        def mock_calculate_finalist_value(obj, finalist):

            assert finalist in finalists
            return 50

        monkeypatch.setattr(
            Finale, "calculate_finalist_value", mock_calculate_finalist_value
        )

        expected_votes = {
            jurors[0]: finalists[0],
            jurors[1]: finalists[0],
            jurors[2]: finalists[1],
            jurors[3]: finalists[1],
            jurors[4]: finalists[1],
        }

        votes = f.run_voting()

        assert votes == expected_votes

    @pytest.mark.django_db
    def test_count_votes(self):

        finalists = HouseguestFactory.create_batch(2)
        jurors = HouseguestFactory.create_batch(5)

        f = Finale(finalists=finalists, jury=jurors)

        vote_dict = {
            jurors[0]: finalists[0],
            jurors[1]: finalists[1],
            jurors[2]: finalists[0],
            jurors[3]: finalists[1],
            jurors[4]: finalists[1],
        }

        expected_count = {finalists[1]: 3, finalists[0]: 2}

        vote_count = f.count_votes(vote_dict)

        assert vote_count == expected_count

    @pytest.mark.django_db
    def test_get_winner(self):

        finalists = HouseguestFactory.create_batch(2)
        jurors = HouseguestFactory.create_batch(5)

        f = Finale(finalists=finalists, jury=jurors)

        vote_count = {finalists[0]: 2, finalists[1]: 3}

        winner = f.determine_winner(vote_count)

        assert winner == finalists[1]

    @pytest.mark.django_db
    def test_calculate_finalist_value(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(7)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        finalists = hgs[:3]
        jurors = hgs[3:]

        f0 = finalists[0]

        f0.competition_count = 3
        f0.save()

        f = Finale(finalists=finalists, jury=jurors)

        assert f.calculate_finalist_value(f0) == 65

    @pytest.mark.django_db
    def test_get_vote(self, monkeypatch):
        voter = HouseguestFactory.create()
        pool = HouseguestFactory.create_batch(5)

        f = Finale(finalists=pool, jury=[voter])

        def mock_randint(low, high):

            assert high == 45 + 65 + 100

            return 45

        voter.initialize_relationships(pool)

        for hg in pool:
            hg.initialize_relationships(pool + [voter])

        monkeypatch.setattr(random, "randint", mock_randint)

        votee = f.get_vote(voter, pool, (45, 65))

        assert votee == f.finalists[0]

    @pytest.mark.django_db
    def test_run_finale(self, monkeypatch):

        # P1: 1, P2: 0, P3: 0, Evicted: 1

        finalists = HouseguestFactory.create_batch(3)
        jurors = HouseguestFactory.create_batch(4)

        f0 = finalists[0]
        f1 = finalists[1]
        f2 = finalists[2]

        f = Finale(finalists=finalists, jury=jurors)

        def mock_run_competition(obj):

            if len(obj.participants) == 3:
                assert obj.participants == finalists
                obj.winner = finalists[1]

            elif obj.participants == [finalists[0], finalists[2]]:
                obj.winner = finalists[0]

            elif set(obj.participants) == set([finalists[0], finalists[1]]):
                obj.winner = finalists[0]

            else:
                raise Exception(f"Invalid participants {obj.participants}")

        def mock_evc_run_ceremony(obj):

            assert set(obj.nominees) == set([finalists[1], finalists[2]])

            obj.evicted = finalists[1]

        def mock_run_voting(obj):

            assert obj.final_hoh == f0
            assert obj.final_juror == f1

            assert set(obj.finalists) == set([f0, f2])

            assert set(obj.jury) == set([f1] + jurors)

            votes = {
                jurors[0]: f2,
                jurors[1]: f0,
                jurors[2]: f0,
                jurors[3]: f0,
                f1: f0,
            }

            return votes

        vote_count = {f2: 4, f0: 1}

        def mock_count_votes(obj, votes):

            assert obj.votes == votes
            return vote_count

        def mock_determine_winner(obj, counted_votes):

            assert counted_votes == vote_count
            return f0

        monkeypatch.setattr(Competition, "run_competition", mock_run_competition)
        monkeypatch.setattr(EvictionCeremony, "run_ceremony", mock_evc_run_ceremony)
        monkeypatch.setattr(Finale, "run_voting", mock_run_voting)
        monkeypatch.setattr(Finale, "count_votes", mock_count_votes)
        monkeypatch.setattr(Finale, "determine_winner", mock_determine_winner)

        f.run_finale()

        assert f.final_juror == f1
        assert f.winner == f0
        assert f.completed
