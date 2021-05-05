import pytest

from ..factories import HouseguestFactory, FinaleFactory
from ..models import Finale, Competition, EvictionCeremony

class TestFinale:

    @pytest.mark.django_db
    def test_initialization(self):

        hgs = HouseguestFactory.create_batch(9)

        finalists = hgs[:3]
        jury = hgs[3:]

        fn = Finale()
        fn.save()
        fn.finalists.set(finalists)
        fn.jury.set(jury)

        data = fn.serialize()

        assert data['Finalists'] == [x.serialize() for x in finalists]
        assert data['Jury'] == [x.serialize() for x in jury]
        assert data['Winner'] == None
        assert data['Final HOH'] == None
        assert data['Final Juror'] == None
        assert data['Votes'] == None

    @pytest.mark.django_db
    def test_run_voting(self, monkeypatch):
        finalists = HouseguestFactory.create_batch(2)
        jurors = HouseguestFactory.create_batch(5)

        f = FinaleFactory(finalists=finalists, jury=jurors)

        def mock_get_vote(obj, voter, votee):
            if (voter == jurors[0] or voter == jurors[1]):
                return finalists[0]
            else:
                return finalists[1]

        monkeypatch.setattr(Finale, "get_vote", mock_get_vote)

        expected_votes = {
            jurors[0]: finalists[0],
            jurors[1]: finalists[0],
            jurors[2]: finalists[1],
            jurors[3]: finalists[1],
            jurors[4]: finalists[1]
        }

        votes = f.run_voting()

        assert votes == expected_votes

    @pytest.mark.django_db
    def test_count_votes(self):

        finalists = HouseguestFactory.create_batch(2)
        jurors = HouseguestFactory.create_batch(5)

        f = FinaleFactory(finalists=finalists, jury=jurors)

        vote_dict = {
            jurors[0]: finalists[0],
            jurors[1]: finalists[1],
            jurors[2]: finalists[0],
            jurors[3]: finalists[1],
            jurors[4]: finalists[1]
        }

        expected_count = {
            finalists[1]: 3,
            finalists[0]: 2
        }

        vote_count = f.count_votes(vote_dict)

        assert vote_count == expected_count

    @pytest.mark.django_db
    def test_get_winner(self):

        finalists = HouseguestFactory.create_batch(2)
        jurors = HouseguestFactory.create_batch(5)

        f = FinaleFactory(finalists=finalists, jury=jurors)

        vote_count = {
            finalists[1]: 3,
            finalists[0]: 2
        }

        winner = f.determine_winner(vote_count)

        assert winner == finalists[1]

    @pytest.mark.django_db
    def test_get_vote(self):
        voter = HouseguestFactory.create()
        pool = HouseguestFactory.create_batch(5)

        f = FinaleFactory(finalists=pool, jury=[voter])

        votee = f.get_vote(voter, pool)

        assert votee in pool

    @pytest.mark.django_db
    def test_run_finale(self, monkeypatch):

        # P1: 1, P2: 0, P3: 0, Evicted: 1

        finalists = HouseguestFactory.create_batch(3)
        jurors = HouseguestFactory.create_batch(4)

        f0 = finalists[0]
        f1 = finalists[1]
        f2 = finalists[2]

        f = FinaleFactory(finalists=finalists, jury=jurors)

        def mock_run_competition(obj):

            if (len(list(obj.participants.all())) == 3):
                assert list(obj.participants.all()) == finalists
                return finalists[1]

            elif (list(obj.participants.all()) == [finalists[0], finalists[2]]):
                return finalists[0]

            elif (set(obj.participants.all()) == set([finalists[0], finalists[1]])):
                return finalists[0]

            else:
                raise Exception("Invalid participants")

        def mock_evc_run_ceremony(obj):

            assert set(obj.nominees.all()) == set([finalists[1], finalists[2]])

            obj.evicted = finalists[1]

        def mock_run_voting(obj):

            assert obj.final_hoh == f0
            assert obj.final_juror == f1

            assert set(obj.finalists.all()) == set([f0, f2])

            assert set(obj.jury.all()) == set([f1] + jurors)

            votes = {
                jurors[0]: f2,
                jurors[1]: f0,
                jurors[2]: f0,
                jurors[3]: f0,
                f1: f0,
            }

            return votes

        vote_count = {
                f2: 4,
                f0: 1
        }

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


