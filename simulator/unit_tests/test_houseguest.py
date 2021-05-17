import pytest
import random
from ..models import Houseguest
from ..factories import HouseguestFactory, ContestantFactory, GameFactory

class TestHouseguest():

    @pytest.mark.django_db
    def test_initialization(self):

        g = GameFactory()

        h = Houseguest(name="Jim", game=g)
        h.save()

        assert h.name == "Jim"

    @pytest.mark.django_db
    def test_serialization(self):

        g = GameFactory()

        hg = HouseguestFactory(name="Mike", immune=True, game=g)

        data = hg.serialize()

        assert data['name'] == 'Mike'
        assert data['immune'] == 'True'
        assert data['evicted'] == 'False'
        assert data['comp_count'] == 0
        assert data['nom_count'] == 0

    @pytest.mark.django_db
    def test_nominate(self):

        g = GameFactory()
        hg = HouseguestFactory(name="Jim", game=g)
        hg.nominate()

        assert hg.nomination_count == 1

    @pytest.mark.django_db
    def test_toggle_evicted(self):
        g = GameFactory()
        hg = HouseguestFactory(game=g)
        hg.toggle_evicted(True)

        assert hg.evicted == True

    @pytest.mark.django_db
    def test_win_competition(self):
        g = GameFactory()
        hg = HouseguestFactory(game=g)
        hg.win_competition()

        assert hg.competition_count == 1

    @pytest.mark.django_db
    def test_initialize_relationships(self):

        g = GameFactory()
        hgs = HouseguestFactory.create_batch(6, game=g)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        expected_rels = {k:Houseguest.NEUTRAL_RELATIONSHIP for k in hgs if k != hgs[0]}

        assert expected_rels == hgs[0].relationships

    @pytest.mark.django_db
    def test_impact_relationship_negative(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(2)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        def mock_randint(lower, upper):

            assert lower == -5
            assert upper == 0

            return -2

        monkeypatch.setattr(random, "randint", mock_randint)

        hgs[0].impact_relationship(hgs[1], Houseguest.NEGATIVE)

        assert hgs[0].relationships[hgs[1]] == Houseguest.NEUTRAL_RELATIONSHIP - 2
        assert hgs[1].relationships[hgs[0]] == Houseguest.NEUTRAL_RELATIONSHIP - 2

    @pytest.mark.django_db
    def test_impact_relationship_positive(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(2)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        def mock_randint(lower, upper):

            assert lower == 0
            assert upper == 5

            return 3

        monkeypatch.setattr(random, "randint", mock_randint)

        hgs[0].impact_relationship(hgs[1], Houseguest.POSITIVE)

        assert hgs[0].relationships[hgs[1]] == Houseguest.NEUTRAL_RELATIONSHIP + 3
        assert hgs[1].relationships[hgs[0]] == Houseguest.NEUTRAL_RELATIONSHIP + 3

    @pytest.mark.django_db
    def test_impact_relationship_neutral(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(2)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        def mock_randint(lower, upper):

            assert lower == -2
            assert upper == 2

            return 1

        monkeypatch.setattr(random, "randint", mock_randint)

        hgs[0].impact_relationship(hgs[1], Houseguest.NEUTRAL)

        assert hgs[0].relationships[hgs[1]] == Houseguest.NEUTRAL_RELATIONSHIP + 1
        assert hgs[1].relationships[hgs[0]] == Houseguest.NEUTRAL_RELATIONSHIP + 1

