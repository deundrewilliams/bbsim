import pytest
from ..models import Contestant
from ..factories import ContestantFactory, HouseguestFactory


class TestContestant:

    @pytest.mark.django_db
    def test_serialization(self):

        c = ContestantFactory(name="Mike")

        data = c.serialize()

        assert data['name'] == "Mike"


    @pytest.mark.django_db
    def test_create_houseguest_clone(self):

        c = ContestantFactory(name="Jimmy")

        new_hg = c.create_houseguest_clone()

        assert new_hg.name == c.name


