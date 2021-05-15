from .models import *
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
    name = fake.name()
    game = factory.SubFactory(GameFactory)

class CompetitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Competition

    comp_type = Competition.HOH

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)

class NominationCeremonyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NominationCeremony

    hoh = factory.SubFactory(HouseguestFactory)

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)

class VetoPlayersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VetoPlayers

    hoh = factory.SubFactory(HouseguestFactory)

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)

    @factory.post_generation
    def nominees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for nominee in extracted:
                self.nominees.add(nominee)

class VetoCeremonyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = VetoCeremony

    hoh = factory.SubFactory(HouseguestFactory)
    veto_holder = factory.SubFactory(HouseguestFactory)

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)

    @factory.post_generation
    def nominees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for nominee in extracted:
                self.nominees.add(nominee)

class EvictionCeremonyFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EvictionCeremony

    hoh = factory.SubFactory(HouseguestFactory)
    evicted = factory.SubFactory(HouseguestFactory)

    @factory.post_generation
    def participants(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for participant in extracted:
                self.participants.add(participant)

    @factory.post_generation
    def nominees(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for nominee in extracted:
                self.nominees.add(nominee)

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


