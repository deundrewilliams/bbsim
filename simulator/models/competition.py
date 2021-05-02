from django.db import models

from . import Houseguest

import random


class Competition(models.Model):

    HOH = 1
    POV = 2

    COMPETITION_TYPE_CHOICES = (
        (HOH, 'HOH'),
        (POV, 'POV'),
    )

    comp_type = models.IntegerField(choices=COMPETITION_TYPE_CHOICES)
    participants = models.ManyToManyField('Houseguest', related_name="comp_participants")
    winner = models.ForeignKey('Houseguest', blank=True, null=True, on_delete=models.CASCADE, related_name="winner")

    def serialize(self):
        """
        Returns a JSON formatted dictionary of a Competition model information

        :return: Information about a Competition
        :rtype: dict
        """

        data = {
            "id": self.id,
            "type": self.COMPETITION_TYPE_CHOICES[self.comp_type - 1][1],
            "players": [x.serialize() for x in list(self.participants.all())],
            "winner": "None" if not self.winner else self.winner.serialize(),
        }

        return data

    def run_competition(self):
        """
        Runs the competition process

        :return: The winner of the competition
        :rtype: simulator.models.Houseguest
        """

        self.winner = self.pick_winner()

    def pick_winner(self):
        """
        Picks a winner of the competition

        :return: The chosen winner
        :rtype: simulator.models.Houseguest
        """

        winner = random.choice(list(self.participants.all()))

        return winner
