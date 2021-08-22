from simulator.models import (
    Contestant,
    Houseguest,
    Game,
    Week
)
from faker import Faker
from django.contrib.auth.models import User

import factory
import random

fake = Faker()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username=factory.LazyAttribute(lambda x: str(random.randint(1, 1000000)))
    password='factorypassword'
    email=factory.LazyAttribute(lambda x: str(random.randint(1, 1000000)))

class ContestantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contestant

    name = fake.name()


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
    user = factory.SubFactory(UserFactory)

class HouseguestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Houseguest

    name = factory.LazyAttribute(lambda x: fake.first_name())
    game = factory.SubFactory(GameFactory)

class WeekFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Week

    number = 1

