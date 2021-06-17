import random


class VetoPlayers:

    def __init__(self, hoh, nominees, participants):
        self.hoh = hoh
        self.nominees = nominees
        self.participants = participants
        self.picked = []

    def serialize(self):
        """
        Return a JSON serialized object of VetoPlayers

        :return: JSON serialized object
        :rtype: dict
        """

        data = {
            "HOH": self.hoh.serialize(),
            "Nominees": [x.serialize() for x in self.nominees],
            "Picked": [x.serialize() for x in self.picked],
        }

        return data

    def pick_players(self):

        eligible = list(
            filter(
                lambda x: x not in self.nominees and x != self.hoh,
                self.participants,
            )
        )

        target = 6

        picked_buffer = [self.hoh] + self.nominees

        while len(picked_buffer) < target and len(eligible) > 0:
            picked = random.choice(eligible)
            eligible.remove(picked)
            picked_buffer.append(picked)

        self.picked = picked_buffer
