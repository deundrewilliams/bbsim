import pytest
import random
from ..models import VetoCeremony, Houseguest
from ..factories import HouseguestFactory, VetoCeremonyFactory

class TestVetoCeremony:

    @pytest.mark.django_db
    def test_initialization(self):

        hgs = HouseguestFactory.create_batch(7)

        hoh = hgs[0]
        noms = [hgs[1], hgs[2]]
        veto_holder = hgs[2]

        vc = VetoCeremony(hoh=hoh, veto_holder=veto_holder)
        vc.save()
        vc.nominees.set(noms)
        vc.participants.set(hgs)

        assert list(vc.participants.all()) == hgs

        data = vc.serialize()
        assert data['HOH'] == hoh.serialize()
        assert data['Used'] == vc.using
        assert data['Final Nominees'] == [x.serialize() for x in noms]

    @pytest.mark.django_db
    def test_get_decision_using(self, monkeypatch):
        hgs = HouseguestFactory.create_batch(5)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        noms = [hgs[0], hgs[1]]

        vc = VetoCeremonyFactory.create(hoh=hgs[2], nominees=noms, participants=hgs, veto_holder=hgs[3])

        def mock_randint(lower, upper):
            return 22

        rel = hgs[3].relationships.get(player=hgs[1])
        rel.value = 72
        rel.save()

        monkeypatch.setattr(random, "randint", mock_randint)

        info = vc.get_decision()

        assert info['Using'] == True
        assert info['On'] == hgs[1]

    @pytest.mark.django_db
    def test_get_decision_not_using(self, monkeypatch):
        hgs = HouseguestFactory.create_batch(5)

        for hg in hgs:
            hg.initialize_relationships(hgs)

        noms = [hgs[0], hgs[1]]

        vc = VetoCeremonyFactory.create(hoh=hgs[2], nominees=noms, participants=hgs, veto_holder=hgs[3])

        def mock_randint(lower, upper):
            return 51

        monkeypatch.setattr(random, "randint", mock_randint)

        info = vc.get_decision()

        assert info['Using'] == False
        assert info['On'] == None

    @pytest.mark.django_db
    def test_get_renom(self):

        hgs = HouseguestFactory.create_batch(5)

        # HOH: 3, Noms: 0 and 1, POV: 2

        noms = [hgs[0], hgs[1]]

        holder = hgs[2]

        vc = VetoCeremonyFactory.create(hoh=hgs[3], nominees=noms, participants=hgs, veto_holder=holder)

        renom = vc.get_renom()

        assert renom != hgs[3] and renom not in noms and renom != holder

    @pytest.mark.django_db
    def test_run_ceremony_nom_winner(self, monkeypatch):

        # HOH: 0, Noms: 1 and 2, POV: 1, Renom: 3

        hgs = HouseguestFactory.create_batch(5)

        hoh = hgs[0]
        noms = [hgs[1], hgs[2]]
        pov = hgs[1]

        def mock_get_renom(a):
            return hgs[3]

        monkeypatch.setattr(VetoCeremony, "get_renom", mock_get_renom)

        vc = VetoCeremonyFactory.create(hoh=hoh, nominees=noms, veto_holder=pov, participants=hgs)

        vc.run_ceremony()

        assert set(vc.nominees.all()) == set([hgs[2], hgs[3]])


        # Assert serializer marks used as True
        data = vc.serialize()
        assert data['Used'] == True
        assert data['Final Nominees'] == [x.serialize() for x in [hgs[2], hgs[3]]]

    @pytest.mark.django_db
    def test_run_ceremony_final_four(self):

        # HOH: 0, Noms: 1 and 2, POV: 3

        hgs = HouseguestFactory.create_batch(4)

        hoh = hgs[0]
        noms = [hgs[1], hgs[2]]
        pov = hgs[3]

        vc = VetoCeremonyFactory.create(hoh=hoh, nominees=noms, veto_holder=pov, participants=hgs)

        vc.run_ceremony()

        assert vc.using == False
        assert list(vc.nominees.all()) == noms

    @pytest.mark.django_db
    def test_run_ceremony_other_winner(self, monkeypatch):

        # HOH: 0, Noms: 1 and 2, POV: 3 used on 1, Renom: 4

        hgs = HouseguestFactory.create_batch(5)

        hoh = hgs[0]
        noms = [hgs[1], hgs[2]]
        pov = hgs[3]

        def mock_get_decision(a):
            a.using = True
            return {'Using': True, 'On': hgs[1]}

        def mock_get_renom(a):
            return hgs[4]

        monkeypatch.setattr(VetoCeremony, "get_decision", mock_get_decision)
        monkeypatch.setattr(VetoCeremony, "get_renom", mock_get_renom)

        vc = VetoCeremonyFactory.create(hoh=hoh, nominees=noms, veto_holder=pov, participants=hgs)

        vc.run_ceremony()

        assert set(vc.nominees.all()) == set([hgs[2], hgs[4]])
