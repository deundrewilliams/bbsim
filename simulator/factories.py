from .models import *

import factory

class HouseguestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Houseguest

