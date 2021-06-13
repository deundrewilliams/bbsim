import pytest

from ..factories import HouseguestFactory, EvictionCeremonyFactory
from ..models import EvictionCeremony


class TestEvictionCeremony:
    @pytest.mark.django_db
    def test_initialization(self):
        """
        Initialize an EvictionCeremony object and check that its serialization matches
        """

        hgs = HouseguestFactory.create_batch(6)

        hoh = hgs[0]
        noms = [hgs[1], hgs[2]]

        ev = EvictionCeremony(hoh=hoh)
        ev.save()

        ev.nominees.set(noms)
        ev.participants.set(hgs)

        data = ev.serialize()

        assert data["HOH"] == hoh.serialize()
        assert data["Nominees"] == [x.serialize() for x in noms]
        assert data["Evicted"] is None
        assert data["Votes"] is None

    @pytest.mark.django_db
    def test_get_vote(self):

        hgs = HouseguestFactory.create_batch(6)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        ret = evc.get_vote(hgs[3], [hgs[1], hgs[2]])

        assert ret in [hgs[1], hgs[2]]

    @pytest.mark.django_db
    def test_run_voting(self, monkeypatch):

        # HOH: 0, Noms: 1 and 2, Voters: 3 -> 1, 4-> 2, 5 -> 1

        hgs = HouseguestFactory.create_batch(6)

        def mock_get_vote(obj, voter, voting_pool):
            if voter == hgs[3] or voter == hgs[5]:
                return hgs[1]
            else:
                return hgs[2]

        monkeypatch.setattr(EvictionCeremony, "get_vote", mock_get_vote)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        expected_votes = {
            hgs[3]: hgs[1],
            hgs[4]: hgs[2],
            hgs[5]: hgs[1],
        }

        received_votes = evc.run_voting([hgs[3], hgs[4], hgs[5]])

        assert received_votes == expected_votes

    @pytest.mark.django_db
    def test_count_votes_no_tie(self):

        hgs = HouseguestFactory.create_batch(6)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        votes = {
            hgs[3]: hgs[2],
            hgs[4]: hgs[1],
            hgs[5]: hgs[1],
        }

        expected_count = {hgs[2]: 1, hgs[1]: 2}

        vote_count = evc.count_votes(votes)

        assert vote_count == expected_count

    @pytest.mark.django_db
    def test_get_evicted_no_tie(self):

        hgs = HouseguestFactory.create_batch(6)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        count = {hgs[2]: 1, hgs[1]: 2}

        evictee = evc.get_evicted(count)

        assert evictee == [hgs[2]]

    @pytest.mark.django_db
    def test_get_evicted_tie(self):

        hgs = HouseguestFactory.create_batch(7)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        count = {hgs[2]: 2, hgs[1]: 2}

        evicted = evc.get_evicted(count)

        assert set(evicted) == set([hgs[1], hgs[2]])

    @pytest.mark.django_db
    def test_tiebreaker(self):

        hgs = HouseguestFactory.create_batch(6)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        evictee = evc.tiebreaker([hgs[1], hgs[2]])

        assert evictee in [hgs[1], hgs[2]]

    @pytest.mark.django_db
    def test_run_ceremony_no_tie(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(6)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        def mock_run_voting(a, b):
            votes = {
                hgs[3]: hgs[2],
                hgs[4]: hgs[1],
                hgs[5]: hgs[1],
            }
            return votes

        count = {hgs[2]: 1, hgs[1]: 2}

        def mock_count_votes(a, b):

            return count

        def mock_get_evicted(a, b):
            return [hgs[2]]

        monkeypatch.setattr(EvictionCeremony, "run_voting", mock_run_voting)
        monkeypatch.setattr(EvictionCeremony, "count_votes", mock_count_votes)
        monkeypatch.setattr(EvictionCeremony, "get_evicted", mock_get_evicted)

        evc.run_ceremony()

        assert evc.vote_count_objs == count
        assert evc.evicted == hgs[2]
        assert evc.tied is False
        assert evc.vote_count == [2, 1]

    @pytest.mark.django_db
    def test_run_ceremony_tie(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(5)

        evc = EvictionCeremonyFactory.create(
            hoh=hgs[0], nominees=[hgs[1], hgs[2]], participants=hgs
        )

        def mock_run_voting(a, b):
            votes = {
                hgs[3]: hgs[2],
                hgs[4]: hgs[1],
            }
            return votes

        count = {hgs[2]: 1, hgs[1]: 1}

        def mock_count_votes(a, b):

            return count

        def mock_get_evicted(a, b):
            return [hgs[2], hgs[1]]

        def mock_tiebreaker(a, b):
            return hgs[1]

        monkeypatch.setattr(EvictionCeremony, "run_voting", mock_run_voting)
        monkeypatch.setattr(EvictionCeremony, "count_votes", mock_count_votes)
        monkeypatch.setattr(EvictionCeremony, "get_evicted", mock_get_evicted)
        monkeypatch.setattr(EvictionCeremony, "tiebreaker", mock_tiebreaker)

        evc.run_ceremony()

        assert evc.vote_count_objs == count
        assert evc.tied
        assert evc.evicted == hgs[1]
        assert evc.vote_count == [2, 1]
