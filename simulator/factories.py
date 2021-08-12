from simulator.models import (
    Contestant,
    Houseguest,
    Game,
    Week
)
from faker import Faker

import factory

fake = Faker()


class ContestantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contestant

    name = fake.name()


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game


class HouseguestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Houseguest

    name = fake.first_name()
    game = factory.SubFactory(GameFactory)

class WeekFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Week

    number = 1
