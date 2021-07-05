import random


class Competition:

    HOH = 1
    POV = 2

    COMPETITION_TYPE_CHOICES = (
        (HOH, "HOH"),
        (POV, "POV"),
    )

    def __init__(self, comp_type, participants):
        self.comp_type = comp_type
        self.participants = participants
        self.winner = None

    def serialize(self):
        """
        Returns a JSON formatted dictionary of a Competition model information

        :return: Information about a Competition
        :rtype: dict
        """

        data = {
            "type": self.COMPETITION_TYPE_CHOICES[self.comp_type - 1][1],
            "players": self.participants,
            "winner": "None" if not self.winner else self.winner.serialize(),
        }

        return data

    def run_competition(self):
        """
        Runs the competition process and stores in winner attribute
        """

        self.winner = self.pick_winner()

    def pick_winner(self):
        """
        Picks a winner of the competition

        :return: The chosen winner
        :rtype: simulator.models.Houseguest
        """

        winner = random.choice(self.participants)

        return winner
