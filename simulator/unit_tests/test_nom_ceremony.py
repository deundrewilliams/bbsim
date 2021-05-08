import pytest
from ..models import NominationCeremony
from ..factories import HouseguestFactory, NominationCeremonyFactory


class TestNominationCeremony:

    @pytest.mark.django_db
    def test_initialization(self):

        hg = HouseguestFactory()

        participants = HouseguestFactory.create_batch(5)

        nc = NominationCeremony(hoh=hg)

        nc.save()

        nc.participants.set(participants)

        assert nc.hoh.serialize() == hg.serialize()
        assert list(nc.participants.all()) == participants

    @pytest.mark.django_db
    def test_serialization(self):

        nc = NominationCeremonyFactory()

        data = nc.serialize()

        assert data['HOH'] == nc.hoh.serialize()
        assert data['participants'] == [x.serialize() for x in list(nc.participants.all())]
        assert data['nominees'] == []

    @pytest.mark.django_db
    def test_choose_nominees(self):

        hgs = []
        hgs.append(HouseguestFactory.create(name="A"))
        hgs.append(HouseguestFactory.create(name="B"))
        hgs.append(HouseguestFactory.create(name="C"))

        nc = NominationCeremonyFactory(participants=hgs)

        nominees = nc.choose_nominees(hgs)

        for nom in nominees:
            assert nom in hgs

    @pytest.mark.django_db
    def test_run_ceremony(self, monkeypatch):

        hgs = []
        hgs.append(HouseguestFactory.create(name="A"))
        hgs.append(HouseguestFactory.create(name="B"))
        hgs.append(HouseguestFactory.create(name="C"))

        hoh = hgs[1]

        def mock_choose_nominees(a, b):
            return [hgs[0], hgs[2]]

        monkeypatch.setattr(NominationCeremony, "choose_nominees", mock_choose_nominees)

        nc = NominationCeremonyFactory(hoh=hoh, participants=hgs)

        nc.run_ceremony()

        nominees = list(nc.nominees.all())

        assert nominees == [hgs[0], hgs[2]]
