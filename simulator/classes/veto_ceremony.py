import random


class VetoCeremony:
    def __init__(self, hoh, nominees, veto_holder, participants, using=None):
        self.hoh = hoh
        self.nominees = nominees
        self.veto_holder = veto_holder
        self.participants = participants
        self.using = using
        self.decision_info = None

    def serialize(self):

        data = {
            "Decision": self.decision_info,
            "Final Nominees": [x.serialize() for x in self.nominees],
        }

        return data

    def run_ceremony(self):

        self.decision_info = {}

        # If veto holder is nominee, use on theirself
        if self.veto_holder in self.nominees:
            self.using = True
            self.decision_info["Using"] = True
            self.decision_info["On"] = self.veto_holder

        # If length of participants is 4 and holder is not hoh, don't use
        elif self.veto_holder != self.hoh and len(self.participants) == 4:
            self.using = False
            self.decision_info["Using"] = False
            self.decision_info["On"] = None

        # Else generate veto decision
        else:
            self.decision_info = self.get_decision()
            self.using = self.decision_info["Using"]

        # If using
        if self.using:

            # Determine renom
            renom = self.get_renom()

            renom.nominate()
            renom.impact_relationship(self.hoh, 3)

            # Remove old nominee from nominees, add new nominee
            self.nominees.remove(self.decision_info["On"])
            self.nominees.append(renom)

            self.decision_info["On"] = self.decision_info["On"].serialize()

    def get_decision(self):

        # Get the relationship with nominees, keep the max val and player
        max_hg = self.veto_holder.choose_positive_relationships(self.nominees)[0]
        max_val = self.veto_holder.relationships.get(player=max_hg).value

        # print(f'{max_hg} ({max_val})')

        # Generate a number 1 through 100, if <= max val, using, else not
        pick_value = random.randint(1, 100)

        if pick_value <= max_val:

            # Positively impact relationship
            max_hg.impact_relationship(self.hoh, 1)

            return {"Using": True, "On": max_hg}
        else:
            return {"Using": False, "On": None}

    def get_renom(self):

        # Create the nomination pool (excl. hoh, nominees, and veto holder)
        nom_pool = list(
            filter(
                lambda x: x != self.hoh
                and x not in self.nominees
                and x != self.veto_holder,
                self.participants,
            )
        )

        # Randomly pick from the nomination pool
        # renom = random.choice(nom_pool)
        renom = self.hoh.choose_negative_relationships(nom_pool)[0]

        # Return picked player
        return renom
