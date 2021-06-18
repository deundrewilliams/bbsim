from simulator.models import (
    Contestant,
    Houseguest,
    Game,
    Week,
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

    hoh = factory.SubFactory(HouseguestFactory)
    evicted = factory.SubFactory(HouseguestFactory)
    pov = factory.SubFactory(HouseguestFactory)
    number = 1

    @factory.post_generation
    def initial_nominees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for nominee in extracted:
                self.initial_nominees.add(nominee)

    @factory.post_generation
    def final_nominees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for nominee in extracted:
                self.final_nominees.add(nominee)
