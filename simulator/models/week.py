from django.db import models
from django.contrib.postgres.fields import ArrayField

class Week(models.Model):

    number = models.IntegerField(unique=False)
    hoh = models.ForeignKey("Houseguest", on_delete=models.CASCADE, blank=True, null=True, related_name="weeks")
    initial_nominees = models.ManyToManyField("Houseguest", related_name="initial_noms_weeks", default=[])
    pov = models.ForeignKey("Houseguest", on_delete=models.CASCADE, related_name="pov_weeks", default=None, blank=True, null=True)
    final_nominees = models.ManyToManyField("Houseguest", related_name="final_noms_weeks", default=[])
    evicted = models.ForeignKey("Houseguest", on_delete=models.CASCADE, related_name="evicted_weeks", default=None, blank=True, null=True)
    vote_count = ArrayField(models.CharField(max_length=20), blank=True, default=list)
    tied = models.BooleanField(default=False)

    def serialize(self):
        print(f"In week # {self.number}")
        print(f"HOH: {self.hoh.name}")
        print(f"Initial nominees: {self.initial_nominees.all()}")
        print(f"POV: {self.pov.name}")
        print(f"Final nominees: {self.final_nominees.all()}")
        print(f"Evicted: {self.evicted.name}")

        data = {
            "week_num": self.number,
            "hoh": self.hoh.name,
            "initial_noms": [x.name for x in self.initial_nominees.all()],
            "pov": self.pov.name,
            "final_noms": [x.name for x in self.final_nominees.all()],
            "evicted": self.evicted.name,
            "vote_count": self.vote_count,
            "tied": self.tied,
        }
        return data
