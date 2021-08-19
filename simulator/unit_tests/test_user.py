import pytest

from django.contrib.auth.models import User
from ..models import Game
from ..factories import GameFactory

class TestUser:

    @pytest.mark.django_db
    def test_get_all_games(self):

        user = User.objects.create_user(username='test', password='test')

        games = GameFactory.create_batch(3, user=user)

        owned_games = Game.objects.filter(user=user)

        assert owned_games.count() == 3
