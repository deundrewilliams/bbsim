NUM_NOMINEES = 2


class NominationCeremony:

    def __init__(self, hoh, participants):

        self.hoh = hoh
        self.participants = participants
        self.nominees = []

    def serialize(self):

        data = {
            "HOH": self.hoh.serialize(),
            "participants": [x.serialize() for x in self.participants],
            "nominees": [x.serialize() for x in self.nominees],
        }

        return data

    def run_ceremony(self):

        # Get eligible people to be nominated
        nom_eligible = list(
            filter(
                lambda x: x != self.hoh and x.immune is False, self.participants
            )
        )

        # Get new nominees
        new_nominees = self.choose_nominees(nom_eligible)

        # Iterate through nominees and update their counts and impact rel with HOH
        for nom in new_nominees:
            nom.nominate()
            nom.impact_relationship(self.hoh, 3)

        # Set nominees
        self.nominees = new_nominees

    def choose_nominees(self, nomination_pool):
        """
        Chooses nominees

        :param nomination_pool: List of houseguests to choose from
        :type nomination_pool: List of simulator.models.Houseguest
        :return: List of chosen nominees
        :rtype: List of simulator.models.Houseguest
        """
        return self.hoh.choose_negative_relationships(nomination_pool, NUM_NOMINEES)
