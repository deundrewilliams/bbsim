from .models import *
from faker import Faker

import factory

fake = Faker()

class HouseguestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Houseguest
    name = fake.unique.first_name()

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
