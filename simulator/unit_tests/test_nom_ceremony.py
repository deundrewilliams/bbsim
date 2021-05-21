import pytest
from ..models import NominationCeremony, Houseguest
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
    def test_choose_nominees(self, monkeypatch):

        hgs = []
        hgs.append(HouseguestFactory.create(name="A"))
        hgs.append(HouseguestFactory.create(name="B"))
        hgs.append(HouseguestFactory.create(name="C"))
        hgs.append(HouseguestFactory.create(name="D"))

        def mock_choose_neg_rels(obj, pool, count):

            assert obj == hgs[0]
            assert count == 2
            assert pool == hgs[1:]

            return [hgs[1], hgs[3]]

        nc = NominationCeremonyFactory(participants=hgs, hoh=hgs[0])

        monkeypatch.setattr(Houseguest, "choose_negative_relationships", mock_choose_neg_rels)

        nominees = nc.choose_nominees(hgs[1:])

        assert nominees == [hgs[1], hgs[3]]

    @pytest.mark.django_db
    def test_run_ceremony(self, monkeypatch):

        hgs = []
        hgs.append(HouseguestFactory.create(name="A"))
        hgs.append(HouseguestFactory.create(name="B"))
        hgs.append(HouseguestFactory.create(name="C"))

        hoh = hgs[0]

        def mock_choose_nominees(obj, pool):
            assert pool == hgs[1:]

            return [hgs[0], hgs[2]]

        monkeypatch.setattr(NominationCeremony, "choose_nominees", mock_choose_nominees)

        nc = NominationCeremonyFactory(hoh=hoh, participants=hgs)

        nc.run_ceremony()

        nominees = list(nc.nominees.all())

        assert nominees == [hgs[0], hgs[2]]
