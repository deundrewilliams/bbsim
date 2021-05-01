from django.db import models


class Houseguest(models.Model):
    name = models.TextField(blank=False, null=False)
    immune = models.BooleanField(blank=False, null=False, default=False)
    evicted = models.BooleanField(blank=False, null=False, default=False)
    competition_count = models.IntegerField(blank=False, null=False, default=0)
    nomination_count = models.IntegerField(blank=False, null=False, default=0)

    def serialize(self):
        data = {
            "name": self.name,
        }
        return data;
