import pytest
from ..models import Competition
from ..factories import CompetitionFactory, HouseguestFactory

class TestHouseguest():

    @pytest.mark.django_db
    def test_initialization(self):

        hgs = HouseguestFactory.create_batch(5)

        comp = Competition(comp_type=Competition.HOH)

        comp.save()

        comp.participants.set(hgs)

        assert comp.comp_type == Competition.HOH
        assert list(comp.participants.all()) == hgs

    @pytest.mark.django_db
    def test_serialization(self):

        comp = CompetitionFactory()

        data = comp.serialize()

        assert data['type'] == "HOH"

    @pytest.mark.django_db
    def test_pick_winner(self):

        hgs = []

        hgs.append(HouseguestFactory(name="John"))
        hgs.append(HouseguestFactory(name="Bob"))
        hgs.append(HouseguestFactory(name="Jim"))
        hgs.append(HouseguestFactory(name="Mike"))

        comp = CompetitionFactory.create(participants=hgs)

        winner = comp.pick_winner()

        assert winner in list(comp.participants.all())


