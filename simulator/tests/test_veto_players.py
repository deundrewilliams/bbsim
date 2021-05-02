import pytest
from ..models import Competition, VetoPlayers
from ..factories import HouseguestFactory, VetoPlayersFactory

class TestVetoPlayers:

    @pytest.mark.django_db
    def test_initialization(self):

        hgs = []
        hgs.append(HouseguestFactory(name="A"))
        hgs.append(HouseguestFactory(name="B"))
        hgs.append(HouseguestFactory(name="C"))
        hgs.append(HouseguestFactory(name="D"))
        hgs.append(HouseguestFactory(name="E"))

        nominees = [hgs[0], hgs[1]]

        vp = VetoPlayers(hoh=hgs[2])

        vp.save()

        vp.nominees.set(nominees)

        vp.participants.set(hgs)

        assert list(vp.nominees.all()) == nominees
        assert list(vp.participants.all()) == hgs
        assert vp.hoh == hgs[2]
        assert list(vp.picked.all()) == []

    @pytest.mark.django_db
    def test_serialization_before_run(self):

        hgs = []
        hgs.append(HouseguestFactory(name="A"))
        hgs.append(HouseguestFactory(name="B"))
        hgs.append(HouseguestFactory(name="C"))
        hgs.append(HouseguestFactory(name="D"))
        hgs.append(HouseguestFactory(name="E"))

        noms = [hgs[0], hgs[1]]

        hoh = hgs[2]

        vps = VetoPlayersFactory.create(hoh=hoh, nominees=noms, participants=hgs)

        data = vps.serialize()

        assert data['HOH'] == hoh.serialize()
        assert data['Nominees'] == [x.serialize() for x in noms]
        assert data['Picked'] == []

    @pytest.mark.django_db
    def test_serialization_after_run(self):

        hgs = []
        hgs.append(HouseguestFactory(name="A"))
        hgs.append(HouseguestFactory(name="B"))
        hgs.append(HouseguestFactory(name="C"))
        hgs.append(HouseguestFactory(name="D"))
        hgs.append(HouseguestFactory(name="E"))

        noms = [hgs[0], hgs[1]]

        hoh = hgs[2]

        vps = VetoPlayersFactory.create(hoh=hoh, nominees=noms, participants=hgs)

        vps.pick_players()

        data = vps.serialize()

        assert data['HOH'] == hoh.serialize()
        assert data['Nominees'] == [x.serialize() for x in noms]
        assert len(data['Picked']) == len(hgs)

    @pytest.mark.django_db
    def test_pick_players_less_six(self):

        hgs = []
        hgs.append(HouseguestFactory(name="A"))
        hgs.append(HouseguestFactory(name="B"))
        hgs.append(HouseguestFactory(name="C"))
        hgs.append(HouseguestFactory(name="D"))
        hgs.append(HouseguestFactory(name="E"))

        noms = [hgs[0], hgs[1]]

        hoh = hgs[2]

        vps = VetoPlayersFactory.create(hoh=hoh, nominees=noms, participants=hgs)

        vps.pick_players()

        assert set(list(vps.picked.all())) == set(hgs)

    @pytest.mark.django_db
    def test_pick_players_more_six(self):

        hgs = []
        hgs.append(HouseguestFactory(name="A"))
        hgs.append(HouseguestFactory(name="B"))
        hgs.append(HouseguestFactory(name="C"))
        hgs.append(HouseguestFactory(name="D"))
        hgs.append(HouseguestFactory(name="E"))
        hgs.append(HouseguestFactory(name="F"))
        hgs.append(HouseguestFactory(name="G"))
        hgs.append(HouseguestFactory(name="H"))

        noms = [hgs[0], hgs[1]]

        hoh = hgs[2]

        vps = VetoPlayersFactory.create(hoh=hoh, nominees=noms, participants=hgs)

        vps.pick_players()

        assert len(set(vps.picked.all())) == 6

