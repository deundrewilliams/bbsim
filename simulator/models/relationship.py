from django.db import models


class Relationship(models.Model):

    DEFAULT_REL = 50

    player = models.ForeignKey(
        to="Houseguest", on_delete=models.CASCADE, related_name="affected_hg"
    )
    value = models.IntegerField(blank=False, null=False, default=50)

    def __str__(self):
        return f"{self.player.name} - {self.value}"
