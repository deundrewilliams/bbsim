from django.db import models

from .houseguest import Houseguest


class Contestant(models.Model):

    name = models.TextField(blank=False, null=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def create_houseguest_clone(self, game_obj):

        h = Houseguest(name=self.name, game=game_obj)
        h.save()

        return h
