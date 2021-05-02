from django.db import models

from ..models import Houseguest

class Week(models.Model):

    number = models.IntegerField(blank=False, null=False)
    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_hoh")
    inital_nominees = models.ManyToManyField('Houseguest', related_name="week_init_noms")
    pov = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_pov")
    final_nominees = models.ManyToManyField('Houseguest', related_name="week_final_noms")
    evicted = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_evicted")

    def serialize(self):
        data = {
            "Week Number": self.number,
            "HOH": self.hoh.name,
            "Initial Nominees": [x.name for x in list(self.inital_nominees.all())],
            "POV": self.pov.name,
            "Final Nominees": [x.name for x in list(self.final_nominees.all())],
            "Evicted": self.evicted.name,
        }
        return data

