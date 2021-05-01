import pytest
from ..models import Houseguest

class TestHouseguest():

    @pytest.mark.django_db
    def test_initialization(self):

        h = Houseguest(name="Jim")
        h.save()

        assert h.name == "Jim"
