import random


class EvictionCeremony:
    def __init__(self, hoh, nominees, participants, evicted=None, completed=False):
        self.hoh = hoh
        self.nominees = nominees
        self.participants = participants
        self.evicted = evicted
        self.completed = completed

    def serialize(self):
        data = {
            "HOH": self.hoh.serialize(),
            "Nominees": [x.serialize() for x in self.nominees],
            "Evicted": self.evicted.serialize() if self.completed else None,
            "Votes": self.vote_count if self.completed else None,
        }
        return data

    def run_ceremony(self, participants=None):

        # Get voters (parts. excl. hoh and nominees)

        voters = list(
            filter(
                lambda x: x != self.hoh and x not in self.nominees,
                participants or self.participants,
            )
        )

        # Run voting process
        votes = self.run_voting(voters)

        # Get count of votes
        self.vote_count_objs = self.count_votes(votes)

        # Get evicted player
        evicted = self.get_evicted(self.vote_count_objs)

        # Initialize tied to false
        self.tied = False

        # If tied, go to tiebreaker
        if len(evicted) > 1:
            evictee = self.tiebreaker(evicted)
            self.vote_count_objs[evictee] += 1
            self.tied = True
        elif len(evicted) == 0:  # Final Eviction
            evictee = self.tiebreaker(self.nominees)
            self.vote_count_objs[evictee] = 1
        else:
            evictee = evicted[0]

        vote_count_int = list(self.vote_count_objs.values())
        vote_count_int.sort(reverse=True)

        # Set vote count
        self.vote_count = vote_count_int

        # Set evicted player
        self.evicted = evictee

        self.completed = True

    def run_voting(self, voters):

        votes = {}

        # Get vote for each voter
        for voter in voters:
            votee = self.get_vote(voter, self.nominees)
            votes[voter] = votee

        return votes

    def count_votes(self, votes):

        vote_count = {k: 0 for k in votes.values()}

        for v in list(votes.values()):
            vote_count[v] += 1

        vote_count = {
            k: v
            for k, v in sorted(
                vote_count.items(), key=lambda item: item[1], reverse=True
            )
        }

        return vote_count

    def get_vote(self, voter, voting_pool):

        return voter.choose_negative_relationships(voting_pool)[0]

    def get_evicted(self, vote_count):

        vote_count = dict(vote_count)

        evicted = []

        max_vote = -1

        for k in vote_count.keys():
            if max_vote == -1:
                max_vote = vote_count[k]
                evicted.append(k)
            # Don't have to check if greater because sorted in decreasing order
            elif vote_count[k] == max_vote:
                evicted.append(k)

        return evicted

    def tiebreaker(self, tied):

        return random.choice(tied)
