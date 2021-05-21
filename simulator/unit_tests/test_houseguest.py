import pytest
import random
from ..models import Houseguest, Relationship
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

        assert len(list(hgs[0].relationships.all())) == 5

    @pytest.mark.django_db
    def test_impact_relationship_negative(self, monkeypatch):

        hgs = []
        hgs.append(HouseguestFactory(name="Mike"))
        hgs.append(HouseguestFactory(name="John"))

        for hg in hgs:
            hg.initialize_relationships(hgs)

        def mock_randint(lower, upper):

            assert lower == -10
            assert upper == 0

            return -2

        monkeypatch.setattr(random, "randint", mock_randint)

        hgs[0].impact_relationship(hgs[1], Houseguest.NEGATIVE)

        one_rel = hgs[0].relationships.get(player=hgs[1]).value
        two_rel = hgs[1].relationships.get(player=hgs[0]).value

        assert one_rel == Houseguest.NEUTRAL_RELATIONSHIP - 2
        assert two_rel == Houseguest.NEUTRAL_RELATIONSHIP - 2

    @pytest.mark.django_db
    def test_impact_relationship_positive(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(2)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        def mock_randint(lower, upper):

            assert lower == 0
            assert upper == 10

            return 3

        monkeypatch.setattr(random, "randint", mock_randint)

        hgs[0].impact_relationship(hgs[1], Houseguest.POSITIVE)

        assert hgs[0].relationships.get(player=hgs[1]).value == Houseguest.NEUTRAL_RELATIONSHIP + 3
        assert hgs[1].relationships.get(player=hgs[0]).value == Houseguest.NEUTRAL_RELATIONSHIP + 3

    @pytest.mark.django_db
    def test_impact_relationship_neutral(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(2)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        def mock_randint(lower, upper):

            assert lower == -5
            assert upper == 5

            return 1

        monkeypatch.setattr(random, "randint", mock_randint)

        hgs[0].impact_relationship(hgs[1], Houseguest.NEUTRAL)

        assert hgs[0].relationships.get(player=hgs[1]).value == Houseguest.NEUTRAL_RELATIONSHIP + 1
        assert hgs[1].relationships.get(player=hgs[0]).value == Houseguest.NEUTRAL_RELATIONSHIP + 1


    @pytest.mark.django_db
    def test_choose_negative_relationships_more_than_three_eligible(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(5)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        # Set to 0 to ensure that it will get selected
        rel = hgs[0].relationships.get(player=hgs[1])
        rel.value = 0
        rel.save()

        def mock_random_sample(population, sample_size):

            assert population == hgs[1:]
            assert sample_size == 3
            return [hgs[2], hgs[1], hgs[4]]

        monkeypatch.setattr(random, "sample", mock_random_sample)

        noms = hgs[0].choose_negative_relationships(hgs[1:])

        assert noms == [hgs[1]]

    @pytest.mark.django_db
    def test_choose_negative_relationships_less_than_three_eligible(self, monkeypatch):

        hgs = HouseguestFactory.create_batch(5)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        rel = hgs[0].relationships.get(player=hgs[1])
        rel.value = 0
        rel.save()

        rel = hgs[0].relationships.get(player=hgs[4])
        rel.value = -12
        rel.save()

        # HOH: 0, Noms: 2 and 4, POV: 4, Eligible: 1 and 3

        def mock_random_sample(population, sample_size):

            assert population == [hgs[1], hgs[3]]
            assert sample_size == 2
            return [hgs[3], hgs[1]]

        monkeypatch.setattr(random, "sample", mock_random_sample)

        noms = hgs[0].choose_negative_relationships([hgs[1], hgs[3]])

        assert noms == [hgs[1]]
