from django.db import models

from ..models import Houseguest

class Week(models.Model):

    number = models.IntegerField(blank=False, null=False)
    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_hoh")
    initial_nominees = models.ManyToManyField('Houseguest', related_name="week_init_noms")
    pov = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_pov")
    final_nominees = models.ManyToManyField('Houseguest', related_name="week_final_noms")
    evicted = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_evicted")

    def serialize(self):
        data = {
            "week_num": self.number,
            "hoh": self.hoh.name,
            "inoms": [x.name for x in list(self.initial_nominees.all())],
            "pov": self.pov.name,
            "fnoms": [x.name for x in list(self.final_nominees.all())],
            "evicted": self.evicted.name,
        }
        return data

