import pytest

from ..factories import HouseguestFactory
from ..models import Week


class TestWeek:

    @pytest.mark.django_db
    def test_initialization(self):

        # HOH: 0, Init Noms: 1, 2, POV: 3, Final Noms: 1, 4, Evicted: 4
        hgs = HouseguestFactory.create_batch(6)

        w = Week(number=1, hoh=hgs[0], pov=hgs[3], evicted=hgs[4], vote_count=[3, 2], tied=True)
        w.save()

        hgs[2].name = "Mike"
        hgs[2].save()

        hgs[4].name = "Bill"
        hgs[4].save()

        w.initial_nominees.set([hgs[1], hgs[2]])
        w.final_nominees.set([hgs[1], hgs[4]])

        data = w.serialize()

        assert data['week_num'] == 1
        assert data['hoh'] == hgs[0].name
        assert data['inoms'] == [hgs[1].name, hgs[2].name]
        assert data['pov'] == hgs[3].name
        assert data['fnoms'] == [hgs[1].name, hgs[4].name]
        assert data['evicted'] == hgs[4].name
        assert data['vote_count'] == [3, 2]
        assert data['tied']

        print(data)
