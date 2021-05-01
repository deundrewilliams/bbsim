import pytest
from ..models import Houseguest
from ..factories import HouseguestFactory

class TestHouseguest():

    @pytest.mark.django_db
    def test_initialization(self):

        h = Houseguest(name="Jim")
        h.save()

        assert h.name == "Jim"

    @pytest.mark.django_db
    def test_serialization(self):

        hg = HouseguestFactory(name="Mike", immune=True)

        data = hg.serialize()

        assert data['name'] == 'Mike'
        assert data['immune'] == 'True'
        assert data['evicted'] == 'False'
        assert data['comp_count'] == 0
        assert data['nom_count'] == 0
