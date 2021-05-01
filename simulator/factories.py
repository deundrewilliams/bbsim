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
