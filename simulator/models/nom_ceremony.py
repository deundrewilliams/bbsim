from django.db import models
from . import Houseguest
import random

NUM_NOMINEES = 2

class NominationCeremony(models.Model):

    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE)
    participants = models.ManyToManyField('Houseguest', related_name="nom_participants")
    nominees = models.ManyToManyField('Houseguest', related_name="nominees", default=[])

    def serialize(self):

        data = {
            "HOH": self.hoh.serialize(),
            "participants": [x.serialize() for x in list(self.participants.all())],
            "nominees": [x.serialize() for x in list(self.nominees.all())]
        }

        return data

    def run_ceremony(self):

        # Get eligible people to be nominated
        nom_eligible = list(filter(lambda x: x != self.hoh and x.immune == False, self.participants.all()))

        # Get nominees
        self.nominees.set(self.choose_nominees(nom_eligible))


    def choose_nominees(self, nomination_pool):
        """
        Chooses nominees

        :param nomination_pool: List of houseguests to choose from
        :type nomination_pool: List of simulator.models.Houseguest
        :return: List of chosen nominees
        :rtype: List of simulator.models.Houseguest
        """

        return random.sample(nomination_pool, NUM_NOMINEES)
