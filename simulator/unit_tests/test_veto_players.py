import pytest
from ..classes import VetoPlayers
from ..factories import HouseguestFactory


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

        vp = VetoPlayers(hoh=hgs[2], nominees=nominees, participants=hgs)

        assert vp.nominees == nominees
        assert vp.participants == hgs
        assert vp.hoh == hgs[2]
        assert vp.picked == []

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

        vps = VetoPlayers(hoh=hoh, nominees=noms, participants=hgs)

        data = vps.serialize()

        assert data["HOH"] == hoh.serialize()
        assert data["Nominees"] == [x.serialize() for x in noms]
        assert data["Picked"] == []

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

        vps = VetoPlayers(hoh=hoh, nominees=noms, participants=hgs)

        vps.pick_players()

        data = vps.serialize()

        assert data["HOH"] == hoh.serialize()
        assert data["Nominees"] == [x.serialize() for x in noms]
        assert len(data["Picked"]) == len(hgs)

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

        vps = VetoPlayers(hoh=hoh, nominees=noms, participants=hgs)

        vps.pick_players()

        assert set(vps.picked) == set(hgs)

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

        vps = VetoPlayers(hoh=hoh, nominees=noms, participants=hgs)

        vps.pick_players()

        assert len(vps.picked) == 6
