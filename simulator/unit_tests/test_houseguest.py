import pytest
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
    def test_unaffected(self):

        c = ContestantFactory()


        pass
