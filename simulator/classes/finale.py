from ..classes import Competition, EvictionCeremony

import random


class Finale:
    def __init__(self, finalists, jury):
        self.finalists = finalists
        self.jury = jury
        self.winner = None
        self.completed = False

    def serialize(self):
        data = {
            "finalists": [x.serialize() for x in self.finalists],
            "jury": [x.serialize() for x in self.jury],
            "winner": self.winner.serialize() if self.completed else None,
            "part_one": self.part_one.serialize() if self.completed else None,
            "part_two": self.part_two.serialize() if self.completed else None,
            "final_hoh": self.final_hoh.serialize() if self.completed else None,
            "final_juror": self.final_juror.serialize() if self.completed else None,
            "votes": {k.name: self.votes[k].name for k in list(self.votes.keys())}
            if self.completed
            else None,
        }
        return data

    def run_finale(self):

        # Get Part 1 HOH
        self.part_one = self.run_final_hoh_comp(self.finalists)

        # Get Part 2 HOH
        self.part_two = self.run_final_hoh_comp(
            list(filter(lambda x: x != self.part_one, self.finalists))
        )

        self.final_hoh = self.run_final_hoh_comp([self.part_one, self.part_two])

        self.final_hoh.win_competition()

        # Run final eviction
        finalnoms = list(filter(lambda x: x != self.final_hoh, self.finalists))
        finalparts = self.finalists

        finalevc = EvictionCeremony(
            hoh=self.final_hoh, nominees=finalnoms, participants=finalparts
        )
        finalevc.run_ceremony()

        # Set final juror
        self.final_juror = finalevc.evicted
        self.jury.append(self.final_juror)
        self.finalists.remove(self.final_juror)

        # Run voting process
        self.votes = self.run_voting()
        vote_count = self.count_votes(self.votes)

        # Get winner
        self.winner = self.determine_winner(vote_count)

        self.completed = True

    def run_final_hoh_comp(self, players):

        # print(players)

        c = Competition(Competition.HOH, players)
        c.run_competition()
        winner = c.winner
        return winner

    def calculate_finalist_value(self, finalist):

        social_val = finalist.get_relationship_average()

        comp_val = (finalist.competition_count) * 5

        return social_val + comp_val

    def run_voting(self):

        votes = {}

        finalists = self.finalists

        finalist_values = (
            self.calculate_finalist_value(finalists[0]),
            self.calculate_finalist_value(finalists[1]),
        )

        # Iterate through each juror
        for juror in self.jury:

            # Get vote
            votes[juror] = self.get_vote(juror, finalists, finalist_values)

        return votes

    def get_vote(self, voter, finalists, finalist_values):

        # Get relationship + finalist value for finalist 1
        finalist_one_chance = (
            voter.relationships.get(player=finalists[0]).value + finalist_values[0]
        )

        # Get relationship + finalist value for finalist 2
        finalist_two_chance = (
            voter.relationships.get(player=finalists[1]).value + finalist_values[1]
        )

        # Generate a random number between 1 and the sum
        vote_roll = random.randint(1, finalist_one_chance + finalist_two_chance)

        # If num is <= finalist 1, finalist 1 gets the vote
        if vote_roll <= finalist_one_chance:
            return finalists[0]

        else:
            return finalists[1]

    def count_votes(self, votes):

        vote_count = {x: 0 for x in self.finalists}

        for voter in votes:
            vote_count[votes[voter]] += 1

        vote_count = {
            k: v for k, v in sorted(vote_count.items(), key=lambda item: item[1])
        }

        return vote_count

    def determine_winner(self, vote_count):

        return list(vote_count.keys())[1]
