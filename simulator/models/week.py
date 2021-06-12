from django.db import models
from django.core.validators import int_list_validator

# from ..models import Houseguest

class Week(models.Model):

    number = models.IntegerField(blank=False, null=False)
    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_hoh")
    initial_nominees = models.ManyToManyField('Houseguest', related_name="week_init_noms")
    pov = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_pov")
    final_nominees = models.ManyToManyField('Houseguest', related_name="week_final_noms")
    evicted = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="week_evicted")
    vote_count = models.CharField(validators=[int_list_validator], max_length=20)
    tied = models.BooleanField(default=False)

    def serialize(self):
        data = {
            "week_num": self.number,
            "hoh": self.hoh.name,
            "inoms": [x.name for x in list(self.initial_nominees.all())],
            "pov": self.pov.name,
            "fnoms": [x.name for x in list(self.final_nominees.all())],
            "evicted": self.evicted.name,
            "vote_count": self.vote_count,
            "tied": self.tied,
        }
        return data

