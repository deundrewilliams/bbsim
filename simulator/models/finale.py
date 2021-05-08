from django.db import models

from ..models import Houseguest, Competition, EvictionCeremony

import random

class Finale(models.Model):

    finalists = models.ManyToManyField('Houseguest', related_name="finalists")
    jury = models.ManyToManyField('Houseguest', related_name="jury")
    winner = models.ForeignKey('Houseguest', on_delete=models.CASCADE, blank=True, null=True)
    completed = models.BooleanField(default=False)

    def serialize(self):
        data = {
            "Finalists": [x.serialize() for x in list(self.finalists.all())],
            "Jury": [x.serialize() for x in list(self.jury.all())],
            "Winner": self.winner.serialize() if self.completed else None,
            "Final HOH": self.final_hoh.serialize() if self.completed else None,
            "Final Juror": self.final_juror.serialize() if self.completed else None,
            "Votes": {k.name:self.votes[k].name for k in list(self.votes.keys())} if self.completed else None,
        }
        return data

    def run_finale(self):

        # Get Part 1 HOH
        p1_hoh = self.run_final_hoh_comp(list(self.finalists.all()))

        # Get Part 2 HOH
        p2_hoh = self.run_final_hoh_comp(list(filter(lambda x: x != p1_hoh, list(self.finalists.all()))))

        self.final_hoh = self.run_final_hoh_comp([p1_hoh, p2_hoh])

        self.final_hoh.win_competition()

        # Run final eviction
        finalevc = EvictionCeremony(hoh=self.final_hoh)
        finalevc.save()
        finalevc.nominees.set(list(filter(lambda x: x != self.final_hoh, list(self.finalists.all()))))
        finalevc.participants.set(list(self.finalists.all()))

        finalevc.run_ceremony()

        # Set final juror
        self.final_juror = finalevc.evicted
        self.jury.add(self.final_juror)
        self.finalists.remove(self.final_juror)

        # Run voting process
        self.votes = self.run_voting()
        vote_count = self.count_votes(self.votes)

        # Get winner
        self.winner = self.determine_winner(vote_count)

        self.completed = True

    def run_final_hoh_comp(self, players):

        # print(players)

        c = Competition(comp_type=Competition.HOH)
        c.save()
        c.participants.set(players)
        c.run_competition()
        winner = c.winner
        return winner

    def run_voting(self):

        votes = {}

        # Iterate through each juror
        for juror in list(self.jury.all()):

            # Get vote
            votes[juror] = self.get_vote(juror, list(self.finalists.all()))

        return votes

    def get_vote(self, voter, voter_pool):

        return random.choice(voter_pool)

    def count_votes(self, votes):

        vote_count = {x:0 for x in list(self.finalists.all())}

        for voter in votes:
            vote_count[votes[voter]] += 1

        vote_count = {k: v for k, v in sorted(vote_count.items(), key=lambda item: item[1])}

        return vote_count

    def determine_winner(self, vote_count):

        return list(vote_count.keys())[1]
