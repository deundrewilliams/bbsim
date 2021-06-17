from simulator.models import (
    Contestant,
    Houseguest,
    Game,
    Finale,
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


class FinaleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Finale

    @factory.post_generation
    def finalists(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for finalist in extracted:
                self.finalists.add(finalist)

    @factory.post_generation
    def jury(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for juror in extracted:
                self.jury.add(juror)
