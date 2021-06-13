from django.db import models

# from ..models import Houseguest

import random


class VetoPlayers(models.Model):

    hoh = models.ForeignKey("Houseguest", on_delete=models.CASCADE)
    nominees = models.ManyToManyField("Houseguest", related_name="veto_player_nominees")
    participants = models.ManyToManyField(
        "Houseguest", related_name="veto_player_participants"
    )
    picked = models.ManyToManyField(
        "Houseguest", default=[], related_name="picked_players"
    )

    def serialize(self):
        """
        Return a JSON serialized object of VetoPlayers

        :return: JSON serialized object
        :rtype: dict
        """

        data = {
            "id": self.id,
            "HOH": self.hoh.serialize(),
            "Nominees": [x.serialize() for x in list(self.nominees.all())],
            "Picked": [x.serialize() for x in list(self.picked.all())],
        }

        return data

    def pick_players(self):

        eligible = list(
            filter(
                lambda x: x not in list(self.nominees.all()) and x != self.hoh,
                list(self.participants.all()),
            )
        )

        target = 6

        picked_buffer = [self.hoh] + list(self.nominees.all())

        while len(picked_buffer) < target and len(eligible) > 0:
            picked = random.choice(eligible)
            eligible.remove(picked)
            picked_buffer.append(picked)

        self.picked.set(picked_buffer)
