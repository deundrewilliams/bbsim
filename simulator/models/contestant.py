from django.db import models

from .houseguest import Houseguest


class Contestant(models.Model):

    name = models.TextField(blank=False, null=False)

    def serialize(self):
        return {
            "name": self.name,
        }

    def create_houseguest_clone(self):

        h = Houseguest(name=self.name)
        h.save()

        return h
