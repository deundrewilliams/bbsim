from django.db import models
from django.contrib.postgres.fields import ArrayField

from ..models import Houseguest


class Week(models.Model):

    number = models.IntegerField(unique=True)
    hoh = models.ForeignKey("Houseguest", on_delete=models.CASCADE, blank=True, null=True, related_name="weeks")
    initial_nominees = models.ManyToManyField("Houseguest", related_name="initial_noms_weeks", default=[])
    pov = models.ForeignKey("Houseguest", on_delete=models.CASCADE, related_name="pov_weeks", default=None, blank=True, null=True)
    final_nominees = models.ManyToManyField("Houseguest", related_name="final_noms_weeks", default=[])
    evicted = models.ForeignKey("Houseguest", on_delete=models.CASCADE, related_name="evicted_weeks", default=None, blank=True, null=True)
    vote_count = models.CharField(max_length=10, default="")
    tied = models.BooleanField(default=False)

    def serialize(self):
        data = {
            "week_num": self.number,
            "hoh": self.hoh.name,
            "inoms": [x.name for x in self.initial_nominees],
            "pov": self.pov.name,
            "fnoms": [x.name for x in self.final_nominees],
            "evicted": self.evicted.name,
            "vote_count": self.vote_count,
            "tied": self.tied,
        }
        return data
