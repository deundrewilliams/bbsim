from django.db import models

from ..models import Houseguest

import random

class EvictionCeremony(models.Model):

    hoh = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="hoh_eviction")
    nominees = models.ManyToManyField('Houseguest', related_name="noms_eviction")
    participants = models.ManyToManyField('Houseguest', related_name="parts_eviction")
    completed = models.BooleanField(default=False)
    evicted = models.ForeignKey('Houseguest', on_delete=models.CASCADE, related_name="evicted_hg", blank=True, null=True)

    def serialize(self):
        data = {
            "HOH": self.hoh.serialize(),
            "Nominees": [x.serialize() for x in list(self.nominees.all())],
            "Evicted": self.evicted.serialize() if self.completed else None,
            "Votes": self.votes if self.completed else None
        }
        return data

    def run_ceremony(self):

        # Get voters (parts. excl. hoh and nominees)
        voters = list(filter(lambda x: x != self.hoh and x not in list(self.nominees.all()), list(self.participants.all())))

        # Run voting process
        votes = self.run_voting(voters)

        # Get count of votes
        vote_count = self.count_votes(votes)

        # Get evicted player
        evicted = self.get_evicted(vote_count)

        # If tied, go to tiebreaker
        if (len(evicted) > 1):
            evictee = self.tiebreaker(evicted)
            vote_count[evictee] += 1
        elif (len(evicted) == 0): # Final Eviction
            evictee = self.tiebreaker(list(self.nominees.all()))
            vote_count[evictee] = 1
        else:
            evictee = evicted[0]

        # Set votes
        self.votes = vote_count

        # Set evicted player
        self.evicted = evictee

    def run_voting(self, voters):

        votes = {}

        # Get vote for each voter
        for voter in voters:
            votee = self.get_vote(voter, list(self.nominees.all()))
            votes[voter] = votee

        return votes

    def count_votes(self, votes):

        vote_count = {k:0 for k in votes.values()}

        for v in list(votes.values()):
            vote_count[v] += 1

        vote_count = {k: v for k, v in sorted(vote_count.items(), key=lambda item: item[1], reverse=True)}

        return vote_count

    def get_vote(self, voter, voting_pool):

        return random.choice(voting_pool)

    def get_evicted(self, vote_count):

        vote_count = dict(vote_count)

        evicted = []

        max_vote = -1

        for k in vote_count.keys():
            if (max_vote == -1):
                max_vote = vote_count[k]
                evicted.append(k)
            # Don't have to check if greater because sorted in decreasing order
            elif (vote_count[k] == max_vote):
                evicted.append(k)

        return evicted

    def tiebreaker(self, tied):

        return random.choice(tied)
