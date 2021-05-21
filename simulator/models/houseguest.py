import random
from django.db import models


class Houseguest(models.Model):

    NEUTRAL_RELATIONSHIP = 50

    POSITIVE = 1
    NEUTRAL = 2
    NEGATIVE = 3

    name = models.TextField(blank=False, null=False)
    game = models.ForeignKey(to="Game", on_delete=models.CASCADE, related_name="players")
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

    def initialize_relationships(self, houseguests):

        self.relationships = {k:self.NEUTRAL_RELATIONSHIP for k in houseguests if k != self}

        # print(f'{self}: {self.relationships}')

    def impact_relationship(self, affected_houseguest, impact_level):

        # POS: 0 to 4
        # NEU: -2 to 2
        # NEG: -4 to 0

        # Set upper bound and lower bound
        if impact_level == self.POSITIVE:
            upper = 5
            lower = 0
        elif impact_level == self.NEUTRAL:
            upper = 2
            lower = -2
        else:
            upper = 0
            lower = -5

        # Generate a random number between upper and lower bound
        impact_amount = random.randint(lower, upper)

        # Edit self's relationship with affected houseguest
        self.relationships[affected_houseguest] += impact_amount

        # Edit affected houseguest's relationship with self
        affected_houseguest.relationships[self] += impact_amount

    def choose_negative_relationships(self, eligible_houseguests, count=1):

        if (len(eligible_houseguests) == 1):
            return [eligible_houseguests[0]]

        # print(self)

        eligible_keys = [x for x in list(self.relationships.keys()) if x in eligible_houseguests]

        # print(eligible_keys)

        picked = []

        # While length of picked is less than requested
        while (len(picked) < count):

            # Get three random keys
            picked_keys = random.sample(eligible_keys, min(3, len(eligible_keys)))

            # print(picked_keys)

            # for key in picked_keys:
            #     print(f'Key: {key} Rel: {self.relationships[key]}')

            # Get the key with the minimum relationship
            picked_key = min(picked_keys, key=self.relationships.get)

            # print(picked)

            picked.append(picked_key)
            eligible_keys.remove(picked_key)

        return picked

