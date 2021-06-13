import pytest

from simulator.factories import GameFactory, HouseguestFactory


# coverage run --source=./simulator/models -m pytest
@pytest.fixture
def small_game():

    g = GameFactory.create()

    _ = HouseguestFactory.create_batch(6, game=g)

    return g
