from django.db import models

# from .game import Game

class Houseguest(models.Model):
    name = models.TextField(blank=False, null=False)
    game = models.ForeignKey(to="Game", on_delete=models.CASCADE, related_name="related_game")
    immune = models.BooleanField(blank=False, null=False, default=False)
    evicted = models.BooleanField(blank=False, null=False, default=False)
    competition_count = models.IntegerField(blank=False, null=False, default=0)
    nomination_count = models.IntegerField(blank=False, null=False, default=0)

    def serialize(self):
        data = {
            "id": self.id,
            "name": self.name,
            "immune": "True" if self.immune == True else "False",
            "evicted": "True" if self.evicted == True else "False",
            "comp_count": self.competition_count,
            "nom_count": self.nomination_count
        }
        return data

    def nominate(self):

        self.nomination_count += 1
        self.save()

    def toggle_evicted(self, status):

        self.evicted = status
        self.save()

    def win_competition(self):

        self.competition_count += 1
        self.save()







