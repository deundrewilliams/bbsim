import pytest

from simulator.factories import *

# coverage run --source=./simulator/models -m pytest
@pytest.fixture
def small_game():

    hgs = HouseguestFactory.create_batch(6)

    g = GameFactory.create(players=hgs)


    return g
